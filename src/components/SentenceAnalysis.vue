<script setup lang="ts">

import type { Segment } from '../types/lesson';

const props = defineProps<{
  visible: boolean;
  segment: Segment | null;
}>();

const emit = defineEmits(['close']);

// 使用 Web Speech API 朗读单词
const speakWord = (word: string) => {
  if (!window.speechSynthesis) return;

  // 确保语音引擎没有暂停
  window.speechSynthesis.resume();
  // 取消正在进行的语音
  window.speechSynthesis.cancel();
  
  const utterance = new SpeechSynthesisUtterance(word);
  utterance.lang = 'en-US'; 
  utterance.rate = 0.8;
  utterance.pitch = 1;
  
  // 更加鲁棒的语音选择
  const selectVoice = () => {
    const voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) return null;
    
    // 优先选择美式英语女声，其次是美式英语，最后是任何英语
    return voices.find(v => v.lang === 'en-US' && v.name.includes('Female')) 
      || voices.find(v => v.lang === 'en-US')
      || voices.find(v => v.lang.startsWith('en-'))
      || voices[0];
  };

  const voice = selectVoice();
  if (voice) {
    utterance.voice = voice;
  } else {
    // 如果还没加载好语音（常见于 Chrome 启动时），监听事件
    window.speechSynthesis.onvoiceschanged = () => {
      const v = selectVoice();
      if (v) utterance.voice = v;
      window.speechSynthesis.speak(utterance);
      window.speechSynthesis.onvoiceschanged = null; // 只执行一次
    };
    const currentVoices = window.speechSynthesis.getVoices();
    if (currentVoices.length > 0) window.speechSynthesis.speak(utterance);
    return;
  }
  
  window.speechSynthesis.speak(utterance);
};
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="visible && segment"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click="emit('close')"
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
            @click="emit('close')"
            class="absolute top-4 right-4 w-8 h-8 rounded-full bg-slate-100/80 hover:bg-slate-200/80 flex items-center justify-center transition-all duration-200 group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 text-slate-600 group-hover:text-slate-900">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Modal Header -->
          <div class="mb-6 pr-8">
            <div class="flex items-center gap-2 mb-3">
              <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-blue-500">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                  </svg>
              </div>
              <h3 class="text-lg font-black text-slate-900">句子分析</h3>
            </div>
            <div class="p-4 rounded-xl bg-gradient-to-r from-slate-50 to-slate-100/50 border border-slate-200/30">
              <p class="text-base text-slate-800 font-semibold leading-relaxed">
                {{ segment.text }}
              </p>
              <p class="text-sm text-slate-500 mt-2 font-medium">
                {{ segment.translation }}
              </p>
            </div>
          </div>

          <!-- Analysis Content -->
          <div v-if="segment.analysis" class="space-y-6 animate-fade-in">
            <!-- Grammar Structure -->
            <div class="space-y-3" v-if="segment.analysis.grammar && segment.analysis.grammar.length">
              <h5 class="text-xs font-black text-blue-600 uppercase tracking-widest flex items-center gap-2">
                <div class="w-1 h-4 bg-blue-500 rounded-full"></div>
                语法结构
              </h5>
              <div class="flex flex-wrap gap-2">
                <div 
                  v-for="(part, i) in segment.analysis.grammar" 
                  :key="i"
                  class="px-3 py-2 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100/50 border border-blue-200/50 flex flex-col shadow-sm"
                >
                  <span class="text-sm font-bold text-slate-800">{{ part.text }}</span>
                  <span class="text-[9px] font-black text-blue-500 uppercase tracking-wider mt-0.5">{{ part.label }}</span>
                </div>
              </div>
            </div>

            <!-- Word Details -->
            <div class="space-y-3" v-if="segment.analysis.words && segment.analysis.words.length">
              <h5 class="text-xs font-black text-indigo-600 uppercase tracking-widest flex items-center gap-2">
                <div class="w-1 h-4 bg-indigo-500 rounded-full"></div>
                词汇详解
                <span class="text-[9px] font-medium text-slate-400 normal-case tracking-normal ml-1">点击发音</span>
              </h5>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button 
                  v-for="(word, i) in segment.analysis.words" 
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

          <!-- Empty State -->
          <div v-else class="py-12 flex flex-col items-center justify-center text-center animate-fade-in">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-slate-400">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.45l.95-.38m-2.45.83c-1.25.54-2.73.68-4.01.26-1.5-.48-2.5-1.96-2.5-3.57 0-1.77 1.4-3.5 3.51-3.5 1.54 0 2.5 1.54 2.5 1.54s.96-1.54 2.5-1.54c2.11 0 3.5 1.73 3.5 3.5 0 1.61-1 .3.09-2.5 3.57-.38.13-1.07.15-2.02.15" />
                  <!-- Adding a sparkle to imply magic/AI coming soon -->
                   <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                </svg>
            </div>
            <h3 class="text-slate-900 font-bold mb-1">AI 正在分析中...</h3>
            <p class="text-slate-500 text-sm">此课程的详细语法解析与词汇数据即将上线，敬请期待！</p>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
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

.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
