# 🎨 Visual NCE: When New Concept English Meets Studio Ghibli

<p align="center">
  <a href="README_zh.md">中文</a> | English
</p>

<p align="center">
  <a href="https://github.com/xiao2shiqi/visual-nce/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://vuejs.org/"><img src="https://img.shields.io/badge/Vue-3.x-42b883?logo=vue.js" alt="Vue 3"></a>
  <a href="https://vitejs.dev/"><img src="https://img.shields.io/badge/Vite-6.x-646cff?logo=vite" alt="Vite"></a>
  <a href="https://github.com/xiao2shiqi/visual-nce/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/xiao2shiqi/visual-nce/main/public/images/nce1/l121/scene1.png" width="600" alt="Visual NCE Splash" style="border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
</p>

<p align="center">
  <strong>Reimagining a 30-year-old English classic with AI visuals and modern web technology.</strong>
</p>

---

## 🚀 Live Demo

**[Start your healing learning journey](https://nce.xiao27.com/)**

---

## 🖼️ Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/xiao2shiqi/visual-nce/main/public/home_page.jpg" width="800" alt="Visual NCE Features Preview">
</p>

---

## 💭 Why This Project?

Many people have bittersweet memories of studying with *New Concept English*: memorizing entire passages, rewinding cassette tapes, staring at dull black-and-white illustrations...

**Visual NCE** started from a simple idea:
What if a classic textbook from 30 years ago could wear the warm, hand-painted coat of Miyazaki — paired with millisecond-precise modern interactivity? Could learning become something you actually look forward to?

We're not just *translating* language anymore. We're *immersing* you in the scene.

---

## ✨ Key Features

### 🎨 Ghibli-Style Reimagination
Using AI, every illustration across all 4 books has been redrawn in **Studio Ghibli** style. Each lesson cover tells a story — your study list feels like a curated film collection.

### 🎧 Smooth Audio-Visual Sync
- **Scrolling highlight**: Text lights up word-by-word as the audio plays — perfectly in sync.
- **Click to seek**: Tap any sentence to jump directly to that point in the audio.
- **Variable speed**: 0.5x – 2.0x playback speed to train your ear at any pace.

### 🧠 Deep Semantic Analysis
No blind spots left behind. Built-in **sentence grammar breakdowns** and **vocabulary analysis** — click any sentence to reveal a detailed card that helps you truly understand every idiomatic phrase.

### 📱 Polished Across All Devices
Built with a Glassmorphism design language. Whether on a 5K display or a mobile screen, the experience is smooth and immersive.

---

## 🛠️ Tech Stack

- **Framework**: [Vue 3](https://vuejs.org/) (Composition API) — reactive interactivity at its core.
- **Build**: [Vite](https://vitejs.dev/) — lightning-fast dev and production builds.
- **Language**: [TypeScript](https://www.typescriptlang.org/) — keeping the project solid and maintainable.
- **Styling**: [TailwindCSS](https://tailwindcss.com/) — atomic CSS for pixel-perfect design.
- **AI**: Stable Diffusion / Gemini — painting new life into old lessons.

---

## 🗂️ Project Structure

```
visual-nce/
├── public/
│   ├── audios/             # NCE audio files (mp3/lrc)
│   └── images/             # Ghibli-style illustrations per lesson
│       ├── nce1/
│       ├── nce2/
│       ├── nce3/
│       └── nce4/
├── src/
│   ├── components/         # Vue components (AudioPlayer, SceneViewer, etc.)
│   ├── data/
│   │   ├── curriculum.json # Course index & metadata
│   │   └── lessons/        # Per-lesson JSON (text, timestamps, analysis)
│   ├── views/              # Page-level views (HomeView, LessonView)
│   ├── types/              # TypeScript type definitions
│   └── utils/
└── scripts/
    ├── generate_images.py  # AI image generation pipeline (Gemini)
    ├── nce1/               # Storyboard scripts for NCE Book 1
    └── nce2/               # Storyboard scripts for NCE Book 2
```

---

## 🗺️ Roadmap

| Book | Lessons | Audio Sync | Sentence Analysis | Ghibli Illustrations |
|------|---------|------------|-------------------|----------------------|
| NCE Book 1 | 72 lessons | ✅ | ✅ | ✅ |
| NCE Book 2 | 96 lessons | ✅ | ✅ | ✅ |
| NCE Book 3 | 60 lessons | ✅ | ✅ | 🚧 In Progress |
| NCE Book 4 | 48 lessons | ✅ | ✅ | 🚧 In Progress |

**Coming next:**
- [ ] Mobile app (PWA)
- [ ] User progress tracking
- [ ] Spaced repetition for vocabulary

---

## 🛠️ Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/xiao2shiqi/visual-nce.git
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start dev server**
   ```bash
   npm run dev
   ```

---

## 🤝 Contributing

With 276 lessons worth of content, things slip through the cracks. If you spot:
- Translation errors
- Incorrect sentence breaks
- Typos or bugs

Feel free to open an **Issue** or submit a **Pull Request**. Let's build this love letter to English learners together.

---

## 🙏 Acknowledgements

- **[New Concept English](https://en.wikipedia.org/wiki/New_Concept_English)** — The timeless textbook by L.G. Alexander that inspired this project. All original content belongs to its respective rights holders and is used here solely for non-commercial educational purposes.
- **[Studio Ghibli](https://www.ghibli.jp/)** — The visual style of this project is inspired by the warmth and artistry of Studio Ghibli films. No official affiliation.
- **[Vue](https://vuejs.org/) / [Vite](https://vitejs.dev/) / [TailwindCSS](https://tailwindcss.com/)** — The modern web foundation that makes this all run smoothly.

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License**.

**🚨 Disclaimer**: Content in this project is derived from *New Concept English* for personal learning, research, and communication purposes only. **Commercial use is strictly prohibited.** If this project infringes on your rights, please contact the author for removal.

---

> **"Learning can be healing."**
> —— Author: **xiaobin** | GitHub: [@xiao2shiqi](https://github.com/xiao2shiqi)
