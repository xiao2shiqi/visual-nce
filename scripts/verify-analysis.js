/**
 * Verify sentence analysis completeness for NCE lessons
 * This script compares each sentence's text with its analysis.words
 * and reports any missing or incomplete analysis
 * @author xiaobin
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const lessonsDir = path.join(__dirname, '../src/data/lessons');

// Simple word tokenizer - splits by spaces and removes punctuation
const tokenize = (text) => {
    return text
        .replace(/[.,!?;:'"()\[\]{}]/g, '') // Remove punctuation
        .split(/\s+/)
        .filter(w => w.length > 0)
        .map(w => w.toLowerCase());
};

// Get lesson files to check (default: NCE2)
const prefix = process.argv[2] || 'nce2';
const files = fs.readdirSync(lessonsDir)
    .filter(f => f.startsWith(`${prefix}-l`) && f.endsWith('.json'))
    .sort((a, b) => {
        const numA = parseInt(a.match(/l(\d+)/)?.[1] || '0');
        const numB = parseInt(b.match(/l(\d+)/)?.[1] || '0');
        return numA - numB;
    });

console.log(`\n📚 Checking ${files.length} ${prefix.toUpperCase()} lessons for analysis completeness...\n`);
console.log('='.repeat(80));

let totalSegments = 0;
let emptyAnalysis = 0;
let incompleteAnalysis = 0;
let completeAnalysis = 0;

const issues = [];

files.forEach(filename => {
    const filePath = path.join(lessonsDir, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const lesson = JSON.parse(content);

    if (!lesson.segments) return;

    const segmentIssues = [];

    lesson.segments.forEach(segment => {
        if (!segment.text) return;
        totalSegments++;

        const textWords = tokenize(segment.text);
        const analysisWords = segment.analysis?.words || [];
        const analysisWordList = analysisWords.map(w => w.word?.toLowerCase());

        if (analysisWords.length === 0) {
            emptyAnalysis++;
            segmentIssues.push({
                id: segment.id,
                text: segment.text,
                status: '❌ EMPTY',
                textCount: textWords.length,
                analysisCount: 0,
                missing: textWords
            });
        } else if (analysisWords.length < textWords.length * 0.5) {
            // Less than 50% coverage is considered incomplete
            incompleteAnalysis++;
            const missing = textWords.filter(w => !analysisWordList.includes(w));
            segmentIssues.push({
                id: segment.id,
                text: segment.text,
                status: '⚠️ INCOMPLETE',
                textCount: textWords.length,
                analysisCount: analysisWords.length,
                coverage: Math.round(analysisWords.length / textWords.length * 100) + '%',
                missing: missing.slice(0, 5) // Only show first 5 missing
            });
        } else {
            completeAnalysis++;
        }
    });

    if (segmentIssues.length > 0) {
        issues.push({ filename, issues: segmentIssues });
    }
});

// Output detailed issues
if (issues.length > 0) {
    console.log('\n🔴 ISSUES FOUND:\n');

    issues.forEach(({ filename, issues: segIssues }) => {
        console.log(`\n📄 ${filename}`);
        console.log('-'.repeat(60));

        segIssues.forEach(issue => {
            console.log(`  ${issue.status} [${issue.id}]`);
            console.log(`    Text: "${issue.text.substring(0, 60)}${issue.text.length > 60 ? '...' : ''}"`);
            console.log(`    Words in text: ${issue.textCount}, In analysis: ${issue.analysisCount}${issue.coverage ? ` (${issue.coverage})` : ''}`);
            if (issue.missing.length > 0) {
                console.log(`    Missing: ${issue.missing.join(', ')}${issue.missing.length >= 5 ? '...' : ''}`);
            }
        });
    });
}

// Summary
console.log('\n' + '='.repeat(80));
console.log('\n📊 SUMMARY:\n');
console.log(`  Total segments checked: ${totalSegments}`);
console.log(`  ✅ Complete analysis:   ${completeAnalysis} (${Math.round(completeAnalysis / totalSegments * 100)}%)`);
console.log(`  ⚠️ Incomplete analysis: ${incompleteAnalysis} (${Math.round(incompleteAnalysis / totalSegments * 100)}%)`);
console.log(`  ❌ Empty analysis:      ${emptyAnalysis} (${Math.round(emptyAnalysis / totalSegments * 100)}%)`);
console.log('\n' + '='.repeat(80));

if (issues.length === 0) {
    console.log('\n🎉 All segments have complete analysis!\n');
} else {
    console.log(`\n⚠️ Found issues in ${issues.length} lesson file(s). Please review above.\n`);
}
