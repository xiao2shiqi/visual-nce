<script setup lang="ts">
import { ref, onMounted } from 'vue';

/**
 * 主题切换：浅色 / 深色 / 跟随系统
 * 与 xiao27-hub、tube-shadowing 共用同一个 localStorage 键
 */
type Theme = 'light' | 'dark' | 'system';

const STORAGE_KEY = 'xiao27-theme';
const theme = ref<Theme>('system');

const apply = (t: Theme) => {
  const root = document.documentElement;
  if (t === 'system') {
    root.removeAttribute('data-theme');
  } else {
    root.setAttribute('data-theme', t);
  }
  try {
    localStorage.setItem(STORAGE_KEY, t);
  } catch { /* 隐私模式写不进去，忽略 */ }
};

const pick = (t: Theme) => {
  theme.value = t;
  apply(t);
};

onMounted(() => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'light' || saved === 'dark' || saved === 'system') theme.value = saved;
  } catch { /* 读不到按跟随系统处理 */ }
});

const options: { value: Theme; label: string; path: string }[] = [
  { value: 'light', label: '浅色', path: 'M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z' },
  { value: 'dark', label: '深色', path: 'M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z' },
  { value: 'system', label: '跟随系统', path: 'M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25' },
];
</script>

<template>
  <div class="flex items-center gap-0.5 p-0.5 rounded-md border border-line" role="radiogroup" aria-label="主题">
    <button
      v-for="o in options"
      :key="o.value"
      role="radio"
      :aria-checked="theme === o.value"
      :title="o.label"
      @click="pick(o.value)"
      class="p-1.5 rounded transition-colors cursor-pointer"
      :class="theme === o.value ? 'bg-hovered text-ink' : 'text-ink-mute hover:text-ink-soft'"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-3.5 h-3.5">
        <path stroke-linecap="round" stroke-linejoin="round" :d="o.path" />
      </svg>
    </button>
  </div>
</template>
