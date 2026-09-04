<script setup lang="ts">
/**
 * xiao27 站点品牌标 —— 三个站共用同一个壳
 * 黑底方块 + 站点图标 + 站名 + 返回 hub
 */
withDefaults(defineProps<{ name?: string }>(), { name: 'Visual NCE' });
</script>

<template>
  <a href="https://xiao27.com" class="group flex items-center gap-2.5 shrink-0" title="返回 phoenix hub">
    <img src="/favicon.svg" alt="" width="32" height="32" class="w-8 h-8 rounded-md" />
    <span class="flex items-center gap-1.5 whitespace-nowrap">
      <span class="text-sm font-semibold tracking-wide text-ink">{{ name }}</span>
      <span class="text-xs font-mono text-ink-mute group-hover:text-ink-soft transition-colors">/ xiao27</span>
    </span>
  </a>
</template>
