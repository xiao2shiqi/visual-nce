<script setup lang="ts">
import { ref } from 'vue';
import AudioPlayer from './AudioPlayer.vue';
import LessonDownloadButton from './LessonDownloadButton.vue';
import type { VideoSegment } from '../utils/videoExporter';

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
  loop?: boolean;
  segments?: VideoSegment[];
}>();

const emit = defineEmits(['timeupdate', 'ended']);
const audioPlayerRef = ref<any>(null);

const localCurrentTime = ref(0);
const localDuration = ref(0);
const localIsPlaying = ref(false);

const handleTimeUpdate = (t: number) => {
  localCurrentTime.value = t;
  emit('timeupdate', t);
};

const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const handleSeek = (event: MouseEvent) => {
  if (!localDuration.value) return;
  const bar = event.currentTarget as HTMLElement;
  const rect = bar.getBoundingClientRect();
  const fraction = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
  const audio = audioPlayerRef.value?.innerAudio;
  if (audio) audio.currentTime = fraction * localDuration.value;
};

defineExpose({ audioPlayerRef });
</script>

<template>
  <div class="col-span-5 sticky top-24 self-start">

    <!-- Movie Player Container -->
    <div class="relative group rounded-3xl overflow-hidden shadow-2xl shadow-slate-300/40 ring-1 ring-black/5 bg-black aspect-[4/3] cursor-pointer">

      <!-- Scene Image -->
      <img
        :src="currentImage"
        :alt="lessonTitle"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.02]"
      />

      <!-- Center Play/Pause Button -->
      <button
        @click="audioPlayerRef?.togglePlay()"
        class="absolute inset-0 flex items-center justify-center transition-opacity duration-300"
        :class="localIsPlaying ? 'opacity-0 hover:opacity-100' : 'opacity-100'"
      >
        <div class="w-16 h-16 rounded-full bg-black/50 backdrop-blur-sm border border-white/30 flex items-center justify-center text-white hover:scale-110 transition-transform duration-200 shadow-2xl">
          <svg v-if="!localIsPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7 ml-0.5">
            <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7">
            <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
          </svg>
        </div>
      </button>

      <!-- Bottom Controls Overlay -->
      <div
        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent pt-14 px-4 pb-4 transition-opacity duration-300 pointer-events-none"
        :class="localIsPlaying ? 'opacity-0 group-hover:opacity-100' : 'opacity-100'"
      >
        <!-- Progress Bar -->
        <div
          class="h-1 bg-white/30 rounded-full cursor-pointer mb-3 hover:h-1.5 transition-all duration-150 pointer-events-auto"
          @click="handleSeek"
        >
          <div
            class="h-full bg-white rounded-full pointer-events-none transition-all duration-150"
            :style="{ width: localDuration > 0 ? (localCurrentTime / localDuration * 100) + '%' : '0%' }"
          ></div>
        </div>

        <!-- Controls Row -->
        <div class="flex items-center justify-between text-white pointer-events-auto">
          <div class="flex items-center gap-3">
            <button @click="audioPlayerRef?.togglePlay()" class="hover:opacity-70 transition-opacity active:scale-95">
              <svg v-if="!localIsPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
              </svg>
            </button>
            <span class="text-xs font-mono text-white/80">
              {{ formatTime(localCurrentTime) }} / {{ formatTime(localDuration) }}
            </span>
          </div>

          <div class="flex items-center gap-2">
            <div v-if="localIsPlaying" class="flex gap-0.5 h-3 items-end">
              <div class="w-0.5 bg-amber-500 animate-[waveBar_0.8s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-amber-500 animate-[waveBar_1.2s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-amber-500 animate-[waveBar_1s_ease-in-out_infinite]"></div>
            </div>
            <span class="text-[10px] font-bold text-white/50 uppercase tracking-wider">{{ lessonTitle }}</span>
          </div>
        </div>
      </div>

      <!-- Segment Progress Line (top of bottom bar) -->
      <div class="absolute bottom-0 left-0 right-0 h-0.5 pointer-events-none">
        <div
          class="h-full bg-gradient-to-r from-amber-600 to-indigo-500 transition-all duration-300"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>

      <!-- Top Badge -->
      <div class="absolute top-4 left-4 pointer-events-none">
        <div class="backdrop-blur-xl bg-black/40 px-3 py-1.5 rounded-full flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></div>
          <span class="text-[10px] font-bold text-white uppercase tracking-wider">{{ lessonTitle }}</span>
        </div>
      </div>

      <!-- Download Icon Overlay -->
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <LessonDownloadButton
          v-if="segments"
          v-show="!localIsPlaying"
          :title="lessonTitle"
          :audio-src="audioSrc"
          :segments="segments"
          :icon-only="true"
        />
      </transition>

      <!-- Glow Effect -->
      <div class="absolute -inset-4 bg-gradient-to-r from-amber-600/20 via-indigo-500/20 to-violet-500/20 rounded-[2rem] blur-2xl opacity-0 group-hover:opacity-60 transition-opacity duration-700 -z-10 pointer-events-none"></div>

      <!-- Headless Audio Player (logic only) -->
      <AudioPlayer
        :hidden="true"
        ref="audioPlayerRef"
        :src="audioSrc"
        :playback-rate="playbackRate"
        :loop="loop"
        @timeupdate="handleTimeUpdate"
        @play="localIsPlaying = true"
        @pause="localIsPlaying = false"
        @durationchange="(d) => localDuration = d"
        @ended="emit('ended')"
      />
    </div>

    <!-- Keyboard Shortcuts -->
    <div class="mt-6 pt-5 border-t border-slate-200/60">
      <div class="flex items-center gap-2 mb-3">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-slate-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 7.5 2.25 12l4.5 4.5m10.5-9 4.5 4.5-4.5 4.5m-9-1.5 3-6h3l3 6" />
        </svg>
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Keyboard Shortcuts</span>
      </div>

      <div class="grid grid-cols-2 gap-y-3 gap-x-6">
        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-amber-700 transition-colors">Play / Pause</span>
          <kbd class="min-w-[40px] text-center px-1.5 py-1 rounded-md border border-slate-200 bg-white text-[9px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-amber-200 group-hover:text-amber-700 transition-all">Space</kbd>
        </div>

        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-amber-700 transition-colors">Repeat Line</span>
          <kbd class="min-w-[40px] text-center px-1.5 py-1 rounded-md border border-slate-200 bg-white text-[9px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-amber-200 group-hover:text-amber-700 transition-all">R</kbd>
        </div>

        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-amber-700 transition-colors">Prev / Next</span>
          <div class="flex gap-1">
            <kbd class="min-w-[20px] text-center px-1 py-1 rounded-md border border-slate-200 bg-white text-[10px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-amber-200 group-hover:text-amber-700 transition-all">←</kbd>
            <kbd class="min-w-[20px] text-center px-1 py-1 rounded-md border border-slate-200 bg-white text-[10px] font-black text-slate-600 shadow-sm ring-1 ring-slate-900/5 group-hover:border-amber-200 group-hover:text-amber-700 transition-all">→</kbd>
          </div>
        </div>

        <div class="flex items-center justify-between group">
          <span class="text-[10px] font-bold text-slate-500 group-hover:text-amber-700 transition-colors">Sentence Analysis</span>
          <div class="flex items-center gap-1.5">
            <span class="text-[9px] font-medium text-slate-400">Click</span>
            <div class="w-5 h-5 rounded-md border border-slate-200 bg-white flex items-center justify-center text-slate-400 group-hover:border-amber-200 group-hover:text-amber-700 transition-all">
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
@keyframes waveBar {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1.2); }
}
</style>
