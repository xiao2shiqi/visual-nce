/**
 * 为 NCE4 添加单词解析（analysis.words）
 * 使用 NLP API 或本地词典生成单词的词性和释义
 * 用法: npx ts-node scripts/addWordAnalysis.ts
 */

import * as fs from 'fs';
import * as path from 'path';

interface WordInfo {
    word: string;
    pos: string;
    meaning: string;
}

interface Segment {
    id: string;
    role: string;
    text: string;
    translation: string;
    startTime: number;
    endTime: number;
    analysis?: {
        words: WordInfo[];
    };
}

interface LessonData {
    id: string;
    title: string;
    audio: string;
    image: string;
    segments: Segment[];
}

// 常见词词典
const COMMON_WORDS: { [word: string]: { pos: string; meaning: string } } = {
    'the': { pos: 'art.', meaning: '这，那（定冠词）' },
    'a': { pos: 'art.', meaning: '一个，一种（不定冠词）' },
    'an': { pos: 'art.', meaning: '一个，一种（不定冠词）' },
    'and': { pos: 'conj.', meaning: '和，与，及' },
    'or': { pos: 'conj.', meaning: '或，或者' },
    'but': { pos: 'conj.', meaning: '但是，然而' },
    'if': { pos: 'conj.', meaning: '如果，假如' },
    'when': { pos: 'conj.', meaning: '当...时，在...时' },
    'where': { pos: 'adv.', meaning: '在哪里，何处' },
    'while': { pos: 'conj.', meaning: '当...时，然而' },
    'since': { pos: 'prep.', meaning: '自从，因为' },
    'although': { pos: 'conj.', meaning: '虽然，尽管' },
    'though': { pos: 'conj.', meaning: '虽然，尽管' },
    'because': { pos: 'conj.', meaning: '因为' },
    'so': { pos: 'adv.', meaning: '所以，如此' },
    'for': { pos: 'prep.', meaning: '为了，因为' },
    'to': { pos: 'prep.', meaning: '向，到，对' },
    'of': { pos: 'prep.', meaning: '...的，关于' },
    'in': { pos: 'prep.', meaning: '在...里，在...期间' },
    'on': { pos: 'prep.', meaning: '在...上' },
    'at': { pos: 'prep.', meaning: '在，于，向' },
    'by': { pos: 'prep.', meaning: '通过，被，在...旁' },
    'with': { pos: 'prep.', meaning: '和...一起，用' },
    'from': { pos: 'prep.', meaning: '来自，从' },
    'about': { pos: 'prep.', meaning: '关于，大约' },
    'into': { pos: 'prep.', meaning: '进入，成为' },
    'over': { pos: 'prep.', meaning: '在...上方，超过' },
    'under': { pos: 'prep.', meaning: '在...下面，低于' },
    'through': { pos: 'prep.', meaning: '通过，穿过' },
    'during': { pos: 'prep.', meaning: '在...期间' },
    'within': { pos: 'prep.', meaning: '在...之内' },
    'without': { pos: 'prep.', meaning: '没有，不' },
    'as': { pos: 'prep.', meaning: '作为，像' },
    'than': { pos: 'conj.', meaning: '比' },
    'before': { pos: 'prep.', meaning: '在...之前' },
    'after': { pos: 'prep.', meaning: '在...之后' },
    'above': { pos: 'prep.', meaning: '在...上方' },
    'below': { pos: 'prep.', meaning: '在...下面' },
    'up': { pos: 'adv.', meaning: '向上' },
    'down': { pos: 'adv.', meaning: '向下' },
    'out': { pos: 'adv.', meaning: '出去，向外' },
    'off': { pos: 'adv.', meaning: '离开，关闭' },
    'very': { pos: 'adv.', meaning: '非常，很' },
    'too': { pos: 'adv.', meaning: '太，也' },
    'just': { pos: 'adv.', meaning: '刚刚，正好，仅仅' },
    'only': { pos: 'adv.', meaning: '只有，仅仅' },
    'also': { pos: 'adv.', meaning: '也，还' },
    'even': { pos: 'adv.', meaning: '甚至，即使' },
    'still': { pos: 'adv.', meaning: '仍然，还' },
    'already': { pos: 'adv.', meaning: '已经' },
    'never': { pos: 'adv.', meaning: '从不，决不' },
    'always': { pos: 'adv.', meaning: '总是，永远' },
    'often': { pos: 'adv.', meaning: '经常' },
    'sometimes': { pos: 'adv.', meaning: '有时' },
    'usually': { pos: 'adv.', meaning: '通常' },
    'well': { pos: 'adv.', meaning: '好，很好地' },
    'how': { pos: 'adv.', meaning: '如何，怎样' },
    'what': { pos: 'pron.', meaning: '什么' },
    'which': { pos: 'pron.', meaning: '哪个，哪些' },
    'who': { pos: 'pron.', meaning: '谁' },
    'whom': { pos: 'pron.', meaning: '谁（宾格）' },
    'whose': { pos: 'pron.', meaning: '谁的' },
    'this': { pos: 'pron.', meaning: '这，这个' },
    'that': { pos: 'pron.', meaning: '那，那个' },
    'these': { pos: 'pron.', meaning: '这些' },
    'those': { pos: 'pron.', meaning: '那些' },
    'it': { pos: 'pron.', meaning: '它' },
    'its': { pos: 'pron.', meaning: '它的' },
    'they': { pos: 'pron.', meaning: '他们，她们，它们' },
    'them': { pos: 'pron.', meaning: '他们（宾格）' },
    'their': { pos: 'pron.', meaning: '他们的' },
    'he': { pos: 'pron.', meaning: '他' },
    'him': { pos: 'pron.', meaning: '他（宾格）' },
    'his': { pos: 'pron.', meaning: '他的' },
    'she': { pos: 'pron.', meaning: '她' },
    'her': { pos: 'pron.', meaning: '她的，她（宾格）' },
    'we': { pos: 'pron.', meaning: '我们' },
    'us': { pos: 'pron.', meaning: '我们（宾格）' },
    'our': { pos: 'pron.', meaning: '我们的' },
    'you': { pos: 'pron.', meaning: '你，你们' },
    'your': { pos: 'pron.', meaning: '你的，你们的' },
    'i': { pos: 'pron.', meaning: '我' },
    'me': { pos: 'pron.', meaning: '我（宾格）' },
    'my': { pos: 'pron.', meaning: '我的' },
    'mine': { pos: 'pron.', meaning: '我的（名词性物主代词）' },
    'be': { pos: 'v.', meaning: '是，成为' },
    'am': { pos: 'v.', meaning: '是' },
    'is': { pos: 'v.', meaning: '是' },
    'are': { pos: 'v.', meaning: '是' },
    'was': { pos: 'v.', meaning: '是（过去式）' },
    'were': { pos: 'v.', meaning: '是（过去式）' },
    'been': { pos: 'v.', meaning: '是（过去分词）' },
    'have': { pos: 'v.', meaning: '有，已经' },
    'has': { pos: 'v.', meaning: '有' },
    'had': { pos: 'v.', meaning: '有（过去式）' },
    'do': { pos: 'v.', meaning: '做，干' },
    'does': { pos: 'v.', meaning: '做（第三人称单数）' },
    'did': { pos: 'v.', meaning: '做（过去式）' },
    'will': { pos: 'v.', meaning: '将，会' },
    'would': { pos: 'v.', meaning: '将，会（过去式）' },
    'could': { pos: 'v.', meaning: '能够，可以' },
    'should': { pos: 'v.', meaning: '应该' },
    'may': { pos: 'v.', meaning: '可能，可以' },
    'might': { pos: 'v.', meaning: '可能，也许' },
    'must': { pos: 'v.', meaning: '必须' },
    'can': { pos: 'v.', meaning: '能够，可以' },
    'not': { pos: 'adv.', meaning: '不，不是' },
    'no': { pos: 'det.', meaning: '没有，不' },
    'yes': { pos: 'adv.', meaning: '是，是的' },
    'all': { pos: 'det.', meaning: '所有的，全部' },
    'some': { pos: 'det.', meaning: '一些' },
    'many': { pos: 'det.', meaning: '许多' },
    'much': { pos: 'det.', meaning: '许多（不可数）' },
    'few': { pos: 'det.', meaning: '很少，少数' },
    'little': { pos: 'det.', meaning: '小的，少许' },
    'more': { pos: 'det.', meaning: '更多的' },
    'most': { pos: 'det.', meaning: '最多的' },
    'such': { pos: 'det.', meaning: '这样的，如此的' },
    'other': { pos: 'det.', meaning: '其他的' },
    'another': { pos: 'det.', meaning: '另一个' },
    'same': { pos: 'det.', meaning: '相同的' },
    'different': { pos: 'adj.', meaning: '不同的' },
    'new': { pos: 'adj.', meaning: '新的' },
    'old': { pos: 'adj.', meaning: '旧的，老的' },
    'good': { pos: 'adj.', meaning: '好的' },
    'bad': { pos: 'adj.', meaning: '坏的' },
    'big': { pos: 'adj.', meaning: '大的' },
    'small': { pos: 'adj.', meaning: '小的' },
    'large': { pos: 'adj.', meaning: '大的' },
    'long': { pos: 'adj.', meaning: '长的' },
    'short': { pos: 'adj.', meaning: '短的' },
    'high': { pos: 'adj.', meaning: '高的' },
    'low': { pos: 'adj.', meaning: '低的' },
    'first': { pos: 'num.', meaning: '第一' },
    'second': { pos: 'num.', meaning: '第二' },
    'third': { pos: 'num.', meaning: '第三' },
    'last': { pos: 'adj.', meaning: '最后的' },
    'next': { pos: 'adj.', meaning: '下一个' },
    'one': { pos: 'num.', meaning: '一' },
    'two': { pos: 'num.', meaning: '二' },
    'three': { pos: 'num.', meaning: '三' },
    'four': { pos: 'num.', meaning: '四' },
    'five': { pos: 'num.', meaning: '五' },
    'six': { pos: 'num.', meaning: '六' },
    'seven': { pos: 'num.', meaning: '七' },
    'eight': { pos: 'num.', meaning: '八' },
    'nine': { pos: 'num.', meaning: '九' },
    'ten': { pos: 'num.', meaning: '十' },
    'hundred': { pos: 'num.', meaning: '百' },
    'thousand': { pos: 'num.', meaning: '千' },
    'million': { pos: 'num.', meaning: '百万' },
    'time': { pos: 'n.', meaning: '时间，次' },
    'year': { pos: 'n.', meaning: '年' },
    'day': { pos: 'n.', meaning: '天，日' },
    'month': { pos: 'n.', meaning: '月' },
    'week': { pos: 'n.', meaning: '周' },
    'man': { pos: 'n.', meaning: '男人，人' },
    'men': { pos: 'n.', meaning: '男人们（复数）' },
    'woman': { pos: 'n.', meaning: '女人' },
    'women': { pos: 'n.', meaning: '女人们（复数）' },
    'people': { pos: 'n.', meaning: '人，人们' },
    'person': { pos: 'n.', meaning: '人' },
    'child': { pos: 'n.', meaning: '孩子' },
    'children': { pos: 'n.', meaning: '孩子们（复数）' },
    'thing': { pos: 'n.', meaning: '事情，东西' },
    'world': { pos: 'n.', meaning: '世界' },
    'life': { pos: 'n.', meaning: '生活，生命' },
    'hand': { pos: 'n.', meaning: '手' },
    'part': { pos: 'n.', meaning: '部分' },
    'way': { pos: 'n.', meaning: '方式，道路' },
    'work': { pos: 'n.', meaning: '工作' },
    'place': { pos: 'n.', meaning: '地方' },
    'case': { pos: 'n.', meaning: '情况，箱子' },
    'point': { pos: 'n.', meaning: '点，要点' },
    'fact': { pos: 'n.', meaning: '事实' },
    'question': { pos: 'n.', meaning: '问题' },
    'problem': { pos: 'n.', meaning: '问题' },
    'example': { pos: 'n.', meaning: '例子' },
    'reason': { pos: 'n.', meaning: '原因，理由' },
    'result': { pos: 'n.', meaning: '结果' },
    'kind': { pos: 'n.', meaning: '种类' },
    'lot': { pos: 'n.', meaning: '很多' },
    'make': { pos: 'v.', meaning: '做，制作' },
    'get': { pos: 'v.', meaning: '得到，获得' },
    'give': { pos: 'v.', meaning: '给，给予' },
    'take': { pos: 'v.', meaning: '拿，取' },
    'come': { pos: 'v.', meaning: '来' },
    'go': { pos: 'v.', meaning: '去' },
    'see': { pos: 'v.', meaning: '看见' },
    'know': { pos: 'v.', meaning: '知道' },
    'think': { pos: 'v.', meaning: '想，认为' },
    'look': { pos: 'v.', meaning: '看' },
    'want': { pos: 'v.', meaning: '想要' },
    'use': { pos: 'v.', meaning: '使用' },
    'find': { pos: 'v.', meaning: '找到' },
    'tell': { pos: 'v.', meaning: '告诉' },
    'ask': { pos: 'v.', meaning: '问' },
    'say': { pos: 'v.', meaning: '说' },
    'speak': { pos: 'v.', meaning: '说话' },
    'talk': { pos: 'v.', meaning: '谈话' },
    'call': { pos: 'v.', meaning: '叫，打电话' },
    'try': { pos: 'v.', meaning: '尝试' },
    'need': { pos: 'v.', meaning: '需要' },
    'feel': { pos: 'v.', meaning: '感觉' },
    'become': { pos: 'v.', meaning: '变成' },
    'leave': { pos: 'v.', meaning: '离开' },
    'put': { pos: 'v.', meaning: '放' },
    'mean': { pos: 'v.', meaning: '意味着' },
    'keep': { pos: 'v.', meaning: '保持' },
    'let': { pos: 'v.', meaning: '让' },
    'begin': { pos: 'v.', meaning: '开始' },
    'help': { pos: 'v.', meaning: '帮助' },
    'show': { pos: 'v.', meaning: '展示，显示' },
    'hear': { pos: 'v.', meaning: '听到' },
    'play': { pos: 'v.', meaning: '玩，播放' },
    'run': { pos: 'v.', meaning: '跑' },
    'move': { pos: 'v.', meaning: '移动' },
    'live': { pos: 'v.', meaning: '居住，生活' },
    'believe': { pos: 'v.', meaning: '相信' },
    'hold': { pos: 'v.', meaning: '持有，拥有' },
    'bring': { pos: 'v.', meaning: '带来' },
    'happen': { pos: 'v.', meaning: '发生' },
    'write': { pos: 'v.', meaning: '写' },
    'sit': { pos: 'v.', meaning: '坐' },
    'stand': { pos: 'v.', meaning: '站' },
    'lose': { pos: 'v.', meaning: '丢失' },
    'pay': { pos: 'v.', meaning: '支付' },
    'meet': { pos: 'v.', meaning: '遇见' },
    'learn': { pos: 'v.', meaning: '学习' },
    'change': { pos: 'v.', meaning: '改变' },
    'lead': { pos: 'v.', meaning: '领导，引导' },
    'understand': { pos: 'v.', meaning: '理解' },
    'watch': { pos: 'v.', meaning: '观看' },
    'follow': { pos: 'v.', meaning: '跟随' },
    'stop': { pos: 'v.', meaning: '停止' },
    'create': { pos: 'v.', meaning: '创造' },
    'speak': { pos: 'v.', meaning: '说话' },
    'read': { pos: 'v.', meaning: '读' },
    'spend': { pos: 'v.', meaning: '花费' },
    'grow': { pos: 'v.', meaning: '生长' },
    'open': { pos: 'v.', meaning: '打开' },
    'walk': { pos: 'v.', meaning: '走' },
    'win': { pos: 'v.', meaning: '赢' },
    'offer': { pos: 'v.', meaning: '提供' },
    'remember': { pos: 'v.', meaning: '记住' },
    'love': { pos: 'v.', meaning: '爱' },
    'consider': { pos: 'v.', meaning: '考虑' },
    'appear': { pos: 'v.', meaning: '出现' },
    'buy': { pos: 'v.', meaning: '买' },
    'wait': { pos: 'v.', meaning: '等待' },
    'serve': { pos: 'v.', meaning: '服务' },
    'die': { pos: 'v.', meaning: '死' },
    'send': { pos: 'v.', meaning: '发送' },
    'expect': { pos: 'v.', meaning: '期望' },
    'build': { pos: 'v.', meaning: '建造' },
    'stay': { pos: 'v.', meaning: '停留' },
    'fall': { pos: 'v.', meaning: '落下' },
    'cut': { pos: 'v.', meaning: '切' },
    'reach': { pos: 'v.', meaning: '到达' },
    'kill': { pos: 'v.', meaning: '杀死' },
    'remain': { pos: 'v.', meaning: '保持，剩余' },
    'suggest': { pos: 'v.', meaning: '建议' },
    'raise': { pos: 'v.', meaning: '提高，举起' },
    'pass': { pos: 'v.', meaning: '通过，传递' },
    'sell': { pos: 'v.', meaning: '卖' },
    'require': { pos: 'v.', meaning: '需要' },
    'report': { pos: 'v.', meaning: '报告' },
    'decide': { pos: 'v.', meaning: '决定' },
    'pull': { pos: 'v.', meaning: '拉' },
    'break': { pos: 'v.', meaning: '打破' },
    'thank': { pos: 'v.', meaning: '感谢' },
    'receive': { pos: 'v.', meaning: '接收' },
    'join': { pos: 'v.', meaning: '加入' },
    'cause': { pos: 'v.', meaning: '导致' },
    'represent': { pos: 'v.', meaning: '代表' },
    'subject': { pos: 'n.', meaning: '主题，科目' },
    'object': { pos: 'n.', meaning: '物体，对象' },
    'lesson': { pos: 'n.', meaning: '课程' },
    'story': { pos: 'n.', meaning: '故事' },
    'book': { pos: 'n.', meaning: '书' },
    'water': { pos: 'n.', meaning: '水' },
    'word': { pos: 'n.', meaning: '单词，词语' },
    'business': { pos: 'n.', meaning: '生意，业务' },
    'issue': { pos: 'n.', meaning: '问题，议题' },
    'side': { pos: 'n.', meaning: '边，侧面' },
    'head': { pos: 'n.', meaning: '头' },
    'house': { pos: 'n.', meaning: '房子' },
    'service': { pos: 'n.', meaning: '服务' },
    'friend': { pos: 'n.', meaning: '朋友' },
    'father': { pos: 'n.', meaning: '父亲' },
    'mother': { pos: 'n.', meaning: '母亲' },
    'parent': { pos: 'n.', meaning: '父母' },
    'student': { pos: 'n.', meaning: '学生' },
    'teacher': { pos: 'n.', meaning: '老师' },
    'school': { pos: 'n.', meaning: '学校' },
    'group': { pos: 'n.', meaning: '组，群体' },
    'country': { pos: 'n.', meaning: '国家' },
    'family': { pos: 'n.', meaning: '家庭' },
    'room': { pos: 'n.', meaning: '房间' },
    'body': { pos: 'n.', meaning: '身体' },
    'money': { pos: 'n.', meaning: '钱' },
    'name': { pos: 'n.', meaning: '名字' },
    'door': { pos: 'n.', meaning: '门' },
    'eye': { pos: 'n.', meaning: '眼睛' },
    'car': { pos: 'n.', meaning: '汽车' },
    'town': { pos: 'n.', meaning: '城镇' },
    'mind': { pos: 'n.', meaning: '思想， mind' },
    'back': { pos: 'n.', meaning: '背部，后面' },
    'parents': { pos: 'n.', meaning: '父母' },
    'moment': { pos: 'n.', meaning: '时刻' },
    'sense': { pos: 'n.', meaning: '感觉，意义' },
    'heart': { pos: 'n.', meaning: '心' },
    'thought': { pos: 'n.', meaning: '想法' },
    'history': { pos: 'n.', meaning: '历史' },
    'attention': { pos: 'n.', meaning: '注意' },
    'power': { pos: 'n.', meaning: '力量，电力' },
    'interest': { pos: 'n.', meaning: '兴趣' },
    'law': { pos: 'n.', meaning: '法律' },
    'end': { pos: 'n.', meaning: '结束，末端' },
    'course': { pos: 'n.', meaning: '课程，过程' },
    'control': { pos: 'n.', meaning: '控制' },
    'action': { pos: 'n.', meaning: '行动' },
    'view': { pos: 'n.', meaning: '观点，景色' },
    'relation': { pos: 'n.', meaning: '关系' },
    'town': { pos: 'n.', meaning: '城镇' },
    'price': { pos: 'n.', meaning: '价格' },
    'market': { pos: 'n.', meaning: '市场' },
    'value': { pos: 'n.', meaning: '价值' },
    'figure': { pos: 'n.', meaning: '数字，人物' },
    'street': { pos: 'n.', meaning: '街道' },
    'foot': { pos: 'n.', meaning: '脚' },
    'nature': { pos: 'n.', meaning: '自然' },
    'process': { pos: 'n.', meaning: '过程' },
    'morning': { pos: 'n.', meaning: '早晨' },
    'matter': { pos: 'n.', meaning: '事情，物质' },
    'section': { pos: 'n.', meaning: '部分，章节' },
    'field': { pos: 'n.', meaning: '领域，田野' },
    'poor': { pos: 'adj.', meaning: '贫穷的' },
    'young': { pos: 'adj.', meaning: '年轻的' },
    'able': { pos: 'adj.', meaning: '能够的' },
    'wrong': { pos: 'adj.', meaning: '错误的' },
    'possible': { pos: 'adj.', meaning: '可能的' },
    'real': { pos: 'adj.', meaning: '真实的' },
    'left': { pos: 'adj.', meaning: '左边的' },
    'important': { pos: 'adj.', meaning: '重要的' },
    'public': { pos: 'adj.', meaning: '公共的' },
    'political': { pos: 'adj.', meaning: '政治的' },
    'social': { pos: 'adj.', meaning: '社会的' },
    'full': { pos: 'adj.', meaning: '满的' },
    'special': { pos: 'adj.', meaning: '特别的' },
    'quite': { pos: 'adv.', meaning: '相当，非常' },
    'especially': { pos: 'adv.', meaning: '特别，尤其' },
    'probably': { pos: 'adv.', meaning: '可能' },
    'certainly': { pos: 'adv.', meaning: '当然' },
    'indeed': { pos: 'adv.', meaning: '的确' },
    'however': { pos: 'adv.', meaning: '然而' },
    'therefore': { pos: 'adv.', meaning: '因此' },
    'otherwise': { pos: 'adv.', meaning: '否则' },
    'already': { pos: 'adv.', meaning: '已经' },
    'yet': { pos: 'adv.', meaning: '还，然而' },
    'early': { pos: 'adv./adj.', meaning: '早的，早' },
    'late': { pos: 'adv./adj.', meaning: '晚的，晚' },
    'hard': { pos: 'adv./adj.', meaning: '努力的，硬的' },
    'both': { pos: 'det.', meaning: '两者都' },
    'either': { pos: 'det./conj.', meaning: '两者之一，或者' },
    'neither': { pos: 'det./conj.', meaning: '两者都不，也不' },
    'between': { pos: 'prep.', meaning: '在...之间' },
    'among': { pos: 'prep.', meaning: '在...之中' },
    'during': { pos: 'prep.', meaning: '在...期间' },
    'against': { pos: 'prep.', meaning: '反对，依靠' },
    'around': { pos: 'prep.', meaning: '围绕，大约' },
    'behind': { pos: 'prep.', meaning: '在...后面' },
    'beyond': { pos: 'prep.', meaning: '超过，在...之外' },
    'beside': { pos: 'prep.', meaning: '在...旁边' },
    'towards': { pos: 'prep.', meaning: '朝向' },
    'forward': { pos: 'adv.', meaning: '向前' },
    'backward': { pos: 'adv.', meaning: '向后' },
    'along': { pos: 'prep.', meaning: '沿着' },
    'across': { pos: 'prep.', meaning: '穿过' },
    'again': { pos: 'adv.', meaning: '再次' },
    'once': { pos: 'adv.', meaning: '一次' },
    'twice': { pos: 'adv.', meaning: '两次' },
    'ago': { pos: 'adv.', meaning: '以前' },
    'today': { pos: 'adv./n.', meaning: '今天' },
    'tomorrow': { pos: 'adv./n.', meaning: '明天' },
    'yesterday': { pos: 'adv./n.', meaning: '昨天' },
    'night': { pos: 'n.', meaning: '夜晚' },
    'noon': { pos: 'n.', meaning: '中午' },
    'evening': { pos: 'n.', meaning: '晚上' },
    'afternoon': { pos: 'n.', meaning: '下午' },
    'spring': { pos: 'n.', meaning: '春天，弹簧' },
    'summer': { pos: 'n.', meaning: '夏天' },
    'autumn': { pos: 'n.', meaning: '秋天' },
    'fall': { pos: 'v./n.', meaning: '落下，秋天' },
    'winter': { pos: 'n.', meaning: '冬天' },
    'season': { pos: 'n.', meaning: '季节' },
    'weather': { pos: 'n.', meaning: '天气' },
    'sun': { pos: 'n.', meaning: '太阳' },
    'moon': { pos: 'n.', meaning: '月亮' },
    'star': { pos: 'n.', meaning: '星星' },
    'earth': { pos: 'n.', meaning: '地球，土地' },
    'air': { pos: 'n.', meaning: '空气' },
    'light': { pos: 'n.', meaning: '光，灯' },
    'sound': { pos: 'n.', meaning: '声音' },
    'voice': { pos: 'n.', meaning: '声音，嗓音' },
    'noise': { pos: 'n.', meaning: '噪音' },
    'music': { pos: 'n.', meaning: '音乐' },
    'art': { pos: 'n.', meaning: '艺术' },
    'science': { pos: 'n.', meaning: '科学' },
    'language': { pos: 'n.', meaning: '语言' },
    'english': { pos: 'n./adj.', meaning: '英语，英国的' },
    'chinese': { pos: 'n./adj.', meaning: '中文，中国的' },
    'number': { pos: 'n.', meaning: '数字，号码' },
    'letter': { pos: 'n.', meaning: '字母，信' },
    'word': { pos: 'n.', meaning: '单词' },
    'sentence': { pos: 'n.', meaning: '句子' },
    'page': { pos: 'n.', meaning: '页' },
    'line': { pos: 'n.', meaning: '线，行' },
    'list': { pos: 'n.', meaning: '列表' },
    'paper': { pos: 'n.', meaning: '纸，论文' },
    'news': { pos: 'n.', meaning: '新闻' },
    'information': { pos: 'n.', meaning: '信息' },
    'data': { pos: 'n.', meaning: '数据' },
    'idea': { pos: 'n.', meaning: '想法' },
    'plan': { pos: 'n.', meaning: '计划' },
    'method': { pos: 'n.', meaning: '方法' },
    'system': { pos: 'n.', meaning: '系统' },
    'program': { pos: 'n.', meaning: '程序，项目' },
    'project': { pos: 'n.', meaning: '项目' },
    'product': { pos: 'n.', meaning: '产品' },
    'machine': { pos: 'n.', meaning: '机器' },
    'computer': { pos: 'n.', meaning: '电脑' },
    'phone': { pos: 'n.', meaning: '电话' },
    'internet': { pos: 'n.', meaning: '互联网' },
    'email': { pos: 'n.', meaning: '电子邮件' },
    'website': { pos: 'n.', meaning: '网站' },
    'technology': { pos: 'n.', meaning: '技术' },
    'development': { pos: 'n.', meaning: '发展' },
    'research': { pos: 'n.', meaning: '研究' },
    'university': { pos: 'n.', meaning: '大学' },
    'hospital': { pos: 'n.', meaning: '医院' },
    'hotel': { pos: 'n.', meaning: '酒店' },
    'restaurant': { pos: 'n.', meaning: '餐厅' },
    'store': { pos: 'n.', meaning: '商店' },
    'office': { pos: 'n.', meaning: '办公室' },
    'company': { pos: 'n.', meaning: '公司' },
    'industry': { pos: 'n.', meaning: '工业，行业' },
    'economy': { pos: 'n.', meaning: '经济' },
    'government': { pos: 'n.', meaning: '政府' },
    'society': { pos: 'n.', meaning: '社会' },
    'culture': { pos: 'n.', meaning: '文化' },
    'education': { pos: 'n.', meaning: '教育' },
    'experience': { pos: 'n.', meaning: '经验' },
    'knowledge': { pos: 'n.', meaning: '知识' },
    'ability': { pos: 'n.', meaning: '能力' },
    'skill': { pos: 'n.', meaning: '技能' },
    'habit': { pos: 'n.', meaning: '习惯' },
    'practice': { pos: 'n.', meaning: '练习' },
    'effect': { pos: 'n.', meaning: '效果，影响' },
    'effort': { pos: 'n.', meaning: '努力' },
    'success': { pos: 'n.', meaning: '成功' },
    'failure': { pos: 'n.', meaning: '失败' },
    'opportunity': { pos: 'n.', meaning: '机会' },
    'challenge': { pos: 'n.', meaning: '挑战' },
    'purpose': { pos: 'n.', meaning: '目的' },
    'goal': { pos: 'n.', meaning: '目标' },
    'dream': { pos: 'n.', meaning: '梦想' },
    'hope': { pos: 'v./n.', meaning: '希望，盼望' },
    'fear': { pos: 'n./v.', meaning: '恐惧，害怕' },
    'worry': { pos: 'v./n.', meaning: '担心，担忧' },
    'care': { pos: 'v./n.', meaning: '关心，照顾' },
    'danger': { pos: 'n.', meaning: '危险' },
    'risk': { pos: 'n.', meaning: '风险' },
    'chance': { pos: 'n.', meaning: '机会，偶然' },
    'advantage': { pos: 'n.', meaning: '优势' },
    'disadvantage': { pos: 'n.', meaning: '劣势' },
    'benefit': { pos: 'n.', meaning: '好处，利益' },
    'problem': { pos: 'n.', meaning: '问题' },
    'solution': { pos: 'n.', meaning: '解决方案' },
    'answer': { pos: 'n./v.', meaning: '答案，回答' },
    'question': { pos: 'n.', meaning: '问题' },
    'test': { pos: 'n./v.', meaning: '测试，考试' },
    'exam': { pos: 'n.', meaning: '考试' },
    'study': { pos: 'v./n.', meaning: '学习，研究' },
    'homework': { pos: 'n.', meaning: '家庭作业' },
    'class': { pos: 'n.', meaning: '班级，课' },
    'lesson': { pos: 'n.', meaning: '课程' },
    'meeting': { pos: 'n.', meaning: '会议' },
    'conference': { pos: 'n.', meaning: '会议' },
    'discussion': { pos: 'n.', meaning: '讨论' },
    'conversation': { pos: 'n.', meaning: '对话' },
    'message': { pos: 'n.', meaning: '信息' },
    'letter': { pos: 'n.', meaning: '信，字母' },
    'email': { pos: 'n.', meaning: '电子邮件' },
    'phone': { pos: 'n.', meaning: '电话' },
    'call': { pos: 'v./n.', meaning: '呼叫，电话' },
    'visit': { pos: 'v./n.', meaning: '访问，拜访' },
    'travel': { pos: 'v./n.', meaning: '旅行' },
    'trip': { pos: 'n.', meaning: '旅行' },
    'journey': { pos: 'n.', meaning: '旅程' },
    'tour': { pos: 'n.', meaning: '旅游' },
    'vacation': { pos: 'n.', meaning: '假期' },
    'holiday': { pos: 'n.', meaning: '假日' },
    'party': { pos: 'n.', meaning: '派对' },
    'event': { pos: 'n.', meaning: '事件' },
    'accident': { pos: 'n.', meaning: '事故' },
    'situation': { pos: 'n.', meaning: '情况' },
    'condition': { pos: 'n.', meaning: '条件' },
    'state': { pos: 'n.', meaning: '状态，国家' },
    'country': { pos: 'n.', meaning: '国家' },
    'nation': { pos: 'n.', meaning: '民族，国家' },
    'city': { pos: 'n.', meaning: '城市' },
    'village': { pos: 'n.', meaning: '村庄' },
    'address': { pos: 'n.', meaning: '地址' },
    'map': { pos: 'n.', meaning: '地图' },
    'direction': { pos: 'n.', meaning: '方向' },
    'distance': { pos: 'n.', meaning: '距离' },
    'speed': { pos: 'n.', meaning: '速度' },
    'energy': { pos: 'n.', meaning: '能量' },
    'force': { pos: 'n.', meaning: '力量' },
    'weight': { pos: 'n.', meaning: '重量' },
    'size': { pos: 'n.', meaning: '大小，尺寸' },
    'shape': { pos: 'n.', meaning: '形状' },
    'color': { pos: 'n.', meaning: '颜色' },
    'sound': { pos: 'n.', meaning: '声音' },
    'smell': { pos: 'n.', meaning: '气味' },
    'taste': { pos: 'n.', meaning: '味道' },
    'touch': { pos: 'v./n.', meaning: '触摸，接触' },
    'feeling': { pos: 'n.', meaning: '感觉' },
    'emotion': { pos: 'n.', meaning: '情感' },
    'mind': { pos: 'n.', meaning: '思想，头脑' },
    'brain': { pos: 'n.', meaning: '大脑' },
    'health': { pos: 'n.', meaning: '健康' },
    'disease': { pos: 'n.', meaning: '疾病' },
    'medicine': { pos: 'n.', meaning: '药，医学' },
    'doctor': { pos: 'n.', meaning: '医生' },
    'nurse': { pos: 'n.', meaning: '护士' },
    'hospital': { pos: 'n.', meaning: '医院' },
    'food': { pos: 'n.', meaning: '食物' },
    'drink': { pos: 'v./n.', meaning: '喝，饮料' },
    'eat': { pos: 'v.', meaning: '吃' },
    'meal': { pos: 'n.', meaning: '一餐' },
    'breakfast': { pos: 'n.', meaning: '早餐' },
    'lunch': { pos: 'n.', meaning: '午餐' },
    'dinner': { pos: 'n.', meaning: '晚餐' },
    'clothes': { pos: 'n.', meaning: '衣服' },
    'wear': { pos: 'v.', meaning: '穿' },
    'dress': { pos: 'v./n.', meaning: '穿衣，连衣裙' },
    'shoe': { pos: 'n.', meaning: '鞋子' },
    'hat': { pos: 'n.', meaning: '帽子' },
    'home': { pos: 'n./adv.', meaning: '家，在家' },
    'room': { pos: 'n.', meaning: '房间' },
    'kitchen': { pos: 'n.', meaning: '厨房' },
    'bedroom': { pos: 'n.', meaning: '卧室' },
    'bathroom': { pos: 'n.', meaning: '浴室' },
    'furniture': { pos: 'n.', meaning: '家具' },
    'table': { pos: 'n.', meaning: '桌子' },
    'chair': { pos: 'n.', meaning: '椅子' },
    'bed': { pos: 'n.', meaning: '床' },
};

// 提取句子中的单词
function extractWords(text: string): string[] {
    // 移除标点符号，拆分成单词
    const words = text
        .toLowerCase()
        .replace(/[.,!?;:'"(){}[\]<>|\\/]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .split(' ')
        .filter(w => w.length > 0 && !/^\d+$/.test(w)); // 过滤纯数字

    return [...new Set(words)]; // 去重
}

// 为单词生成解析
function analyzeWord(word: string): WordInfo | null {
    const lowerWord = word.toLowerCase();
    const originalWord = word;

    // 检查词典
    if (COMMON_WORDS[lowerWord]) {
        return {
            word: originalWord,
            pos: COMMON_WORDS[lowerWord].pos,
            meaning: COMMON_WORDS[lowerWord].meaning
        };
    }

    // 如果词典中没有，尝试推测词性和简单翻译
    // 对于未知单词，返回 null 表示需要手动处理
    return null;
}

async function processSegment(segment: Segment): Promise<boolean> {
    // 如果已经有 words 且不为空，跳过
    if (segment.analysis?.words && segment.analysis.words.length > 0) {
        return false;
    }

    const text = segment.text;
    const words = extractWords(text);
    const wordInfos: WordInfo[] = [];

    for (const word of words) {
        const info = analyzeWord(word);
        if (info) {
            wordInfos.push(info);
        }
    }

    // 更新 segment
    segment.analysis = {
        words: wordInfos
    };

    return wordInfos.length > 0;
}

async function processLesson(lessonPath: string): Promise<void> {
    console.log(`处理文件: ${path.basename(lessonPath)}`);

    const data: LessonData = JSON.parse(fs.readFileSync(lessonPath, 'utf-8'));
    let updatedCount = 0;

    for (let i = 0; i < data.segments.length; i++) {
        const segment = data.segments[i];
        const updated = await processSegment(segment);
        if (updated) {
            updatedCount++;
            console.log(`  [${i + 1}/${data.segments.length}] ${segment.text.substring(0, 40)}...`);
        }
    }

    if (updatedCount > 0) {
        fs.writeFileSync(lessonPath, JSON.stringify(data, null, 2), 'utf-8');
        console.log(`  ✓ 更新了 ${updatedCount} 个单词解析\n`);
    } else {
        console.log('  ✓ 所有单词解析已完整\n');
    }
}

async function main() {
    const lessonsDir = path.join(process.cwd(), 'src/data/lessons');
    const nce4Files = fs.readdirSync(lessonsDir)
        .filter(f => f.startsWith('nce4-l') && f.endsWith('.json'))
        .sort();

    console.log(`找到 ${nce4Files.length} 个 NCE 4 课程文件\n`);

    for (let i = 0; i < nce4Files.length; i++) {
        const file = nce4Files[i];
        const filePath = path.join(lessonsDir, file);
        console.log(`[${i + 1}/${nce4Files.length}] 处理 ${file}...`);

        try {
            await processLesson(filePath);
        } catch (error) {
            console.error(`  ✗ 处理失败:`, error);
        }
    }

    console.log('✓ 所有课程处理完成！');
}

main().catch(console.error);
