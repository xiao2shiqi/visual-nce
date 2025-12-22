<script setup lang="ts">
import { ref } from 'vue';
import AudioPlayer from './AudioPlayer.vue';

/**
 * @author xiaobin
 */
defineProps<{
  currentImage: string;
  activeSegmentId: string | null;
  audioSrc: string;
  playbackRate: number;
  progress: number;
  segmentsCount: number;
  lessonTitle: string;
}>();

const emit = defineEmits(['timeupdate']);
const audioPlayerRef = ref<any>(null);

defineExpose({
  audioPlayerRef
});
</script>

<template>
  <div class="lg:col-span-5 lg:sticky lg:top-24 lg:self-start">
    <div class="relative group">
      <!-- Image Container -->
      <div class="aspect-[4/3] bg-gradient-to-br from-slate-100 to-slate-50 rounded-3xl overflow-hidden shadow-2xl shadow-slate-200/50 ring-1 ring-black/5">
        <Transition name="fade" mode="out-in">
          <img 
            :key="currentImage"
            :src="currentImage" 
            :alt="lessonTitle"
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.02]"
          />
        </Transition>
        
        <!-- Scene Badge -->
        <div class="absolute top-4 left-4">
          <div class="backdrop-blur-xl bg-black/40 px-3 py-1.5 rounded-full flex items-center gap-2">
            <div class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></div>
            <span class="text-[10px] font-bold text-white uppercase tracking-wider">
              {{ lessonTitle }}
            </span>
          </div>
        </div>
        
        <!-- Progress Indicator -->
        <div class="absolute bottom-0 left-0 right-0 h-1 bg-black/10">
          <div 
            class="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>
      
      <!-- Glow Effect -->
      <div class="absolute -inset-4 bg-gradient-to-r from-blue-500/20 via-indigo-500/20 to-violet-500/20 rounded-[2rem] blur-2xl opacity-0 group-hover:opacity-60 transition-opacity duration-700 -z-10"></div>
    </div>
    
    <!-- Scene Info -->
    <div class="mt-6 flex items-center justify-between px-1">
      <div class="flex items-center gap-3">
        <div class="flex -space-x-1">
          <div class="w-6 h-6 rounded-full bg-blue-500 ring-2 ring-white flex items-center justify-center text-[8px] font-bold text-white">M</div>
          <div class="w-6 h-6 rounded-full bg-indigo-500 ring-2 ring-white flex items-center justify-center text-[8px] font-bold text-white">W</div>
        </div>
        <span class="text-xs text-gray-500 font-medium">2 speakers</span>
      </div>
    </div>

    <!-- Audio Player -->
    <div class="mt-8">
      <AudioPlayer 
        ref="audioPlayerRef"
        :src="audioSrc" 
        :playback-rate="playbackRate"
        @timeupdate="(t) => emit('timeupdate', t)"
      />
    </div>

    <!-- Shortcuts Guide -->
    <div class="mt-8 pt-6 border-t border-slate-200/60">
      <div class="flex items-center gap-2 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 7.5 2.25 12l4.5 4.5m10.5-9 4.5 4.5-4.5 4.5m-9-1.5 3-6h3l3 6" />
        </svg>
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Keyboard Shortcuts</span>
      </div>
      
      <div class="grid grid-cols-2 gap-y-3 gap-x-6">
        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-blue-600 transition-colors">Play / Pause</span>
          <kbd class="min-w-[40px] text-center px-1.5 py-1 rounded-md border border-slate-200 bg-white text-[9px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-blue-200 group-hover:text-blue-600 transition-all">Space</kbd>
        </div>
        
        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-blue-600 transition-colors">Repeat Line</span>
          <kbd class="min-w-[40px] text-center px-1.5 py-1 rounded-md border border-slate-200 bg-white text-[9px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-blue-200 group-hover:text-blue-600 transition-all">R</kbd>
        </div>

        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-blue-600 transition-colors">Prev / Next</span>
          <div class="flex gap-1">
            <kbd class="min-w-[20px] text-center px-1 py-1 rounded-md border border-slate-200 bg-white text-[10px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-blue-200 group-hover:text-blue-600 transition-all">←</kbd>
            <kbd class="min-w-[20px] text-center px-1 py-1 rounded-md border border-slate-200 bg-white text-[10px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-blue-200 group-hover:text-blue-600 transition-all">→</kbd>
          </div>
        </div>

        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-blue-600 transition-colors">Sentence Analysis</span>
          <div class="flex items-center gap-1.5">
            <span class="text-[9px] font-medium text-slate-400">Click</span>
            <div class="w-5 h-5 rounded-md border border-slate-200 bg-white flex items-center justify-center text-slate-400 group-hover:border-blue-200 group-hover:text-blue-600 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3 h-3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
