<script setup lang="ts">

import { ref } from 'vue';
import type { Segment } from '../types/lesson';

const props = defineProps<{
  visible: boolean;
  segment: Segment | null;
}>();

const emit = defineEmits(['close']);

// Track which word was just copied
const copiedWordIndex = ref<number | null>(null);

// Copy word to clipboard
const copyWord = (word: string, index: number, event: Event) => {
  event.stopPropagation(); // Prevent triggering speakWord
  navigator.clipboard.writeText(word).then(() => {
    copiedWordIndex.value = index;
    setTimeout(() => {
      if (copiedWordIndex.value === index) {
        copiedWordIndex.value = null;
      }
    }, 2000);
  });
};

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
        <!-- Backdrop with magical blur -->
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-md"></div>
        
        <!-- Modal Content -->
        <div 
          class="relative max-w-2xl w-full max-h-[80vh] overflow-y-auto bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 p-6 ring-1 ring-white/50"
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
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 via-purple-500 to-indigo-500 flex items-center justify-center text-white shadow-lg shadow-purple-500/30 ring-2 ring-purple-200/50">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                  </svg>
              </div>
              <h3 class="text-xl font-black bg-clip-text text-transparent bg-gradient-to-r from-violet-600 to-indigo-600">句子魔法分析</h3>
            </div>
            <div class="p-5 rounded-2xl bg-gradient-to-br from-violet-50/50 via-purple-50/50 to-indigo-50/50 border border-violet-100/50 shadow-sm relative overflow-hidden group">
              <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-purple-200/20 to-indigo-200/20 rounded-full blur-2xl -mr-16 -mt-16 pointer-events-none"></div>
              <p class="text-lg text-slate-800 font-semibold leading-relaxed relative z-10">
                {{ segment.text }}
              </p>
              <p class="text-sm text-slate-500 mt-2 font-medium relative z-10">
                {{ segment.translation }}
              </p>
            </div>
          </div>

          <!-- Analysis Content -->
          <div v-if="segment.analysis" class="space-y-6 animate-fade-in">
            <!-- Word Details -->
            <div class="space-y-3" v-if="segment.analysis.words && segment.analysis.words.length">
              <h5 class="text-xs font-black text-violet-600 uppercase tracking-widest flex items-center gap-2 mb-4">
                <div class="w-1.5 h-1.5 rounded-full bg-violet-500 shadow-[0_0_8px_rgba(139,92,246,0.6)]"></div>
                <div class="w-1 h-4 bg-gradient-to-b from-violet-500 to-indigo-500 rounded-full"></div>
                词汇详解
                <span class="text-[9px] font-medium text-slate-400 normal-case tracking-normal ml-1">点击发音</span>
              </h5>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div 
                  v-for="(word, i) in segment.analysis.words" 
                  :key="i"
                  class="p-4 rounded-xl bg-white border border-slate-200/60 shadow-sm group/word transition-all hover:shadow-lg hover:shadow-purple-500/10 hover:border-violet-200 hover:-translate-y-0.5 text-left relative overflow-hidden"
                >
                  <div class="absolute inset-0 bg-gradient-to-br from-violet-50/50 via-transparent to-transparent opacity-0 group-hover/word:opacity-100 transition-opacity"></div>
                  <div class="relative z-10">
                    <div class="flex items-center gap-2 mb-1.5">
                      <!-- Clickable word for pronunciation -->
                      <button 
                        @click="speakWord(word.word)"
                        class="text-base font-black text-slate-800 hover:text-violet-600 transition-colors cursor-pointer"
                      >
                        {{ word.word }}
                      </button>
                      <span class="px-1.5 py-0.5 rounded-md bg-slate-100 text-[10px] font-bold text-slate-500 italic group-hover/word:bg-violet-100 group-hover/word:text-violet-600 transition-colors">{{ word.pos }}</span>
                      
                      <div class="flex items-center gap-1 ml-auto">
                        <!-- Speaker Icon -->
                        <button
                          @click="speakWord(word.word)"
                          class="w-7 h-7 rounded-lg flex items-center justify-center text-violet-400 hover:bg-violet-50 hover:text-violet-600 opacity-0 group-hover/word:opacity-100 transition-all"
                          title="点击发音"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.01 9.01 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
                          </svg>
                        </button>
                        <!-- Dictionary Lookup Button (Eudic) -->
                        <a
                          :href="`eudic://dict/${encodeURIComponent(word.word)}`"
                          @click.stop
                          class="w-7 h-7 rounded-lg flex items-center justify-center text-amber-500 hover:bg-amber-50 hover:text-amber-600 opacity-0 group-hover/word:opacity-100 transition-all"
                          title="在欧路词典中查询"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                          </svg>
                        </a>
                        <!-- Copy Button -->
                        <button
                          @click="copyWord(word.word, i, $event)"
                          class="w-7 h-7 rounded-lg flex items-center justify-center transition-all"
                          :class="copiedWordIndex === i ? 'bg-green-50 text-green-500' : 'text-slate-400 hover:bg-slate-100 hover:text-slate-600 opacity-0 group-hover/word:opacity-100'"
                          title="复制单词"
                        >
                          <svg v-if="copiedWordIndex !== i" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                          </svg>
                          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                          </svg>
                        </button>
                      </div>
                    </div>
                    <p class="text-sm text-slate-600 font-medium leading-relaxed">{{ word.meaning }}</p>
                  </div>
                </div>
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
