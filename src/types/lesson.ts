/**
 * 课程数据类型定义
 * @author xiaobin
 * 
 * 所有课程 JSON 文件都应遵循此数据结构
 */

// 词汇详情
export interface Word {
    word: string;       // 单词
    pos: string;        // 词性（如：n., v., adj.）
    meaning: string;    // 中文释义
}


// 句子分析
export interface Analysis {
    words: Word[];           // 词汇详解
}

// 对话片段
export interface Segment {
    id: string;              // 唯一标识符
    role: string;            // 说话人角色（如：Man, Woman, Narrator）
    text: string;            // 英文文本
    translation: string;     // 中文翻译
    startTime: number;       // 开始时间（秒）
    endTime: number;         // 结束时间（秒）
    image?: string;          // 可选：此片段对应的场景图片
    analysis?: Analysis;     // 可选：语法和词汇分析
}

// 课程数据
export interface LessonData {
    id: string;              // 课程 ID（如：l1, l127）
    title: string;           // 课程标题
    audio: string;           // 音频文件路径
    image?: string;          // 可选：课程封面图片（如果指定，将覆盖 segment 的图片）
    segments: Segment[];     // 对话片段列表
}

// 课程列表项（用于首页展示）
export interface LessonListItem {
    id: string;
    title: string;
    description?: string;
    thumbnail?: string;
    duration?: string;
    difficulty?: 'beginner' | 'intermediate' | 'advanced';
}
