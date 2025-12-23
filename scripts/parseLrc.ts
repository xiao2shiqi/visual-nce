/**
 * LRC 文件解析器 - 将 LRC 文件转换为课程 JSON 格式
 * 用法: npx ts-node scripts/parseLrc.ts
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
}

interface LessonData {
    id: string;
    title: string;
    audio: string;
    image: string;
    segments: Segment[];
}

// 解析 LRC 时间戳 [mm:ss.xx] -> 秒数
function parseTime(timeStr: string): number {
    const match = timeStr.match(/\[(\d+):(\d+)\.(\d+)\]/);
    if (!match) return 0;
    const minutes = parseInt(match[1], 10);
    const seconds = parseInt(match[2], 10);
    const centiseconds = parseInt(match[3], 10);
    return minutes * 60 + seconds + centiseconds / 100;
}

// 判断角色
function detectRole(text: string, prevRole: string): string {
    // 叙述性文本通常包含这些关键词
    const narrativeKeywords = ['Lesson', 'Listen to', 'answer this question', 'Why', 'What', 'How', 'Which', 'Who'];

    for (const kw of narrativeKeywords) {
        if (text.startsWith(kw) || text.includes('Listen to the tape')) {
            return 'Narrator';
        }
    }

    // 根据引号和上下文判断
    if (text.includes('"') || text.includes("'")) {
        // 可能是引用，保持 Narrator
        return 'Narrator';
    }

    // 简单的对话交替
    if (prevRole === 'Narrator') return 'Man';
    if (prevRole === 'Man') return 'Woman';
    if (prevRole === 'Woman') return 'Man';

    return 'Narrator';
}

// 解析 LRC 文件
function parseLrc(lrcContent: string, lessonNum: string, title: string): LessonData {
    const lines = lrcContent.split('\n').filter(line => line.trim());
    const segments: Segment[] = [];

    let prevRole = 'Narrator';
    let segmentIndex = 0;

    const contentLines = lines.filter(line => line.match(/^\[\d+:\d+\.\d+\]/));

    for (let i = 0; i < contentLines.length; i++) {
        const line = contentLines[i];
        const timeMatch = line.match(/^\[(\d+:\d+\.\d+)\]/);
        if (!timeMatch) continue;

        const startTime = parseTime(`[${timeMatch[1]}]`);
        const content = line.replace(/^\[\d+:\d+\.\d+\]/, '').trim();

        // 分离英文和中文
        const parts = content.split('|');
        const text = parts[0]?.trim() || content;
        const translation = parts[1]?.trim() || '';

        // 计算结束时间（使用下一行的开始时间，或者当前时间 +5 秒）
        let endTime = startTime + 5;
        if (i + 1 < contentLines.length) {
            const nextTimeMatch = contentLines[i + 1].match(/^\[(\d+:\d+\.\d+)\]/);
            if (nextTimeMatch) {
                endTime = parseTime(`[${nextTimeMatch[1]}]`) - 0.01;
            }
        }

        // 判断角色
        let role = detectRole(text, prevRole);

        // 前几行通常是标题和说明
        if (segmentIndex < 4) {
            role = 'Narrator';
        }

        const segmentId = segmentIndex < 4 ? `intro_${segmentIndex + 1}` : `s${segmentIndex - 3}`;

        segments.push({
            id: segmentId,
            role,
            text,
            translation,
            startTime: Math.round(startTime * 100) / 100,
            endTime: Math.round(endTime * 100) / 100
        });

        prevRole = role;
        segmentIndex++;
    }

    return {
        id: `l${lessonNum}`,
        title: `Lesson ${lessonNum}: ${title}`,
        audio: `/audio/nce1/${lessonNum.padStart(3, '0')}&${(parseInt(lessonNum) + 1).toString().padStart(3, '0')}－${title.replace(/[?!]/g, '')}.mp3`,
        image: `/images/nce1/l${lessonNum}/scene1.png`,
        segments
    };
}

// 主函数
async function main() {
    const audioDir = path.join(process.cwd(), 'public/audio/nce1');
    const outputDir = path.join(process.cwd(), 'src/data/lessons');

    // 课程映射
    const lessons = [
        { num: '3', title: 'Sorry, Sir.' },
        { num: '5', title: 'Nice to Meet You.' },
        { num: '7', title: 'Are You a Teacher' },
        { num: '9', title: 'How Are You Today' },
        { num: '131', title: "Don't be So Sure" },
        { num: '133', title: 'Sensational News' },
        { num: '135', title: 'The Latest Report' },
        { num: '137', title: 'A Pleasant Dream' },
        { num: '139', title: 'Is That You, John' },
        { num: '141', title: "Sally's First Train Ride" },
        { num: '143', title: 'A Walk Through the Woods' },
    ];

    for (const lesson of lessons) {
        // 查找对应的 LRC 文件
        const files = fs.readdirSync(audioDir);
        const searchNum = lesson.num.padStart(3, '0');
        const lrcFile = files.find(f => f.startsWith(searchNum) && f.endsWith('.lrc'));

        if (!lrcFile) {
            console.log(`未找到 Lesson ${lesson.num} 的 LRC 文件`);
            continue;
        }

        const lrcPath = path.join(audioDir, lrcFile);
        const lrcContent = fs.readFileSync(lrcPath, 'utf-8');

        const lessonData = parseLrc(lrcContent, lesson.num, lesson.title);

        // 写入 JSON 文件
        const outputPath = path.join(outputDir, `l${lesson.num}.json`);
        fs.writeFileSync(outputPath, JSON.stringify(lessonData, null, 2), 'utf-8');

        console.log(`已生成: l${lesson.num}.json`);
    }
}

main().catch(console.error);
