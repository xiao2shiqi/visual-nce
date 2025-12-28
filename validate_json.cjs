const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'src/data/lessons');

const files = fs.readdirSync(dir);

files.forEach(file => {
    if (!file.endsWith('.json')) return;
    const filePath = path.join(dir, file);
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        JSON.parse(content);
    } catch (e) {
        console.error(`Error in ${file}: ${e.message}`);
    }
});
