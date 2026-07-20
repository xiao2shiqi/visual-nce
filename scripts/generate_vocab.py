#!/usr/bin/env python3
"""
Generate per-lesson new-word lists (生词表) from lesson JSON.

Principle: New Concept English introduces vocabulary by first occurrence —
a word belongs to the lesson where it first shows up. We replay the book in
lesson order over `segments[].analysis.words` and emit each word once, at its
first appearance.

Output: src/data/vocab/{book}-l{n}.json

Re-runnable. The lesson JSON stays the single source of truth; if a lesson's
text or glosses change, just run this again.
"""

import json
import glob
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSON_DIR = os.path.join(ROOT, "src", "data", "lessons")
OUT_DIR = os.path.join(ROOT, "src", "data", "vocab")

BOOKS = ["nce1", "nce2"]

# Function words: real words, but not what a learner needs on a new-word list.
# Shared with check_missing_words.py's notion of "trivial".
TRIVIAL_WORDS = {
    'a', 'an', 'the',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their', 'this', 'that', 'these', 'those',
    'mine', 'yours', 'hers', 'ours', 'theirs', 'myself', 'yourself', 'himself',
    'herself', 'itself', 'ourselves', 'themselves',
    'in', 'on', 'at', 'to', 'for', 'of', 'by', 'with', 'from', 'into', 'onto',
    'up', 'down', 'out', 'over', 'under', 'about', 'as', 'after', 'before', 'during',
    'through', 'between', 'among', 'against', 'behind', 'beside', 'beyond', 'near',
    'off', 'since', 'until', 'within', 'without', 'along',
    'and', 'but', 'or', 'nor', 'so', 'yet', 'because', 'although', 'though', 'while',
    'when', 'where', 'if', 'unless', 'than', 'which',
    'who', 'whom', 'whose', 'whether', 'what', 'why', 'how',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should',
    'may', 'might', 'can', 'could', 'must',
    "isn't", "aren't", "wasn't", "weren't", "don't", "doesn't", "didn't",
    'not', 'no', 'yes', 'there', 'here', 'now', 'then', 'never', 'always', 'still',
    'just', 'also', 'too', 'very', 'more', 'most', 'all', 'any', 'some', 'each',
    'every', 'both', 'few', 'many', 'much', 'such', 'own', 'same', 'other', 'another',
    'one', 'two', 'three',
    # book scaffolding, not vocabulary
    'lesson',
}

# Segments that are pure scaffolding, e.g. "Lesson 1", "Listen to the tape then
# answer this question." — the latter still teaches words, so only kill numbering.
SCAFFOLD_RE = re.compile(r'^\s*lesson\s+\d+\s*$', re.I)


def clean(raw):
    """Strip surrounding punctuation/quotes from a stored word form."""
    # Edge-strip only, so an internal apostrophe ("don't") survives while a
    # leading quote ("'Excuse me,' she said") does not.
    return raw.strip().strip('.,!?;:"“”‘’\'()[]')


def lesson_num(path):
    return int(re.search(r'-l(\d+)\.json$', path).group(1))


def load_book(book):
    files = sorted(glob.glob(os.path.join(LESSON_DIR, f"{book}-l*.json")),
                   key=lesson_num)
    return [(f, json.load(open(f, encoding='utf-8'))) for f in files]


def iter_words(lessons):
    """Yield (lesson_path, segment, raw_word, entry, is_sentence_initial)."""
    for path, data in lessons:
        for seg in data.get('segments', []):
            text = seg.get('text', '') or ''
            if SCAFFOLD_RE.match(text):
                continue
            first_tok = clean(text.split()[0]).lower() if text.split() else None
            for entry in (seg.get('analysis') or {}).get('words', []):
                raw = clean(entry.get('word', ''))
                if not raw:
                    continue
                initial = raw.lower() == first_tok
                yield path, seg, raw, entry, initial


def build_proper_nouns(lessons):
    """A word is a proper noun if it is ever capitalized away from sentence start."""
    cap_noninitial = set()
    seen_lower = set()
    for _, _, raw, _, initial in iter_words(lessons):
        # Sentence-initial capitals carry no information either way — skip them
        # entirely rather than counting them as evidence.
        if initial:
            continue
        key = raw.lower()
        if raw[:1].isupper():
            cap_noninitial.add(key)
        else:
            seen_lower.add(key)
    # Ever seen lowercase mid-sentence => not a proper noun ("Nice"/"nice").
    return cap_noninitial - seen_lower


# The Chinese gloss already names the base form for inflected words, e.g.
# "包围（surround的过去分词）" / "去（go的过去式）". That is a far better lemma
# source than suffix guessing — it covers irregulars too.
_INFL = r'(?:过去式|过去分词|现在分词|复数|第三人称单数|比较级|最高级)'
# The marker may be followed by more useful text — "（复数，litter basket意为垃圾篓）"
# — so match up to a separator rather than demanding the closing paren.
GLOSS_BASE_RE = re.compile(
    r'[（(]\s*([A-Za-z][A-Za-z\'-]*)\s*的\s*' + _INFL + r'\s*(?=[）)，,/、])')
# Same marker, but without naming the base: "游客（复数）".
GLOSS_INFLECTED_RE = re.compile(
    r'[（(]\s*' + _INFL + r'\s*(?=[）)，,/、])')


# Irregular past / past-participle forms whose gloss does not flag them.
# A closed class, so an explicit table beats any suffix rule.
IRREGULAR = {}
for _base, _forms in {
    'be': 'was were been', 'become': 'became', 'begin': 'began begun',
    'bite': 'bit bitten', 'blow': 'blew blown', 'break': 'broke broken',
    'bring': 'brought', 'build': 'built', 'burn': 'burnt', 'buy': 'bought',
    'catch': 'caught', 'choose': 'chose chosen', 'come': 'came',
    'creep': 'crept', 'deal': 'dealt', 'dig': 'dug', 'draw': 'drew drawn',
    'drink': 'drank drunk', 'drive': 'drove driven', 'eat': 'ate eaten',
    'fall': 'fell fallen', 'feed': 'fed', 'feel': 'felt', 'fight': 'fought',
    'find': 'found', 'fly': 'flew flown', 'forget': 'forgot forgotten',
    'freeze': 'froze frozen', 'get': 'got gotten', 'give': 'gave given',
    'go': 'went gone', 'grow': 'grew grown', 'hang': 'hung', 'hear': 'heard',
    'hide': 'hid hidden', 'hold': 'held', 'keep': 'kept', 'know': 'knew known',
    'lay': 'laid', 'lead': 'led', 'learn': 'learnt', 'leave': 'left',
    'lend': 'lent', 'lie': 'lay lain', 'lose': 'lost', 'make': 'made',
    'mean': 'meant', 'meet': 'met', 'pay': 'paid', 'ride': 'rode ridden',
    'ring': 'rang rung', 'rise': 'rose risen', 'run': 'ran',
    'say': 'said', 'see': 'saw seen', 'seek': 'sought', 'sell': 'sold',
    'send': 'sent', 'shake': 'shook shaken', 'shine': 'shone',
    'shoot': 'shot', 'show': 'shown', 'sing': 'sang sung', 'sink': 'sank sunk',
    'sit': 'sat', 'sleep': 'slept', 'speak': 'spoke spoken', 'spend': 'spent',
    'stand': 'stood', 'steal': 'stole stolen', 'stick': 'stuck',
    'strike': 'struck', 'swear': 'swore sworn', 'sweep': 'swept',
    'swim': 'swam swum', 'take': 'took taken', 'teach': 'taught',
    'tear': 'tore torn', 'tell': 'told', 'think': 'thought',
    'throw': 'threw thrown', 'understand': 'understood', 'wake': 'woke woken',
    'wear': 'wore worn', 'weep': 'wept', 'win': 'won', 'write': 'wrote written',
}.items():
    for _f in _forms.split():
        IRREGULAR[_f] = _base


def base_from_gloss(word, meaning, vocab):
    """Base form declared by the gloss, or guessed when the gloss only flags it."""
    m = GLOSS_BASE_RE.search(meaning or '')
    if m:
        return m.group(1).lower()
    if GLOSS_INFLECTED_RE.search(meaning or ''):
        # The gloss confirms it is inflected but not of what. Only accept a
        # guess the book actually attests — an unchecked guess produces
        # non-words ("living" -> "liv").
        for guess in candidate_bases(word):
            if guess in vocab or guess in IRREGULAR:
                return guess
    return None


def strip_inflection_note(meaning):
    """Drop the '（surround的过去分词）' tail once the headword is the base form."""
    out = GLOSS_BASE_RE.sub('（', meaning or '')
    out = GLOSS_INFLECTED_RE.sub('（', out)
    # The marker is gone; tidy up what it left behind.
    out = re.sub(r'（\s*[，,]\s*', '（', out)      # "（，litter basket…" -> "（litter basket…"
    out = re.sub(r'（\s*[）)]', '', out)           # empty parens
    return out.strip().strip('，,、').strip() or (meaning or '')


def build_lemmas(vocab):
    """Map inflected form -> base form, but only when the base exists in the book.

    Conservative on purpose: we would rather list a word twice than hide a
    genuinely new one behind a bad stem.
    """
    lemma = {}
    for w in vocab:
        for base in candidate_bases(w):
            if base != w and base in vocab:
                lemma[w] = base
                break
    return lemma


def candidate_bases(w):
    """Plausible base forms for an inflected word, best guess first."""
    out = []
    if w.endswith('ies') and len(w) > 4:
        out.append(w[:-3] + 'y')
    if w.endswith('s') and not w.endswith('ss') and len(w) > 3:
        # "-es" only drops both letters after a sibilant (boxes -> box);
        # otherwise it is a plain "-s" on an "-e" stem (pieces -> piece).
        if w.endswith(('ses', 'xes', 'zes', 'ches', 'shes')):
            out.append(w[:-2])
        out.append(w[:-1])
    if w.endswith('ied') and len(w) > 4:
        out.append(w[:-3] + 'y')
    if w.endswith('ed') and len(w) > 3:
        out.append(w[:-2])
        out.append(w[:-1])                      # liked -> like
        if len(w) > 4 and w[-3] == w[-4]:
            out.append(w[:-3])                  # stopped -> stop
    if w.endswith('ing') and len(w) > 4:
        out.append(w[:-3])                      # walking -> walk
        out.append(w[:-3] + 'e')                # making -> make
        if len(w) > 5 and w[-4] == w[-5]:
            out.append(w[:-4])                  # running -> run
    # No -er/-est: those are derivational as often as inflectional
    # (writer is not a form of write), and a wrong merge hides a real word.
    return out


def generate(book):
    lessons = load_book(book)
    proper = build_proper_nouns(lessons)

    vocab = set()
    for _, _, raw, _, _ in iter_words(lessons):
        k = raw.lower()
        if k.isalpha():
            vocab.add(k)
    lemma = build_lemmas(vocab)

    seen = set()
    results = []
    for path, data in lessons:
        words = []
        for p, seg, raw, entry, _ in iter_words([(path, data)]):
            key = raw.lower()
            if not key.isalpha() or len(key) < 2:
                continue
            if key in TRIVIAL_WORDS:
                continue
            meaning = entry.get('meaning', '')
            # Gloss-declared base wins over suffix guessing.
            base = (base_from_gloss(key, meaning, vocab) or IRREGULAR.get(key)
                    or lemma.get(key, key))
            # A suffix guess can land on another inflected form
            # (hiding -> hid); finish the walk to the real base.
            base = IRREGULAR.get(base, base)
            if base in TRIVIAL_WORDS or base in seen:
                continue
            seen.add(base)
            seen.add(key)
            if base != key:
                meaning = strip_inflection_note(meaning)
            display = raw if key in proper else base
            words.append({
                "word": display,
                "pos": entry.get('pos', ''),
                "meaning": meaning,
                "firstSeg": seg.get('id', ''),
            })
        results.append((data['id'], words))

    os.makedirs(OUT_DIR, exist_ok=True)
    for lesson_id, words in results:
        with open(os.path.join(OUT_DIR, f"{lesson_id}.json"), 'w', encoding='utf-8') as fh:
            json.dump({"id": lesson_id, "words": words}, fh,
                      ensure_ascii=False, indent=2)
            fh.write('\n')

    counts = [len(w) for _, w in results]
    print(f"{book}: {len(results)} lessons, {sum(counts)} words, "
          f"min={min(counts)} median={sorted(counts)[len(counts)//2]} max={max(counts)}")
    return results


if __name__ == '__main__':
    for book in (sys.argv[1:] or BOOKS):
        generate(book)
