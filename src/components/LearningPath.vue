<script setup lang="ts">
import InfoTip from './InfoTip.vue';

defineProps<{
  completed: boolean;
}>();

const emit = defineEmits<{
  (e: 'open-grammar'): void;
  (e: 'open-challenge'): void;
  (e: 'toggle-complete'): void;
}>();
</script>

<template>
  <!-- 学习动线：告诉学习者进入课程后按什么顺序学 -->
  <section class="mb-8 animate-fade-in">
    <div class="rounded-2xl bg-white/60 backdrop-blur-sm border border-slate-200/70 px-5 py-4">
      <div class="flex items-center gap-1.5 mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-amber-500">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z" />
        </svg>
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">本课学习动线</span>
        <InfoTip text="回译挑战是选做的练习，没拼对的句子点「回去听这句」回到第 2 步复听。这课学到什么程度算完，你自己说了算——觉得学完了，点最后那个「标记学完」，点错了再点一次就能取消。" />
      </div>

      <!-- 步骤条 -->
      <div class="flex flex-wrap items-center gap-x-1.5 gap-y-2">
        <!-- 1 语法预习（可点击） -->
        <button
          @click="emit('open-grammar')"
          class="group flex items-center gap-2 pl-1.5 pr-3 py-1.5 rounded-xl border border-amber-200/80 bg-amber-50/70 hover:bg-amber-100 hover:border-amber-400 transition-all"
          title="点击打开语法预习"
        >
          <span class="w-5 h-5 rounded-lg bg-amber-500 text-white text-[11px] font-black flex items-center justify-center">1</span>
          <span class="text-xs font-bold text-amber-800">语法预习</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-2.5 h-2.5 text-amber-500 opacity-0 group-hover:opacity-100 transition-opacity">
            <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
          </svg>
        </button>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-300 shrink-0">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>

        <!-- 2 听课文 -->
        <div class="flex items-center gap-2 pl-1.5 pr-3 py-1.5 rounded-xl border border-slate-200 bg-white/70">
          <span class="w-5 h-5 rounded-lg bg-slate-400 text-white text-[11px] font-black flex items-center justify-center">2</span>
          <span class="text-xs font-bold text-slate-600">听课文</span>
        </div>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-300 shrink-0">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>

        <!-- 3 循环跟读 -->
        <div class="flex items-center gap-2 pl-1.5 pr-3 py-1.5 rounded-xl border border-slate-200 bg-white/70">
          <span class="w-5 h-5 rounded-lg bg-slate-400 text-white text-[11px] font-black flex items-center justify-center">3</span>
          <span class="text-xs font-bold text-slate-600">循环 · 跟读</span>
        </div>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-300 shrink-0">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>

        <!-- 4 回译练习（选做，可点击） -->
        <button
          @click="emit('open-challenge')"
          class="group flex items-center gap-2 pl-1.5 pr-3 py-1.5 rounded-xl border border-emerald-200/80 bg-emerald-50/70 hover:bg-emerald-100 hover:border-emerald-400 transition-all"
          title="点击打开回译挑战（选做）"
        >
          <span class="w-5 h-5 rounded-lg bg-emerald-500 text-white text-[11px] font-black flex items-center justify-center">4</span>
          <span class="text-xs font-bold text-emerald-800">回译练习</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-2.5 h-2.5 text-emerald-500 opacity-0 group-hover:opacity-100 transition-opacity">
            <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
          </svg>
        </button>

        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-300 shrink-0">
          <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>

        <!-- 终点：由学习者自己打勾，可反悔 -->
        <button
          @click="emit('toggle-complete')"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-colors"
          :class="completed
            ? 'border-emerald-300 bg-emerald-50 text-emerald-600 hover:border-emerald-400'
            : 'border-dashed border-slate-300 bg-transparent text-slate-400 hover:border-emerald-400 hover:text-emerald-600'"
          :title="completed ? '再点一次可取消标记' : '觉得这课学完了就点一下'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-3 h-3">
            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          <span class="text-xs font-bold">{{ completed ? '已学完' : '标记学完' }}</span>
        </button>
      </div>
    </div>
  </section>
</template>
