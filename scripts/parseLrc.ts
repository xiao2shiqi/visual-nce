/**
 * LRC 文件解析器 - 自动扫描并生成所有 NCE1 课程 JSON
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

const GHIBLI_LESSONS = new Set(['l1', 'l127', 'l129', 'l131', 'l133', 'l135', 'l137', 'l139']);
const COMING_SOON_IMAGE = '/images/coming-soon.png';

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
    const narrativeKeywords = ['Lesson', 'Listen to', 'answer this question', 'Why', 'What', 'How', 'Which', 'Who'];
    for (const kw of narrativeKeywords) {
        if (text.startsWith(kw) || text.includes('Listen to the tape')) {
            return 'Narrator';
        }
    }
    if (prevRole === 'Narrator') return 'Man';
    if (prevRole === 'Man') return 'Woman';
    if (prevRole === 'Woman') return 'Man';
    return 'Narrator';
}

// 解析 LRC 文件
function parseLrc(lrcContent: string, lessonNum: string, title: string, audioFileName: string): LessonData {
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

        const parts = content.split('|');
        const text = parts[0]?.trim() || content;
        const translation = parts[1]?.trim() || '';

        let endTime = startTime + 5;
        if (i + 1 < contentLines.length) {
            const nextTimeMatch = contentLines[i + 1].match(/^\[(\d+:\d+\.\d+)\]/);
            if (nextTimeMatch) {
                endTime = parseTime(`[${nextTimeMatch[1]}]`) - 0.01;
            }
        }

        let role = detectRole(text, prevRole);
        if (segmentIndex < 4) role = 'Narrator';

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

    const lessonId = `l${lessonNum}`;
    const image = GHIBLI_LESSONS.has(lessonId) ? `/images/nce1/${lessonId}/scene1.png` : COMING_SOON_IMAGE;

    return {
        id: lessonId,
        title: `Lesson ${lessonNum}: ${title}`,
        audio: `/audio/nce1/${audioFileName}`,
        image,
        segments
    };
}

async function main() {
    const audioDir = path.join(process.cwd(), 'public/audio/nce1');
    const outputDir = path.join(process.cwd(), 'src/data/lessons');
    const curriculumPath = path.join(process.cwd(), 'src/data/curriculum.json');

    const files = fs.readdirSync(audioDir);
    const lrcFiles = files.filter(f => f.endsWith('.lrc'));

    const curriculum = JSON.parse(fs.readFileSync(curriculumPath, 'utf-8'));
    const book1 = curriculum.books.find((b: any) => b.id === 'nce1');

    const lessonsData: any[] = [];

    for (const lrcFile of lrcFiles) {
        const match = lrcFile.match(/^(\d+)&(\d+)－(.+)\.lrc$/);
        if (!match) continue;

        const lessonNum = parseInt(match[1], 10).toString();
        const title = match[3].trim();
        const lessonId = `l${lessonNum}`;
        const audioFileName = lrcFile.replace('.lrc', '.mp3');

        const outputPath = path.join(outputDir, `${lessonId}.json`);

        let lessonData;
        if (!fs.existsSync(outputPath)) {
            const lrcPath = path.join(audioDir, lrcFile);
            const lrcContent = fs.readFileSync(lrcPath, 'utf-8');
            lessonData = parseLrc(lrcContent, lessonNum, title, audioFileName);
            fs.writeFileSync(outputPath, JSON.stringify(lessonData, null, 2), 'utf-8');
            console.log(`生成新课程: ${lessonId}`);
        } else {
            // 如果已存在，读取并根据是否在吉卜力名单中更新图片
            lessonData = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
            const targetImage = GHIBLI_LESSONS.has(lessonId) ? `/images/nce1/${lessonId}/scene1.png` : COMING_SOON_IMAGE;
            if (lessonData.image !== targetImage) {
                lessonData.image = targetImage;
                // 同时更新 segments 中的图片 (如果有)
                if (lessonData.segments) {
                    lessonData.segments.forEach((seg: any) => {
                        if (seg.image) seg.image = targetImage;
                    });
                }
                fs.writeFileSync(outputPath, JSON.stringify(lessonData, null, 2), 'utf-8');
                console.log(`更新图片路径: ${lessonId}`);
            }
        }

        lessonsData.push({
            id: lessonId,
            title: `Lesson ${lessonNum}`,
            subtitle: title,
            image: lessonData.image
        });
    }

    // 排序
    book1.lessons = lessonsData.sort((a, b) => parseInt(a.id.slice(1)) - parseInt(b.id.slice(1)));

    fs.writeFileSync(curriculumPath, JSON.stringify(curriculum, null, 4), 'utf-8');
    console.log('所有课程同步完成！');
}

main().catch(console.error);
