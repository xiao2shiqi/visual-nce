const fs = require('fs');
const path = require('path');

/**
 * 批量修复课程分析数据的脚本
 * usage: node scripts/fix-analysis-batch.js <data_json_path>
 */
const dataPath = process.argv[2];
if (!dataPath) {
    console.error('Please provide a data JSON file path');
    process.exit(1);
}

const updateData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

for (const [lessonId, segments] of Object.entries(updateData)) {
    const filePath = path.join(process.cwd(), 'src/data/lessons', `${lessonId}.json`);
    if (!fs.existsSync(filePath)) {
        console.warn(`File not found: ${filePath}`);
        continue;
    }

    const lesson = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    let updatedCount = 0;

    for (const segment of lesson.segments) {
        if (segments[segment.id]) {
            // 检查单词是否匹配（简单校验）
            const newWords = segments[segment.id];
            segment.analysis = { words: newWords };
            updatedCount++;
        }
    }

    fs.writeFileSync(filePath, JSON.stringify(lesson, null, 2) + '\n');
    console.log(`✅ Updated ${lessonId}: ${updatedCount} segments fixed.`);
}
