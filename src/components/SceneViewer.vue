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
  <div>

    <!-- Movie Player Container -->
    <div class="relative group rounded-3xl overflow-hidden shadow-2xl shadow-zinc-300/40 ring-1 ring-black/5 bg-black aspect-[4/3] cursor-pointer">

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
              <div class="w-0.5 bg-zinc-900 animate-[waveBar_0.8s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-zinc-900 animate-[waveBar_1.2s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-zinc-900 animate-[waveBar_1s_ease-in-out_infinite]"></div>
            </div>
            <span class="text-[10px] font-bold text-white/50 uppercase tracking-wider">{{ lessonTitle }}</span>
          </div>
        </div>
      </div>

      <!-- Segment Progress Line (top of bottom bar) -->
      <div class="absolute bottom-0 left-0 right-0 h-0.5 pointer-events-none">
        <div
          class="h-full bg-gradient-to-r from-zinc-900 to-indigo-500 transition-all duration-300"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>

      <!-- Top Badge -->
      <div class="absolute top-4 left-4 pointer-events-none">
        <div class="backdrop-blur-xl bg-black/40 px-3 py-1.5 rounded-full flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-zinc-900 animate-pulse"></div>
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
      <div class="absolute -inset-4 bg-gradient-to-r from-zinc-900/20 via-indigo-500/20 to-violet-500/20 rounded-[2rem] blur-2xl opacity-0 group-hover:opacity-60 transition-opacity duration-700 -z-10 pointer-events-none"></div>

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

    <!-- Keyboard Shortcuts: 压缩成一行小字，把左栏空间让给语法地图 -->
    <div class="mt-5 pt-4 border-t border-zinc-200/60 flex items-center flex-wrap gap-x-4 gap-y-1.5 text-[10px] font-bold text-zinc-400">
      <span class="flex items-center gap-1.5">
        <kbd class="px-1.5 py-0.5 rounded border border-zinc-200 bg-white text-[9px] font-black text-zinc-500 shadow-sm">Space</kbd>
        播放/暂停
      </span>
      <span class="flex items-center gap-1.5">
        <kbd class="px-1 py-0.5 rounded border border-zinc-200 bg-white text-[9px] font-black text-zinc-500 shadow-sm">←</kbd>
        <kbd class="px-1 py-0.5 rounded border border-zinc-200 bg-white text-[9px] font-black text-zinc-500 shadow-sm">→</kbd>
        上/下句
      </span>
      <span class="flex items-center gap-1.5">
        <kbd class="px-1.5 py-0.5 rounded border border-zinc-200 bg-white text-[9px] font-black text-zinc-500 shadow-sm">R</kbd>
        重复本句
      </span>
    </div>

  </div>
</template>

<style scoped>
@keyframes waveBar {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1.2); }
}
</style>
