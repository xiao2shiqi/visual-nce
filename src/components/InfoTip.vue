<script setup lang="ts">
defineProps<{
  text: string;
}>();
</script>

<template>
  <!-- 点击/悬停都能弹出说明；点别处或再点一次关闭（靠失焦） -->
  <button
    type="button"
    tabindex="0"
    class="group/tip relative inline-flex shrink-0 text-slate-300 hover:text-slate-500 focus:text-slate-500 focus:outline-none cursor-help"
    @click.stop
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3 h-3">
      <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
    </svg>
    <span
      class="hidden group-hover/tip:block group-focus/tip:block absolute z-20 top-full left-1/2 -translate-x-1/2 mt-2 w-64 rounded-xl bg-slate-800 text-white text-[11px] leading-relaxed font-normal normal-case tracking-normal text-left px-3 py-2 shadow-xl"
    >
      {{ text }}
    </span>
  </button>
</template>
