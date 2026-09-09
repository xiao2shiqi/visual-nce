<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  src: string;
  playbackRate?: number;
  loop?: boolean;
  hidden?: boolean;
}>();

const emit = defineEmits<{
  (e: 'timeupdate', time: number): void;
  (e: 'ended'): void;
  (e: 'play'): void;
  (e: 'pause'): void;
  (e: 'durationchange', duration: number): void;
}>();

const audioRef = ref<HTMLAudioElement | null>(null);
const isPlaying = ref(false);
const isMuted = ref(false);
const currentTime = ref(0);
const duration = ref(0);

watch(() => props.playbackRate, (newRate) => {
  if (audioRef.value && newRate !== undefined) {
    audioRef.value.playbackRate = newRate;
  }
}, { immediate: true });

watch(() => props.src, (newSrc) => {
  if (audioRef.value && newSrc) {
    audioRef.value.pause();
    audioRef.value.load();
    isPlaying.value = false;
    currentTime.value = 0;
  }
});

const togglePlay = () => {
  if (!audioRef.value) return;
  if (!audioRef.value.paused) {
    audioRef.value.pause();
  } else {
    audioRef.value.play().catch((err) => {
      console.warn('Audio play() was interrupted or failed:', err);
    });
  }
};

const onTimeUpdate = () => {
  if (!audioRef.value) return;
  currentTime.value = audioRef.value.currentTime;
  emit('timeupdate', currentTime.value);
};

const onLoadedMetadata = () => {
  if (!audioRef.value) return;
  duration.value = audioRef.value.duration;
  emit('durationchange', duration.value);
  if (props.playbackRate !== undefined) {
    audioRef.value.playbackRate = props.playbackRate;
  }
};

const onPlay = () => { isPlaying.value = true; emit('play'); };
const onPause = () => { isPlaying.value = false; emit('pause'); };

const seek = (event: MouseEvent) => {
  if (!audioRef.value || !duration.value) return;
  const progressBar = event.currentTarget as HTMLElement;
  const rect = progressBar.getBoundingClientRect();
  const clickX = event.clientX - rect.left;
  const width = rect.width;
  const percentage = clickX / width;
  audioRef.value.currentTime = percentage * duration.value;
};

const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const playAt = (seconds: number) => {
  if (!audioRef.value) return;
  try {
    audioRef.value.currentTime = seconds;
  } catch (e) {
    console.warn('Seek error in playAt:', e);
  }
  audioRef.value.play().catch((err) => {
    console.warn('Audio play() in playAt failed:', err);
  });
};

const pause = () => {
  if (!audioRef.value) return;
  audioRef.value.pause();
};

const seekTo = (seconds: number) => {
  if (!audioRef.value || !duration.value) return;
  const clamped = Math.max(0, Math.min(duration.value, seconds));
  audioRef.value.currentTime = clamped;
  currentTime.value = clamped;
  emit('timeupdate', clamped);
};

const onProgressBarKeyDown = (e: KeyboardEvent) => {
  if (!duration.value) return;
  const isLeft = e.key === 'ArrowLeft' || e.code === 'ArrowLeft' || e.key === 'ArrowDown' || e.code === 'ArrowDown';
  const isRight = e.key === 'ArrowRight' || e.code === 'ArrowRight' || e.key === 'ArrowUp' || e.code === 'ArrowUp';
  const isHome = e.key === 'Home' || e.code === 'Home';
  const isEnd = e.key === 'End' || e.code === 'End';
  const isSpace = e.key === ' ' || e.code === 'Space';

  if (isLeft) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(currentTime.value - 3);
  } else if (isRight) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(currentTime.value + 3);
  } else if (isHome) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(0);
  } else if (isEnd) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(duration.value);
  } else if (isSpace) {
    e.preventDefault();
    e.stopPropagation();
    togglePlay();
  }
};

const toggleMute = () => {
  if (!audioRef.value) return;
  audioRef.value.muted = !audioRef.value.muted;
  isMuted.value = audioRef.value.muted;
};

defineExpose({
  playAt,
  pause,
  togglePlay,
  toggleMute,
  isMuted,
  isPlaying,
  currentTime,
  duration,
  formatTime,
  innerAudio: audioRef
});
</script>

<template>
  <!-- Full player UI -->
  <div v-if="!hidden" class="audio-player glass-card p-4 rounded-xl shadow-lg shadow-ink/5 flex items-center gap-4 border border-line">
    <!-- Play/Pause Button -->
    <button
      type="button"
      @click="togglePlay"
      :aria-label="isPlaying ? '暂停' : '播放'"
      class="w-14 h-14 flex-shrink-0 flex items-center justify-center bg-btn text-btn-fg rounded-xl hover:scale-105 active:scale-95 transition-all duration-150 shadow-md group relative overflow-hidden cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ink focus-visible:ring-offset-2 focus-visible:ring-offset-base"
    >
      <div class="absolute inset-0 bg-raised/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
      <span v-if="!isPlaying" class="relative z-10 scale-125">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
        </svg>
      </span>
      <span v-else class="relative z-10 scale-125">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
        </svg>
      </span>
    </button>

    <div class="flex-1 min-w-0 py-1">
      <!-- Info Row -->
      <div class="flex justify-between items-end mb-2.5">
        <div class="flex items-center gap-2">
           <div v-if="isPlaying" class="flex gap-0.5 h-3 items-end">
              <div class="w-0.5 bg-btn animate-[bounce_0.8s_infinite]"></div>
              <div class="w-0.5 bg-btn animate-[bounce_1.2s_infinite]"></div>
              <div class="w-0.5 bg-btn animate-[bounce_1s_infinite]"></div>
           </div>
           <span class="text-[10px] font-black tracking-widest text-ink/60 uppercase">Playback</span>
        </div>
        <div class="flex gap-1.5 text-[10px] font-bold font-mono">
          <span class="text-ink">{{ formatTime(currentTime) }}</span>
          <span class="text-ink-mute">/</span>
          <span class="text-ink-mute">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div
        class="h-2 bg-line-strong/50 rounded-full cursor-pointer relative group transition-all duration-150 hover:h-3 focus-visible:h-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ink focus-visible:ring-offset-2 focus-visible:ring-offset-base before:content-[''] before:absolute before:-top-3.5 before:-bottom-3.5 before:left-0 before:right-0 before:z-10"
        role="slider"
        tabindex="0"
        :aria-valuenow="Math.round(currentTime)"
        :aria-valuemin="0"
        :aria-valuemax="Math.round(duration)"
        aria-label="音频播放进度"
        @keydown="onProgressBarKeyDown"
        @click="seek"
      >
        <div class="absolute inset-0 bg-line-strong/50 rounded-full overflow-hidden">
            <div
              class="h-full bg-ink relative rounded-full transition-all duration-150 ease-out"
              :style="{ width: (currentTime / duration * 100) + '%' }"
            >
            </div>
        </div>
        <div
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-raised border-2 border-line-strong rounded-full shadow-lg opacity-0 group-hover:opacity-100 group-focus-visible:opacity-100 transition-opacity pointer-events-none"
          :style="{ left: `calc(${(currentTime / duration * 100)}% - 8px)` }"
        ></div>
      </div>
    </div>

    <button
      type="button"
      @click="toggleMute"
      :aria-label="isMuted ? '取消静音' : '静音'"
      class="w-8 h-8 rounded-md flex items-center justify-center text-ink-mute hover:text-ink hover:bg-hovered active:scale-90 transition-all duration-150 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ink"
    >
      <svg v-if="!isMuted" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 9.75L19.5 12m0 0l2.25 2.25M19.5 12l2.25-2.25M19.5 12l-2.25 2.25m-10.5-1.5l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
      </svg>
    </button>

    <audio
      ref="audioRef"
      :src="src"
      :loop="loop"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
      @play="onPlay"
      @pause="onPause"
      @ended="emit('ended')"
    ></audio>
  </div>

  <!-- Headless: audio element only -->
  <audio
    v-else
    ref="audioRef"
    :src="src"
    :loop="loop"
    @timeupdate="onTimeUpdate"
    @loadedmetadata="onLoadedMetadata"
    @play="onPlay"
    @pause="onPause"
    @ended="emit('ended')"
  ></audio>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1.2); }
}
</style>
