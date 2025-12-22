<script setup lang="ts">
import { ref } from 'vue';
import type { Segment } from '../types/lesson';

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

const expandedSegmentId = ref<string | null>(null);

const toggleAnalysis = (id: string, event: Event) => {
  event.stopPropagation();
  expandedSegmentId.value = expandedSegmentId.value === id ? null : id;
};

// 使用 Web Speech API 朗读单词
const speakWord = (word: string) => {
  // 取消正在进行的语音
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(word);
  utterance.lang = 'en-US'; // 设置为美式英语
  utterance.rate = 0.9; // 稍微慢一点，便于学习
  utterance.pitch = 1;
  
  // 尝试选择英语语音
  const voices = window.speechSynthesis.getVoices();
  const englishVoice = voices.find(v => v.lang.startsWith('en-') && v.name.includes('Female')) 
    || voices.find(v => v.lang.startsWith('en-'));
  if (englishVoice) {
    utterance.voice = englishVoice;
  }
  
  window.speechSynthesis.speak(utterance);
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
          class="relative p-3.5 rounded-xl transition-all duration-300 border"
          :class="[
            activeSegmentId === s.id 
              ? 'bg-white shadow-xl shadow-blue-500/5 border-blue-100 scale-[1.01]' 
              : 'bg-white/50 border-transparent hover:bg-white hover:shadow-lg hover:border-gray-100'
          ]"
        >
          <div class="flex items-start gap-3">
            <!-- Avatar -->
            <div 
              class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-bold shadow-sm transition-transform duration-300 group-hover:scale-110"
              :class="[
                s.role === 'Man' ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' : 
                s.role === 'Woman' ? 'bg-gradient-to-br from-indigo-500 to-violet-600 text-white' :
                'bg-gradient-to-br from-slate-500 to-slate-600 text-white'
              ]"
            >
              {{ s.role[0] }}
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-baseline gap-2">
                <span class="flex-shrink-0 text-[10px] font-black text-gray-400 uppercase tracking-wide">{{ s.role }}:</span>
                <p 
                  class="text-sm leading-relaxed transition-colors duration-300"
                  :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-600'"
                >
                  {{ s.text }}
                </p>
              </div>
              <p 
                v-if="showTranslation" 
                class="text-[11px] mt-1 ml-0 text-gray-400 font-medium leading-relaxed animate-fade-in"
              >
                {{ s.translation }}
              </p>


            </div>
            
            <!-- Analysis Trigger (Magic Wand) -->
            <button 
              v-if="s.analysis"
              @click="toggleAnalysis(s.id, $event)"
              class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-blue-50 group/ai"
              :class="[expandedSegmentId === s.id ? 'bg-blue-50 text-blue-500' : 'text-slate-300 opacity-0 group-hover:opacity-100']"
              title="Show Analysis"
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

    <!-- Analysis Modal with Glassmorphism -->
    <Teleport to="body">
      <Transition name="modal">
        <div 
          v-if="expandedSegmentId && segments.find(s => s.id === expandedSegmentId)?.analysis"
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
          @click="expandedSegmentId = null"
        >
          <!-- Backdrop with blur -->
          <div class="absolute inset-0 bg-slate-900/30 backdrop-blur-md"></div>
          
          <!-- Modal Content -->
          <div 
            class="relative max-w-2xl w-full max-h-[80vh] overflow-y-auto bg-white/90 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 p-6"
            @click.stop
          >
            <!-- Close Button -->
            <button 
              @click="expandedSegmentId = null"
              class="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100/80 hover:bg-slate-200/80 flex items-center justify-center transition-all duration-200 group"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 text-slate-600 group-hover:text-slate-900">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>

            <!-- Modal Header -->
            <div class="mb-6 pr-8">
              <div class="flex items-center gap-2 mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-blue-500">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                </svg>
                <h3 class="text-lg font-black text-slate-900">句子分析</h3>
              </div>
              <div class="p-4 rounded-xl bg-gradient-to-r from-slate-50 to-slate-100/50 border border-slate-200/30">
                <p class="text-base text-slate-800 font-semibold leading-relaxed">
                  {{ segments.find(s => s.id === expandedSegmentId)?.text }}
                </p>
                <p class="text-sm text-slate-500 mt-2 font-medium">
                  {{ segments.find(s => s.id === expandedSegmentId)?.translation }}
                </p>
              </div>
            </div>

            <!-- Analysis Content -->
            <div v-if="segments.find(s => s.id === expandedSegmentId)?.analysis" class="space-y-6">
              <!-- Grammar Structure -->
              <div class="space-y-3">
                <h5 class="text-xs font-black text-blue-600 uppercase tracking-widest flex items-center gap-2">
                  <div class="w-1 h-4 bg-blue-500 rounded-full"></div>
                  语法结构
                </h5>
                <div class="flex flex-wrap gap-2">
                  <div 
                    v-for="(part, i) in segments.find(s => s.id === expandedSegmentId)?.analysis?.grammar" 
                    :key="i"
                    class="px-3 py-2 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100/50 border border-blue-200/50 flex flex-col shadow-sm"
                  >
                    <span class="text-sm font-bold text-slate-800">{{ part.text }}</span>
                    <span class="text-[9px] font-black text-blue-500 uppercase tracking-wider mt-0.5">{{ part.label }}</span>
                  </div>
                </div>
              </div>

              <!-- Word Details -->
              <div class="space-y-3">
                <h5 class="text-xs font-black text-indigo-600 uppercase tracking-widest flex items-center gap-2">
                  <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
                  词汇详解
                  <span class="text-[9px] font-medium text-slate-400 normal-case tracking-normal ml-1">点击发音</span>
                </h5>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <button 
                    v-for="(word, i) in segments.find(s => s.id === expandedSegmentId)?.analysis?.words" 
                    :key="i"
                    @click="speakWord(word.word)"
                    class="p-3 rounded-xl bg-gradient-to-br from-slate-50 to-slate-100/50 border border-slate-200/50 group/word transition-all hover:shadow-lg hover:border-indigo-200 hover:from-indigo-50 hover:to-indigo-100/30 text-left cursor-pointer"
                  >
                    <div class="flex items-center gap-2 mb-1">
                      <span class="text-sm font-black text-slate-900 group-hover/word:text-indigo-700">{{ word.word }}</span>
                      <span class="text-[9px] font-bold text-slate-400 italic">{{ word.pos }}</span>
                      <!-- Speaker Icon -->
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5 text-indigo-400 opacity-0 group-hover/word:opacity-100 transition-opacity">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
                      </svg>
                    </div>
                    <p class="text-xs text-slate-600 font-medium">{{ word.meaning }}</p>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
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

/* Modal Transition */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from > div:first-child,
.modal-leave-to > div:first-child {
  backdrop-filter: blur(0px);
}

.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.95);
  opacity: 0;
}

.animate-pulse-slow {
  animation: pulse-slow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes pulse-slow {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(0.98); }
}
</style>
