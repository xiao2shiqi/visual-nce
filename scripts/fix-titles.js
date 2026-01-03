/**
 * Auto-fill empty title analysis (intro_2 segments) for NCE lessons
 * @author xiaobin
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const lessonsDir = path.join(__dirname, '../src/data/lessons');

// Common word analysis dictionary for titles
const wordDict = {
    // Articles
    'a': { pos: 'art.', meaning: '一个' },
    'an': { pos: 'art.', meaning: '一个' },
    'the': { pos: 'art.', meaning: '这，那' },
    // Prepositions
    'of': { pos: 'prep.', meaning: '...的' },
    'in': { pos: 'prep.', meaning: '在...里' },
    'on': { pos: 'prep.', meaning: '在...上' },
    'at': { pos: 'prep.', meaning: '在' },
    'to': { pos: 'prep.', meaning: '到，向' },
    'for': { pos: 'prep.', meaning: '为了' },
    'from': { pos: 'prep.', meaning: '从' },
    'by': { pos: 'prep.', meaning: '通过，被' },
    'with': { pos: 'prep.', meaning: '和，用' },
    'out': { pos: 'adv.', meaning: '出，外面' },
    'up': { pos: 'adv.', meaning: '向上' },
    'after': { pos: 'prep.', meaning: '在...之后' },
    // Conjunctions
    'and': { pos: 'conj.', meaning: '和' },
    'or': { pos: 'conj.', meaning: '或者' },
    // Common adjectives
    'good': { pos: 'adj.', meaning: '好的' },
    'new': { pos: 'adj.', meaning: '新的' },
    'old': { pos: 'adj.', meaning: '老的，旧的' },
    'big': { pos: 'adj.', meaning: '大的' },
    'small': { pos: 'adj.', meaning: '小的' },
    'last': { pos: 'adj.', meaning: '最后的' },
    'first': { pos: 'adj.', meaning: '第一的' },
    'great': { pos: 'adj.', meaning: '伟大的' },
    'perfect': { pos: 'adj.', meaning: '完美的' },
    'successful': { pos: 'adj.', meaning: '成功的' },
    'noble': { pos: 'adj.', meaning: '高贵的' },
    'dead': { pos: 'adj.', meaning: '死的' },
    'future': { pos: 'adj.', meaning: '未来的' },
    // Common nouns (title keywords)
    'news': { pos: 'n.', meaning: '新闻' },
    'car': { pos: 'n.', meaning: '汽车' },
    'taxi': { pos: 'n.', meaning: '出租车' },
    'man': { pos: 'n.', meaning: '男人' },
    'men': { pos: 'n.', meaning: '男人们' },
    'woman': { pos: 'n.', meaning: '女人' },
    'day': { pos: 'n.', meaning: '天' },
    'night': { pos: 'n.', meaning: '夜晚' },
    'time': { pos: 'n.', meaning: '时间' },
    'life': { pos: 'n.', meaning: '生活' },
    'world': { pos: 'n.', meaning: '世界' },
    'house': { pos: 'n.', meaning: '房子' },
    'home': { pos: 'n.', meaning: '家' },
    'way': { pos: 'n.', meaning: '方式，路' },
    'end': { pos: 'n.', meaning: '结束，末端' },
    'air': { pos: 'n.', meaning: '空气，空中' },
    'water': { pos: 'n.', meaning: '水' },
    'fire': { pos: 'n.', meaning: '火' },
    'letter': { pos: 'n.', meaning: '信' },
    'letters': { pos: 'n.', meaning: '信件' },
    'trip': { pos: 'n.', meaning: '旅行' },
    'journey': { pos: 'n.', meaning: '旅程' },
    'trouble': { pos: 'n.', meaning: '麻烦' },
    'dream': { pos: 'n.', meaning: '梦想' },
    'dreams': { pos: 'n.', meaning: '梦想' },
    'gift': { pos: 'n.', meaning: '礼物' },
    'champion': { pos: 'n.', meaning: '冠军' },
    'champions': { pos: 'n.', meaning: '冠军们' },
    'fantasy': { pos: 'n.', meaning: '幻想' },
    'escape': { pos: 'n.', meaning: '逃跑' },
    'strike': { pos: 'n.', meaning: '罢工' },
    'control': { pos: 'n.', meaning: '控制' },
    'alibi': { pos: 'n.', meaning: '不在场证明' },
    'mine': { pos: 'n.', meaning: '矿井' },
    'slip': { pos: 'n.', meaning: '失误' },
    'tongue': { pos: 'n.', meaning: '舌头' },
    'supper': { pos: 'n.', meaning: '晚餐' },
    'basket': { pos: 'n.', meaning: '篮子' },
    'monster': { pos: 'n.', meaning: '怪物' },
    'fish': { pos: 'n.', meaning: '鱼' },
    'elections': { pos: 'n.', meaning: '选举' },
    'palace': { pos: 'n.', meaning: '宫殿' },
    'crystal': { pos: 'n.', meaning: '水晶' },
    'operation': { pos: 'n.', meaning: '手术' },
    'one': { pos: 'n.', meaning: '一个' },
    'three': { pos: 'num.', meaning: '三' },
    // Verbs
    'learn': { pos: 'v.', meaning: '学习' },
    'return': { pos: 'v.', meaning: '返回' },
    'asking': { pos: 'v.', meaning: '询问' },
    'trapped': { pos: 'v.', meaning: '被困' },
    // Adverbs
    'never': { pos: 'adv.', meaning: '从不' },
    'too': { pos: 'adv.', meaning: '太' },
    // Special
    "what's": { pos: 'phr.', meaning: '什么是' },
    'whats': { pos: 'phr.', meaning: '什么是' },
};

// Get prefix from args
const prefix = process.argv[2] || 'nce2';
const files = fs.readdirSync(lessonsDir)
    .filter(f => f.startsWith(`${prefix}-l`) && f.endsWith('.json'))
    .sort((a, b) => {
        const numA = parseInt(a.match(/l(\d+)/)?.[1] || '0');
        const numB = parseInt(b.match(/l(\d+)/)?.[1] || '0');
        return numA - numB;
    });

console.log(`\n📝 Fixing empty title analysis for ${prefix.toUpperCase()} lessons...\n`);

let fixedCount = 0;

files.forEach(filename => {
    const filePath = path.join(lessonsDir, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const lesson = JSON.parse(content);

    if (!lesson.segments) return;

    let modified = false;

    lesson.segments.forEach(segment => {
        // Only process intro_2 (title) segments with empty analysis
        if (segment.id === 'intro_2' && segment.analysis?.words?.length === 0) {
            const words = segment.text
                .replace(/[.,!?;:'"()\[\]{}]/g, '')
                .split(/\s+/)
                .filter(w => w.length > 0);

            const analysis = words.map(word => {
                const lower = word.toLowerCase();
                if (wordDict[lower]) {
                    return {
                        word: word,
                        pos: wordDict[lower].pos,
                        meaning: wordDict[lower].meaning
                    };
                } else {
                    // For unknown words, provide a placeholder that needs manual review
                    return {
                        word: word,
                        pos: 'n.',
                        meaning: `${word}（待补充）`
                    };
                }
            });

            segment.analysis.words = analysis;
            modified = true;
            console.log(`  ✅ Fixed: ${filename} - "${segment.text}"`);
            fixedCount++;
        }
    });

    if (modified) {
        fs.writeFileSync(filePath, JSON.stringify(lesson, null, 2) + '\n');
    }
});

console.log(`\n🎉 Done! Fixed ${fixedCount} title segments.\n`);
console.log('⚠️  Note: Some words marked as "待补充" may need manual review.\n');
