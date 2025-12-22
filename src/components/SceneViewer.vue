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
