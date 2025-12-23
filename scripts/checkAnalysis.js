import fs from 'fs';
import path from 'path';

const lessonsDir = './src/data/lessons';
const files = fs.readdirSync(lessonsDir)
    .filter(f => f.startsWith('nce1-l') && f.endsWith('.json'))
    .sort((a, b) => {
        const numA = parseInt(a.match(/-l(\d+)/)[1]);
        const numB = parseInt(b.match(/-l(\d+)/)[1]);
        return numA - numB;
    });

const results = [];

files.forEach(file => {
    const filePath = path.join(lessonsDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    let totalWordsInText = 0;
    let totalAnalyzedWords = 0;

    data.segments.forEach(segment => {
        if (segment.text && !segment.id.startsWith('intro')) {
            const wordsInText = segment.text.replace(/['",.!?]/g, '').trim().split(/\s+/).filter(w => w.length > 0).length;
            totalWordsInText += wordsInText;

            if (segment.analysis && segment.analysis.words) {
                totalAnalyzedWords += segment.analysis.words.length;
            }
        }
    });

    const wordRatio = totalWordsInText > 0 ? totalAnalyzedWords / totalWordsInText : 0;
    const lessonNum = parseInt(file.match(/-l(\d+)/)[1]);

    if (wordRatio < 0.9 && lessonNum <= 131) {
        results.push({
            file,
            lessonNum,
            wordRatio: wordRatio.toFixed(2)
        });
    }
});

console.log(JSON.stringify(results, null, 2));
