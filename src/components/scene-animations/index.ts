import type { Component } from 'vue';
import PoliteNoteAnimation from './PoliteNoteAnimation.vue';

/** 课程 JSON 里 segment.animation 的名字 → 动画组件 */
export const sceneAnimations: Record<string, Component> = {
  'nce2-l16-polite-note': PoliteNoteAnimation,
};
