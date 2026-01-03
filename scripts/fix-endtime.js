/**
 * Fix endTime for NCE1 and NCE2 lessons
 * Rule: endTime = next segment's startTime - 0.5s
 * For last segment: endTime = startTime + 5s (reasonable estimate)
 * @author xiaobin
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SINGLE_CUTOFF = 0.5; // seconds before next segment starts
const LAST_SEGMENT_DURATION = 5.0; // estimated duration for last segment

const lessonsDir = path.join(__dirname, '../src/data/lessons');

// Get all NCE1 and NCE2 lesson files
const files = fs.readdirSync(lessonsDir).filter(f =>
    (f.startsWith('nce1-l') || f.startsWith('nce2-l')) && f.endsWith('.json')
);

console.log(`Found ${files.length} lesson files to process...`);

let totalFixed = 0;

files.forEach(filename => {
    const filePath = path.join(lessonsDir, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const lesson = JSON.parse(content);

    if (!lesson.segments || lesson.segments.length === 0) {
        console.log(`[SKIP] ${filename}: No segments found`);
        return;
    }

    let fixedCount = 0;
    const segments = lesson.segments;

    for (let i = 0; i < segments.length; i++) {
        const current = segments[i];
        const next = segments[i + 1];

        // Skip segments without startTime
        if (current.startTime === undefined) continue;

        let newEndTime;

        if (next && next.startTime !== undefined) {
            // Normal case: endTime = next startTime - SINGLE_CUTOFF
            newEndTime = Math.round((next.startTime - SINGLE_CUTOFF) * 100) / 100;
        } else {
            // Last segment: endTime = startTime + LAST_SEGMENT_DURATION
            newEndTime = Math.round((current.startTime + LAST_SEGMENT_DURATION) * 100) / 100;
        }

        // Only update if different
        if (current.endTime !== newEndTime) {
            current.endTime = newEndTime;
            fixedCount++;
        }
    }

    if (fixedCount > 0) {
        // Write back with proper formatting
        fs.writeFileSync(filePath, JSON.stringify(lesson, null, 2) + '\n');
        console.log(`[FIXED] ${filename}: Updated ${fixedCount} segments`);
        totalFixed += fixedCount;
    } else {
        console.log(`[OK] ${filename}: No changes needed`);
    }
});

console.log(`\nDone! Total segments fixed: ${totalFixed}`);
