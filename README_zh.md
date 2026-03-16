# 🎨 Visual NCE: 当《新概念英语》遇上吉卜力

<p align="center">
  中文 | <a href="README.md">English</a>
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
  <strong>融合 AI 视觉与现代 Web 技术，重构跨越 30 年的英语经典。</strong>
</p>

---

## 🚀 在线体验

**[点击开启治愈学习之旅](https://nce.xiao27.com/)**

---

## 🖼️ 产品预览

<p align="center">
  <img src="https://raw.githubusercontent.com/xiao2shiqi/visual-nce/main/public/home_page.jpg" width="800" alt="Visual NCE 功能预览">
</p>

---

## 💭 为什么做这个项目？

很多人的童年记忆里，都有一段被《新概念英语》支配的恐惧："背诵全文"、"磁带复读"、"枯燥的黑白插图"……

**Visual NCE** 的想法很简单：
如果 30 年前的经典教材，能穿上"宫崎骏"的温暖外衣，配上毫秒级的现代交互，学习会不会变成一种享受？

我们不再是**"翻译"**语言，而是在**"浸入"**场景。

---

## ✨ 核心卖点 (Magic Factors)

### 🎨 治愈系重制计划
我们利用 AI 技术，将全书四册课程的插图全部重绘为 **Studio Ghibli（吉卜力）** 风格。每一张封面图都是一个故事，让你的学习列表像精选电影集一样赏心悦目。

### 🎧 丝滑的音画同步
- **滚动高亮**：课文朗读到哪，文字高亮就跟到哪，视听完全一致。
- **点击跳转**：想听哪句点哪句，彻底告别手动拉进度条。
- **无级变速**：支持 0.5x - 2.0x 语速调节，磨耳朵神器。

### 🧠 深度语义解析
不留任何知识盲区！内置**逐句语法拆解**和**核心词汇分析**。点击句子即可弹出详细卡片，助你真正吃透每一句地道英文。

### 📱 极致终端适配
采用玻璃拟态（Glassmorphism）设计语言，无论在 5K 显示器还是在手机屏幕上，都能提供丝滑且沉浸的交互体验。

---

## 🛠️ 背后的一砖一瓦 (Tech Stack)

- **框架**: [Vue 3](https://vuejs.org/) (Composition API) - 响应式交互的核心。
- **构建**: [Vite](https://vitejs.dev/) - 极速的开发与生产构建。
- **逻辑**: [TypeScript](https://www.typescriptlang.org/) - 确保项目稳如泰山。
- **视觉**: [TailwindCSS](https://tailwindcss.com/) - 原子化样式，像素级还原设计。
- **AI 赋能**: Stable Diffusion / Gemini - 为老教材绘制新皮肤。

---

## 🗂️ 项目结构

```
visual-nce/
├── public/
│   ├── audios/             # NCE 音频文件 (mp3/lrc)
│   └── images/             # 吉卜力风格插图（按课程分目录）
│       ├── nce1/
│       ├── nce2/
│       ├── nce3/
│       └── nce4/
├── src/
│   ├── components/         # Vue 组件（AudioPlayer、SceneViewer 等）
│   ├── data/
│   │   ├── curriculum.json # 课程索引与元数据
│   │   └── lessons/        # 每课 JSON（文本、时间戳、语法解析）
│   ├── views/              # 页面级视图（首页、课程页）
│   ├── types/              # TypeScript 类型定义
│   └── utils/
└── scripts/
    ├── generate_images.py  # AI 图像生成流水线（Gemini）
    ├── nce1/               # 新概念第一册分镜脚本
    └── nce2/               # 新概念第二册分镜脚本
```

---

## 🗺️ 路线图 (Roadmap)

| 教材 | 课程数 | 音画同步 | 语法解析 | 吉卜力插图 |
|------|--------|----------|----------|------------|
| 新概念第一册 | 72 课 | ✅ | ✅ | ✅ |
| 新概念第二册 | 96 课 | ✅ | ✅ | ✅ |
| 新概念第三册 | 60 课 | ✅ | ✅ | 🚧 进行中 |
| 新概念第四册 | 48 课 | ✅ | ✅ | 🚧 进行中 |

**近期计划：**
- [ ] PWA 移动端离线支持
- [ ] 学习进度记录
- [ ] 词汇间隔重复复习

---

## 🛠️ 本地开发 (Getting Started)

1. **克隆项目**
   ```bash
   git clone https://github.com/xiao2shiqi/visual-nce.git
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **开启传送门**
   ```bash
   npm run dev
   ```

---

## 🤝 参与项目

由于数据量巨大（276 课！），如果你在学习过程中发现了：
- 翻译错误
- 断句不准
- 拼写 Bug

欢迎直接开 **Issue** 或 **Pull Request**。让我们一起完成这份给所有英语学习者的"情怀大礼"。

---

## 🙏 致谢

- **[《新概念英语》](https://en.wikipedia.org/wiki/New_Concept_English)** — L.G. Alexander 编著的经典教材，本项目内容源于此，版权归原著作权人所有，仅供非商业教育用途。
- **[Studio Ghibli（吉卜力工作室）](https://www.ghibli.jp/)** — 本项目视觉风格受吉卜力电影启发，与官方无任何关联。
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** — 驱动本项目 AI 图像生成流水线。
- **[Vue](https://vuejs.org/) / [Vite](https://vitejs.dev/) / [TailwindCSS](https://tailwindcss.com/)** — 支撑整个项目流畅运行的现代 Web 基础设施。

---

## 📄 许可证 & 声明

本项目采用 **MIT License**。

**🚨 声明**：本项目内容素材取材于《新概念英语》，仅供个人学习、研究与交流使用，**严禁用于任何商业用途**。如果本项目侵犯了您的权益，请联系作者删除。

---

> **"学习，也可以是治愈人心的。"**
> —— Author: **xiaobin** | GitHub: [@xiao2shiqi](https://github.com/xiao2shiqi)
