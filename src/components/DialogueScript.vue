<script setup lang="ts">
import { ref } from 'vue';
import type { Segment } from '../types/lesson';
import SentenceAnalysis from './SentenceAnalysis.vue';

/**
 * DialogueScript 组件
 * 显示对话脚本，支持播放控制、翻译切换和语法分析
 * @author xiaobin
 */

const props = defineProps<{
  segments: Segment[];
  activeSegmentId: string | null;
  playMode: 'continuous' | 'single' | 'repeat';
  playbackRate: number;
  showTranslation: boolean;
  playbackRates: number[];
}>();

const emit = defineEmits([
  'update:playMode', 
  'update:playbackRate', 
  'update:showTranslation', 
  'segmentClick'
]);


const activeAnalysisSegment = ref<Segment | null>(null);

const toggleAnalysis = (segment: Segment, event: Event) => {
  event.stopPropagation();
  activeAnalysisSegment.value = segment;
};

const closeAnalysis = () => {
    activeAnalysisSegment.value = null;
};

const scrollToActive = (id: string) => {
  const el = document.getElementById(`segment-${id}`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};

defineExpose({
  scrollToActive
});
</script>

<template>
  <div class="lg:col-span-7">
    <!-- Section Title & Controls -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-gray-100 to-gray-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-gray-600">
            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
          </svg>
        </div>
        <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide whitespace-nowrap">Dialogue Script</h2>      
      </div>
      
      <div class="flex items-center gap-3">
        <!-- Play Mode Toggle -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <button 
            @click="emit('update:playMode', 'continuous')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'continuous' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            连读
          </button>
          <button 
            @click="emit('update:playMode', 'single')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'single' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            点读
          </button>
          <button 
            @click="emit('update:playMode', 'repeat')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'repeat' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            循环
          </button>
        </div>

        <!-- Speed Selector -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <select 
            :value="playbackRate"
            @change="(e) => emit('update:playbackRate', parseFloat((e.target as HTMLSelectElement).value))"
            class="appearance-none bg-transparent px-2.5 py-1 text-[10px] font-bold text-gray-500 hover:text-blue-600 transition-all cursor-pointer outline-none"
          >
            <option v-for="rate in playbackRates" :key="rate" :value="rate">
              {{ rate === 1.0 ? '1.0x' : rate + 'x' }}
            </option>
          </select>
        </div>

        <!-- Language Toggle -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <button 
            @click="emit('update:showTranslation', false)"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="!showTranslation ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            EN
          </button>
          <button 
            @click="emit('update:showTranslation', true)"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="showTranslation ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            EN+CN
          </button>
        </div>
      </div>
    </div>

    <!-- Script Cards -->
    <div class="max-h-[620px] overflow-y-auto pr-4 -mr-4 space-y-2.5">
      <div 
        v-for="s in segments" 
        :key="s.id"
        :id="`segment-${s.id}`"
        class="script-card group relative cursor-pointer"
        @click="emit('segmentClick', s)"
      >
        <div 
          class="relative p-3.5 rounded-xl transition-all duration-300 border flex items-start gap-3"
          :class="[
            activeSegmentId === s.id 
              ? 'bg-white shadow-xl shadow-blue-500/5 border-blue-100 scale-[1.01]' 
              : 'bg-white/50 border-transparent hover:bg-white hover:shadow-lg hover:border-gray-100'
          ]"
        >
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p 
                class="text-sm leading-relaxed transition-colors duration-300"
                :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-600'"
              >
                {{ s.text }}
              </p>
              <p 
                v-if="showTranslation" 
                class="text-[11px] mt-1 text-gray-400 font-medium leading-relaxed animate-fade-in"
              >
                {{ s.translation }}
              </p>
            </div>
            
            <!-- Analysis Trigger (Magic Wand) -->
            <!-- Now always visible on hover, even if analysis is missing (will show coming soon) -->
            <button 
              @click="toggleAnalysis(s, $event)"
              class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-purple-50 group/ai"
              :class="[activeAnalysisSegment?.id === s.id ? 'bg-purple-100 text-purple-600 shadow-sm ring-1 ring-purple-200' : 'text-slate-300 opacity-0 group-hover:opacity-100 group-hover:text-purple-400']"
              title="魔法分析"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 transition-transform group-hover/ai:rotate-12">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
              </svg>
            </button>

            <!-- Play Indicator -->
            <div 
              v-if="s.startTime !== undefined"
              class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center transition-all duration-300"
              :class="activeSegmentId === s.id ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-400 opacity-0 group-hover:opacity-100'"
            >
              <svg v-if="activeSegmentId !== s.id" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
              <div v-else class="flex gap-0.5 items-end h-3">
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.2s_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.4s_infinite]"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <SentenceAnalysis 
        :visible="!!activeAnalysisSegment"
        :segment="activeAnalysisSegment"
        @close="closeAnalysis"
    />
</template>

<style scoped>
.script-card {
  -webkit-tap-highlight-color: transparent;
}
@keyframes eq {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
