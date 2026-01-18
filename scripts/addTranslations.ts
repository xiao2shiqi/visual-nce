/**
 * 为 NCE 4 添加中文翻译
 * 使用 LibreTranslate 免费翻译 API
 * 用法: npx ts-node scripts/addTranslations.ts
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

// 翻译 API 配置 - 使用 MyMemory 免费 API
const TRANSLATE_API = 'https://api.mymemory.translated.net/get';

// 简单的翻译函数（使用 MyMemory 免费版，无需 API key）
async function translateText(text: string, retries = 3): Promise<string> {
    // 跳过已经翻译过的文本
    if (!text || text.trim() === '') return '';

    // 如果文本很短或是常见表达，使用本地词典
    const localDict: { [key: string]: string } = {
        'Lesson 1': '第1课',
        'Lesson 2': '第2课',
        'Lesson 3': '第3课',
        'Lesson 4': '第4课',
        'Lesson 5': '第5课',
        'Lesson 6': '第6课',
        'Lesson 7': '第7课',
        'Lesson 8': '第8课',
        'Lesson 9': '第9课',
        'Lesson 10': '第10课',
        'Lesson 11': '第11课',
        'Lesson 12': '第12课',
        'Lesson 13': '第13课',
        'Lesson 14': '第14课',
        'Lesson 15': '第15课',
        'Lesson 16': '第16课',
        'Lesson 17': '第17课',
        'Lesson 18': '第18课',
        'Lesson 19': '第19课',
        'Lesson 20': '第20课',
        'Lesson 21': '第21课',
        'Lesson 22': '第22课',
        'Lesson 23': '第23课',
        'Lesson 24': '第24课',
        'Lesson 25': '第25课',
        'Lesson 26': '第26课',
        'Lesson 27': '第27课',
        'Lesson 28': '第28课',
        'Lesson 29': '第29课',
        'Lesson 30': '第30课',
        'Lesson 31': '第31课',
        'Lesson 32': '第32课',
        'Lesson 33': '第33课',
        'Lesson 34': '第34课',
        'Lesson 35': '第35课',
        'Lesson 36': '第36课',
        'Lesson 37': '第37课',
        'Lesson 38': '第38课',
        'Lesson 39': '第39课',
        'Lesson 40': '第40课',
        'Lesson 41': '第41课',
        'Lesson 42': '第42课',
        'Lesson 43': '第43课',
        'Lesson 44': '第44课',
        'Lesson 45': '第45课',
        'Lesson 46': '第46课',
        'Lesson 47': '第47课',
        'Lesson 48': '第48课',
    };

    if (localDict[text]) {
        return localDict[text];
    }

    // 使用 MyMemory 翻译 API（免费，无需注册，每天有限额但足够用）
    try {
        const encodedText = encodeURIComponent(text);
        const url = `${TRANSLATE_API}?q=${encodedText}&langpair=en|zh`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0'
            }
        });

        if (!response.ok) {
            throw new Error(`Translation failed: ${response.status}`);
        }

        const data = await response.json();

        if (data.responseStatus === 200 && data.responseData?.translatedText) {
            return data.responseData.translatedText;
        }

        // 如果达到限额，返回原文标记
        if (data.responseStatus === 403 || data.responseStatus === 429) {
            console.warn('  ⚠ API 限额已达到，跳过此文本');
            return '';
        }

        return '';
    } catch (error) {
        if (retries > 0) {
            console.log(`  重试翻译 (${retries} 次剩余): ${text.substring(0, 30)}...`);
            await new Promise(resolve => setTimeout(resolve, 1000));
            return translateText(text, retries - 1);
        }
        console.error(`翻译失败: ${text}`, error);
        return ''; // 失败时返回空字符串
    }
}

// 批量翻译（避免 API 限流）
async function translateBatch(texts: string[]): Promise<string[]> {
    const results: string[] = [];
    for (const text of texts) {
        const translation = await translateText(text);
        results.push(translation);
        // 添加延迟避免限流
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    return results;
}

async function processLesson(lessonPath: string): Promise<void> {
    console.log(`处理文件: ${path.basename(lessonPath)}`);

    const data: LessonData = JSON.parse(fs.readFileSync(lessonPath, 'utf-8'));
    let updatedCount = 0;

    // 收集需要翻译的文本
    const textsToTranslate: { segment: Segment; index: number }[] = [];
    for (let i = 0; i < data.segments.length; i++) {
        const segment = data.segments[i];
        if (!segment.translation || segment.translation.trim() === '') {
            textsToTranslate.push({ segment, index: i });
        }
    }

    if (textsToTranslate.length === 0) {
        console.log('  ✓ 所有翻译已完整');
        return;
    }

    console.log(`  需要翻译 ${textsToTranslate.length} 个片段`);

    // 批量翻译（增加延迟避免 429 错误）
    let successCount = 0;
    let failCount = 0;

    for (const { segment, index } of textsToTranslate) {
        if (!segment.translation || segment.translation.trim() === '') {
            console.log(`  [${index + 1}/${data.segments.length}] ${segment.text.substring(0, 50)}...`);

            // 如果连续失败太多，暂停更长时间
            if (failCount >= 3) {
                console.log('  ⏸ 检测到多次失败，暂停 30 秒...');
                await new Promise(resolve => setTimeout(resolve, 30000));
                failCount = 0;
            }

            const translation = await translateText(segment.text);
            if (translation) {
                data.segments[index].translation = translation;
                updatedCount++;
                successCount++;
                failCount = 0;
            } else {
                failCount++;
            }

            // 增加延迟到 2 秒，避免 429 错误
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }

    // 保存更新后的文件
    if (updatedCount > 0) {
        fs.writeFileSync(lessonPath, JSON.stringify(data, null, 2), 'utf-8');
        console.log(`  ✓ 更新了 ${updatedCount} 个翻译`);
    }
}

async function main() {
    const lessonsDir = path.join(process.cwd(), 'src/data/lessons');

    // 获取所有 NCE4 课程
    const nce4Files = fs.readdirSync(lessonsDir)
        .filter(f => f.startsWith('nce4-l') && f.endsWith('.json'))
        .sort();

    console.log(`找到 ${nce4Files.length} 个 NCE 4 课程文件\n`);

    // 逐个处理
    for (let i = 0; i < nce4Files.length; i++) {
        const file = nce4Files[i];
        const filePath = path.join(lessonsDir, file);
        console.log(`\n[${i + 1}/${nce4Files.length}] 处理 ${file}...`);

        try {
            await processLesson(filePath);
        } catch (error) {
            console.error(`  ✗ 处理失败:`, error);
        }
    }

    console.log('\n✓ 所有课程处理完成！');
}

main().catch(console.error);
