/**
 * 改进的 NCE4 翻译脚本
 * 使用多个翻译 API 源，避免限额问题
 * 用法: npx ts-node scripts/addTranslationsImproved.ts
 */

import * as fs from 'fs';
import * as path from 'path';

interface Segment {
    id: string;
    role: string;
    text: string;
    translation: string;
    startTime: number;
    endTime: number;
    analysis?: any;
}

interface LessonData {
    id: string;
    title: string;
    audio: string;
    image: string;
    segments: Segment[];
}

// 本地词典 - 用于快速翻译常见短语
const LOCAL_DICT: { [key: string]: string } = {
    'Lesson 1': '第1课', 'Lesson 2': '第2课', 'Lesson 3': '第3课', 'Lesson 4': '第4课', 'Lesson 5': '第5课',
    'Lesson 6': '第6课', 'Lesson 7': '第7课', 'Lesson 8': '第8课', 'Lesson 9': '第9课', 'Lesson 10': '第10课',
    'Lesson 11': '第11课', 'Lesson 12': '第12课', 'Lesson 13': '第13课', 'Lesson 14': '第14课', 'Lesson 15': '第15课',
    'Lesson 16': '第16课', 'Lesson 17': '第17课', 'Lesson 18': '第18课', 'Lesson 19': '第19课', 'Lesson 20': '第20课',
    'Lesson 21': '第21课', 'Lesson 22': '第22课', 'Lesson 23': '第23课', 'Lesson 24': '第24课', 'Lesson 25': '第25课',
    'Lesson 26': '第26课', 'Lesson 27': '第27课', 'Lesson 28': '第28课', 'Lesson 29': '第29课', 'Lesson 30': '第30课',
    'Lesson 31': '第31课', 'Lesson 32': '第32课', 'Lesson 33': '第33课', 'Lesson 34': '第34课', 'Lesson 35': '第35课',
    'Lesson 36': '第36课', 'Lesson 37': '第37课', 'Lesson 38': '第38课', 'Lesson 39': '第39课', 'Lesson 40': '第40课',
    'Lesson 41': '第41课', 'Lesson 42': '第42课', 'Lesson 43': '第43课', 'Lesson 44': '第44课', 'Lesson 45': '第45课',
    'Lesson 46': '第46课', 'Lesson 47': '第47课', 'Lesson 48': '第48课',
    'Listen to the tape then answer this question.': '听录音，然后回答问题。',
};

// 翻译 API 列表（按优先级排序）
const TRANSLATE_APIS = [
    {
        name: 'MyMemory',
        url: 'https://api.mymemory.translated.net/get',
        buildUrl: (text: string) => `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=en|zh`,
        parseResponse: (data: any) => data.responseData?.translatedText
    },
    {
        name: 'Google Translate (unofficial)',
        url: 'https://translate.googleapis.com/translate_a/single',
        buildUrl: (text: string) => `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=${encodeURIComponent(text)}`,
        parseResponse: (data: any) => data?.[0]?.[0]?.[0]
    }
];

let currentApiIndex = 0;
let lastApiCallTime = 0;
const MIN_DELAY_BETWEEN_CALLS = 3000; // 3 秒延迟

async function translateWithApi(text: string, apiIndex: number): Promise<{ success: boolean; translation?: string; error?: string }> {
    const api = TRANSLATE_APIS[apiIndex];

    try {
        // 添加延迟避免限额
        const now = Date.now();
        const timeSinceLastCall = now - lastApiCallTime;
        if (timeSinceLastCall < MIN_DELAY_BETWEEN_CALLS) {
            const delay = MIN_DELAY_BETWEEN_CALLS - timeSinceLastCall;
            await new Promise(resolve => setTimeout(resolve, delay));
        }

        const url = api.buildUrl(text);
        const response = await fetch(url, {
            method: 'GET',
            headers: { 'User-Agent': 'Mozilla/5.0' }
        });

        lastApiCallTime = Date.now();

        if (!response.ok) {
            return { success: false, error: `HTTP ${response.status}` };
        }

        const data = await response.json();
        const translation = api.parseResponse(data);

        if (translation) {
            return { success: true, translation };
        }

        return { success: false, error: 'No translation returned' };
    } catch (error) {
        return { success: false, error: String(error) };
    }
}

async function translateText(text: string): Promise<string> {
    if (!text || text.trim() === '') return '';

    // 检查本地词典
    if (LOCAL_DICT[text]) {
        return LOCAL_DICT[text];
    }

    // 尝试使用所有 API
    for (let i = 0; i < TRANSLATE_APIS.length; i++) {
        const apiIndex = (currentApiIndex + i) % TRANSLATE_APIS.length;
        const result = await translateWithApi(text, apiIndex);

        if (result.success && result.translation) {
            // 成功后切换到下一个 API（负载均衡）
            currentApiIndex = (apiIndex + 1) % TRANSLATE_APIS.length;
            return result.translation;
        }

        console.warn(`  ⚠ ${TRANSLATE_APIS[apiIndex].name} 失败: ${result.error}`);
    }

    return '';
}

async function processLesson(lessonPath: string): Promise<void> {
    console.log(`处理文件: ${path.basename(lessonPath)}`);

    const data: LessonData = JSON.parse(fs.readFileSync(lessonPath, 'utf-8'));
    let updatedCount = 0;

    const textsToTranslate: { segment: Segment; index: number }[] = [];
    for (let i = 0; i < data.segments.length; i++) {
        const segment = data.segments[i];
        if (!segment.translation || segment.translation.trim() === '') {
            textsToTranslate.push({ segment, index: i });
        }
    }

    if (textsToTranslate.length === 0) {
        console.log('  ✓ 所有翻译已完整\n');
        return;
    }

    console.log(`  需要翻译 ${textsToTranslate.length} 个片段`);

    for (const { segment, index } of textsToTranslate) {
        console.log(`  [${index + 1}/${data.segments.length}] ${segment.text.substring(0, 40)}...`);

        const translation = await translateText(segment.text);
        if (translation) {
            data.segments[index].translation = translation;
            updatedCount++;
            console.log(`    → ${translation.substring(0, 40)}...`);
        } else {
            console.log(`    ✗ 翻译失败`);
        }
    }

    if (updatedCount > 0) {
        fs.writeFileSync(lessonPath, JSON.stringify(data, null, 2), 'utf-8');
        console.log(`  ✓ 更新了 ${updatedCount} 个翻译\n`);
    } else {
        console.log(`  ✗ 未能翻译任何片段\n`);
    }
}

async function main() {
    const lessonsDir = path.join(process.cwd(), 'src/data/lessons');
    const nce4Files = fs.readdirSync(lessonsDir)
        .filter(f => f.startsWith('nce4-l') && f.endsWith('.json'))
        .sort();

    console.log(`找到 ${nce4Files.length} 个 NCE 4 课程文件`);
    console.log(`使用 ${TRANSLATE_APIS.length} 个翻译 API 源\n`);

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
