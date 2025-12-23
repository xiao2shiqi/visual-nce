/**
 * LRC 文件解析器 - 自动扫描并生成 NCE1-4 所有课程 JSON
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

// 仅 NCE1 的特定课程享有吉卜力风格插画，其他全部为 Coming Soon
const GHIBLI_LESSONS_NCE1 = new Set(['nce1-l1', 'nce1-l127', 'nce1-l129', 'nce1-l131', 'nce1-l133', 'nce1-l135', 'nce1-l137', 'nce1-l139']);
const COMING_SOON_IMAGE = '/images/coming-soon.png';

const BOOKS = [
    {
        id: 'nce1',
        title: 'First Things First',
        subtitle: 'NCE 1',
        description: '英语初阶 - 建立英语基础的关键。',
        level: 'Beginner',
        color: 'from-blue-500 to-cyan-500',
        folder: 'nce1',
        filenamePattern: /^(\d+)&(\d+)－(.+)\.lrc$/
    },
    {
        id: 'nce2',
        title: 'Practice and Progress',
        subtitle: 'NCE 2',
        description: '实践与进步 - 掌握语法规则，提高口语能力。',
        level: 'Pre-Intermediate',
        color: 'from-green-500 to-emerald-500',
        folder: 'nce2',
        filenamePattern: /^(\d+)－(.+)\.lrc$/
    },
    {
        id: 'nce3',
        title: 'Developing Skills',
        subtitle: 'NCE 3',
        description: '培养技能 - 强化阅读与写作，深入语言精髓。',
        level: 'Intermediate',
        color: 'from-yellow-500 to-orange-500',
        folder: 'nce3',
        filenamePattern: /^(\d+)－(.+)\.lrc$/
    },
    {
        id: 'nce4',
        title: 'Fluency in English',
        subtitle: 'NCE 4',
        description: '流利英语 - 体会英语文化，达到流利水准。',
        level: 'Advanced',
        color: 'from-purple-500 to-indigo-500',
        folder: 'nce4',
        filenamePattern: /^(\d+)－(.+)\.lrc$/
    }
];

function parseTime(timeStr: string): number {
    const match = timeStr.match(/\[(\d+):(\d+)\.(\d+)\]/);
    if (!match) return 0;
    const minutes = parseInt(match[1], 10);
    const seconds = parseInt(match[2], 10);
    const centiseconds = parseInt(match[3], 10);
    return minutes * 60 + seconds + centiseconds / 100;
}

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

function parseLrc(lrcContent: string, bookId: string, lessonNum: string, title: string, audioFileName: string): LessonData {
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

    const lessonId = `${bookId}-l${lessonNum}`;

    // 图片逻辑: NCE1 的特定课程保留 Ghibli 图, 其他所有书的所有课都用 Coming Soon
    let image = COMING_SOON_IMAGE;
    if (GHIBLI_LESSONS_NCE1.has(lessonId)) {
        image = `/images/${bookId}/l${lessonNum}/scene1.png`;
    }

    return {
        id: lessonId,
        title: `Lesson ${lessonNum}: ${title}`,
        audio: `/audio/${bookId}/${audioFileName}`,
        image,
        segments
    };
}

async function main() {
    const outputDir = path.join(process.cwd(), 'src/data/lessons');
    const curriculumPath = path.join(process.cwd(), 'src/data/curriculum.json');
    let curriculum = JSON.parse(fs.readFileSync(curriculumPath, 'utf-8'));

    // 确保 outputDir 存在
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    for (const book of BOOKS) {
        console.log(`正在处理: ${book.title} (${book.id})...`);
        const audioDir = path.join(process.cwd(), `public/audio/${book.folder}`);

        if (!fs.existsSync(audioDir)) {
            console.warn(`警告: 音频目录不存在 ${audioDir}`);
            continue;
        }

        const files = fs.readdirSync(audioDir);
        const lrcFiles = files.filter(f => f.endsWith('.lrc'));
        const bookLessons: any[] = [];

        for (const lrcFile of lrcFiles) {
            const match = lrcFile.match(book.filenamePattern);
            if (!match) continue;

            const lessonNum = parseInt(match[1], 10).toString();
            // NCE1 的正则 match[3] 是 title, NCE2-4 match[2] 是 title
            const title = book.id === 'nce1' ? match[3].trim() : match[2].trim();

            const lessonId = `${book.id}-l${lessonNum}`;
            const audioFileName = lrcFile.replace('.lrc', '.mp3');

            // 生成 JSON 文件路径
            const outputPath = path.join(outputDir, `${lessonId}.json`);

            // 如果文件不存在，生成它
            if (!fs.existsSync(outputPath)) {
                const lrcPath = path.join(audioDir, lrcFile);
                const lrcContent = fs.readFileSync(lrcPath, 'utf-8');
                const lessonData = parseLrc(lrcContent, book.id, lessonNum, title, audioFileName);
                fs.writeFileSync(outputPath, JSON.stringify(lessonData, null, 2), 'utf-8');
                console.log(`+ 生成: ${lessonId}`);
            } else {
                // 如果文件存在，我们要确保图片和ID是最新的 (迁移逻辑)
                // 读取现有文件
                const existingData = JSON.parse(fs.readFileSync(outputPath, 'utf-8'));
                let changed = false;

                // 检查 ID 是否匹配新格式 (之前已手动批量 rename 且 sed replace, 但这里做双重保险)
                if (existingData.id !== lessonId) {
                    existingData.id = lessonId;
                    changed = true;
                }

                // 检查图片逻辑
                let targetImage = COMING_SOON_IMAGE;
                if (GHIBLI_LESSONS_NCE1.has(lessonId)) {
                    targetImage = `/images/${book.id}/l${lessonNum}/scene1.png`;
                }

                if (existingData.image !== targetImage) {
                    existingData.image = targetImage;
                    // 同时更新 segments 中的图片
                    if (existingData.segments) {
                        existingData.segments.forEach((seg: any) => {
                            if (seg.image) seg.image = targetImage;
                        });
                    }
                    changed = true;
                }

                if (changed) {
                    fs.writeFileSync(outputPath, JSON.stringify(existingData, null, 2), 'utf-8');
                    console.log(`~ 更新: ${lessonId}`);
                }
            }

            // 收集 curriculum 数据
            // 为了避免覆盖手工修改的 curriculum 图片 (如果有), 再次检查
            let displayImage = COMING_SOON_IMAGE;
            if (GHIBLI_LESSONS_NCE1.has(lessonId)) {
                displayImage = `/images/${book.id}/l${lessonNum}/scene1.png`;
            }

            bookLessons.push({
                id: lessonId,
                title: `Lesson ${lessonNum}`,
                subtitle: title,
                image: displayImage
            });
        }

        // 排序 lessons
        bookLessons.sort((a, b) => {
            const numA = parseInt(a.id.split('-l')[1]);
            const numB = parseInt(b.id.split('-l')[1]);
            return numA - numB;
        });

        // 更新 curriculum.json 中的 book entry
        let bookEntry = curriculum.books.find((b: any) => b.id === book.id);
        if (!bookEntry) {
            bookEntry = {
                id: book.id,
                title: book.title,
                subtitle: book.subtitle,
                description: book.description,
                level: book.level,
                color: book.color,
                lessons: []
            };
            curriculum.books.push(bookEntry);
        } else {
            // Update existing book metadata
            bookEntry.title = book.title;
            bookEntry.subtitle = book.subtitle;
            bookEntry.description = book.description;
            bookEntry.level = book.level;
            bookEntry.color = book.color;
        }

        // 更新 lessons 列表
        // 保留原 curriculum 中可能存在的自定义数据? 
        // 简单策略: 全量替换为 file system 扫描结果，因为我们希望 filesystem 是 source of truth
        // 但对于 NCE1，我们之前已经 carefully curated.
        // 如果我们完全替换，就会覆盖掉 NCE1 之前保留的 image 路径吗？
        // 我们的 displayImage 逻辑已经涵盖了 Ghibli 白名单。
        // 所以全量替换是安全的，且能保证顺序和完整性。
        bookEntry.lessons = bookLessons;
    }

    fs.writeFileSync(curriculumPath, JSON.stringify(curriculum, null, 4), 'utf-8');
    console.log('Curriculum 更新完成！');
}

main().catch(console.error);
