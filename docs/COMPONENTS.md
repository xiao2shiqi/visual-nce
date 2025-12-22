# Visual NCE 组件架构说明

## 组件概览

本项目采用 Vue 3 + TypeScript 构建，组件设计遵循可复用原则，方便添加新课程。

```
src/
├── components/           # 可复用组件
│   ├── AudioPlayer.vue   # 音频播放器
│   ├── DialogueScript.vue # 对话脚本（含语法分析弹窗）
│   ├── LessonHeader.vue   # 课程头部导航
│   └── SceneViewer.vue    # 场景图片查看器
├── views/
│   └── LessonView.vue     # 课程页面（整合所有组件）
├── types/
│   └── lesson.ts          # TypeScript 类型定义
├── data/
│   ├── lessons/           # 课程数据 JSON 文件
│   │   ├── l1.json
│   │   ├── l127.json
│   │   └── _template.jsonc  # 课程模板
│   └── courses.json       # 课程列表
└── utils/
    └── resolvePath.ts     # 路径解析工具
```

## 组件说明

### 1. AudioPlayer.vue
**功能**: 音频播放控制器
**Props**:
- `src: string` - 音频文件路径
- `playbackRate?: number` - 播放速度

**Events**:
- `@timeupdate(time: number)` - 播放进度更新

**Expose**:
- `playAt(seconds)` - 跳转到指定时间播放
- `pause()` - 暂停播放
- `innerAudio` - 原生 audio 元素引用

---

### 2. DialogueScript.vue
**功能**: 对话脚本展示、播放模式控制、语法分析弹窗
**Props**:
- `segments: Segment[]` - 对话片段列表
- `activeSegmentId: string | null` - 当前播放的片段 ID
- `playMode: 'continuous' | 'single' | 'repeat'` - 播放模式
- `playbackRate: number` - 播放速度
- `showTranslation: boolean` - 是否显示翻译
- `playbackRates: number[]` - 可选播放速度列表

**Events**:
- `@update:playMode` - 播放模式改变
- `@update:playbackRate` - 播放速度改变
- `@update:showTranslation` - 翻译显示状态改变
- `@segment-click(segment)` - 点击某个对话片段

---

### 3. SceneViewer.vue
**功能**: 场景图片展示、进度显示、快捷键说明
**Props**:
- `currentImage: string` - 当前场景图片路径
- `activeSegmentId: string | null` - 当前活跃片段 ID
- `audioSrc: string` - 音频路径
- `playbackRate: number` - 播放速度
- `progress: number` - 播放进度百分比
- `segmentsCount: number` - 总片段数
- `lessonTitle: string` - 课程标题

---

### 4. LessonHeader.vue
**功能**: 课程页面顶部导航栏
**Props**:
- `title: string` - 课程标题
- `subtitle?: string` - 副标题
- `badge?: string` - 徽章文本

**Events**:
- `@back` - 返回按钮点击

---

## 添加新课程步骤

### 1. 准备资源文件
```bash
# 音频文件
public/audio/lX.mp3

# 场景图片
public/images/lX/scene1.png
```

### 2. 创建课程数据
复制模板文件并填写内容：
```bash
cp src/data/lessons/_template.jsonc src/data/lessons/lX.json
```

编辑 `lX.json`，按照格式填写：
- 课程 ID、标题
- 音频和图片路径
- 对话片段（包含时间戳）
- 语法分析（可选）

### 3. 更新课程列表
编辑 `src/data/courses.json`，添加新课程：
```json
{
  "id": "lX",
  "title": "Lesson X: ...",
  "description": "..."
}
```

---

## 数据结构 (TypeScript)

详见 `src/types/lesson.ts`

```typescript
interface Segment {
  id: string;              // 唯一标识符
  role: string;            // 说话人角色
  text: string;            // 英文文本
  translation: string;     // 中文翻译
  startTime: number;       // 开始时间（秒）
  endTime: number;         // 结束时间（秒）
  image?: string;          // 场景图片（可选）
  analysis?: {             // 语法分析（可选）
    grammar: GrammarPart[];
    words: Word[];
  };
}
```

---

## 功能特性

- ✅ 音频同步高亮
- ✅ 三种播放模式（连读/点读/循环）
- ✅ 可调节播放速度
- ✅ 中英文翻译切换
- ✅ 语法分析弹窗（毛玻璃效果）
- ✅ 单词发音（Web Speech API）
- ✅ 键盘快捷键（Space/←/→/R）
- ✅ 自动滚动到活跃片段
