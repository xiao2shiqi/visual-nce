<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue';
import AudioPlayer from './AudioPlayer.vue';
import LessonDownloadButton from './LessonDownloadButton.vue';
import type { VideoSegment } from '../utils/videoExporter';
import { sceneAnimations } from './scene-animations';

/**
 * @author xiaobin
 */
const props = defineProps<{
  currentImage: string;
  currentClip?: { src?: string; animation?: string; start: number } | null;
  activeSegmentId: string | null;
  audioSrc: string;
  playbackRate: number;
  progress: number;
  segmentsCount: number;
  lessonTitle: string;
  loop?: boolean;
  segments?: VideoSegment[];
}>();

const emit = defineEmits(['timeupdate', 'ended', 'play', 'pause']);
const audioPlayerRef = ref<any>(null);

const progressBarRef = ref<HTMLElement | null>(null);
const isDragging = ref(false);
const isFocused = ref(false);
const dragTime = ref(0);

const localCurrentTime = ref(0);
const localDuration = ref(0);
const localIsPlaying = ref(false);

const displayTime = computed(() => {
  return isDragging.value ? dragTime.value : localCurrentTime.value;
});

const progressPercent = computed(() => {
  if (!localDuration.value || localDuration.value <= 0) return 0;
  return Math.max(0, Math.min(100, (displayTime.value / localDuration.value) * 100));
});

const handleTimeUpdate = (t: number) => {
  if (isDragging.value) return;
  localCurrentTime.value = t;
  emit('timeupdate', t);
};

const formatTime = (seconds: number) => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const seekTo = (seconds: number) => {
  if (!localDuration.value) return;
  const clamped = Math.max(0, Math.min(localDuration.value, seconds));
  const audio = audioPlayerRef.value?.innerAudio;
  if (audio) {
    audio.currentTime = clamped;
  }
  localCurrentTime.value = clamped;
  emit('timeupdate', clamped);
};

const calculateTimeFromEvent = (e: MouseEvent): number => {
  if (!progressBarRef.value || !localDuration.value) return 0;
  const rect = progressBarRef.value.getBoundingClientRect();
  if (rect.width <= 0) return 0;
  const fraction = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  return fraction * localDuration.value;
};

const onMouseMove = (e: MouseEvent) => {
  if (!isDragging.value || !localDuration.value) return;
  dragTime.value = calculateTimeFromEvent(e);
};

const onMouseUp = (e: MouseEvent) => {
  if (!isDragging.value) return;
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);

  const targetTime = calculateTimeFromEvent(e);
  isDragging.value = false;
  seekTo(targetTime);
};

const onMouseDown = (e: MouseEvent) => {
  if (e.button !== 0 || !localDuration.value) return;
  e.preventDefault();
  progressBarRef.value?.focus();

  isDragging.value = true;
  dragTime.value = calculateTimeFromEvent(e);

  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
};

const onKeyDown = (e: KeyboardEvent) => {
  if (!localDuration.value) return;

  const isLeft = e.key === 'ArrowLeft' || e.code === 'ArrowLeft' || e.key === 'ArrowDown' || e.code === 'ArrowDown';
  const isRight = e.key === 'ArrowRight' || e.code === 'ArrowRight' || e.key === 'ArrowUp' || e.code === 'ArrowUp';
  const isHome = e.key === 'Home' || e.code === 'Home';
  const isEnd = e.key === 'End' || e.code === 'End';
  const isSpace = e.key === ' ' || e.code === 'Space';

  if (isLeft) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(localCurrentTime.value - 3);
  } else if (isRight) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(localCurrentTime.value + 3);
  } else if (isHome) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(0);
  } else if (isEnd) {
    e.preventDefault();
    e.stopPropagation();
    seekTo(localDuration.value);
  } else if (isSpace) {
    e.preventDefault();
    e.stopPropagation();
    audioPlayerRef.value?.togglePlay();
  }
};

// ---- 动画片段：静态图之上叠一层静音视频，跟随音频时间轴 ----
const videoRef = ref<HTMLVideoElement | null>(null);
const videoReady = ref(false);
const videoFailed = ref(false);

const syncVideo = () => {
  const video = videoRef.value;
  const clip = props.currentClip;
  if (!video || !clip?.src || !videoReady.value) return;
  video.playbackRate = props.playbackRate;
  const end = Math.max(0, video.duration - 0.05);
  const target = Math.min(Math.max(0, localCurrentTime.value - clip.start), end);
  if (Math.abs(video.currentTime - target) > 0.25) video.currentTime = target;
  const shouldPlay = localIsPlaying.value && target < end;
  if (shouldPlay && video.paused) video.play().catch(() => {});
  if (!shouldPlay && !video.paused) video.pause();
};

watch(() => props.currentClip?.src, () => {
  videoReady.value = false;
  videoFailed.value = false;
});
watch([localCurrentTime, localIsPlaying, () => props.playbackRate], syncVideo);

// 代码绘制的场景动画：直接读音频元素时间，逐帧平滑
const animationComponent = computed(() =>
  props.currentClip?.animation ? sceneAnimations[props.currentClip.animation] ?? null : null
);
const getAudioTime = () => audioPlayerRef.value?.innerAudio?.currentTime ?? localCurrentTime.value;

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);
});

defineExpose({ audioPlayerRef });
</script>

<template>
  <div>

    <!-- Movie Player Container -->
    <div class="relative group rounded-xl overflow-hidden shadow-2xl shadow-zinc-300/40 ring-1 ring-black/5 bg-black aspect-[4/3] cursor-pointer">

      <!-- Scene Image -->
      <img
        :src="currentImage"
        :alt="lessonTitle"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.02]"
      />

      <!-- Scene Clip：有动画时盖在静态图上；加载完成前或失败时显示静态图 -->
      <video
        v-if="currentClip?.src && !videoFailed"
        ref="videoRef"
        :key="currentClip.src"
        :src="currentClip.src"
        muted
        playsinline
        preload="auto"
        aria-hidden="true"
        class="absolute inset-0 w-full h-full object-cover transition-[transform,opacity] duration-700 group-hover:scale-[1.02]"
        :class="videoReady ? 'opacity-100' : 'opacity-0'"
        @loadeddata="videoReady = true; syncVideo()"
        @error="videoFailed = true"
      ></video>

      <!-- Scene Animation：代码绘制，盖在静态图上 -->
      <div v-if="animationComponent" class="absolute inset-0" aria-hidden="true">
        <component :is="animationComponent" :key="currentClip!.animation" :start="currentClip!.start" :get-time="getAudioTime" />
      </div>

      <!-- Center Play/Pause Button -->
      <button
        @click="audioPlayerRef?.togglePlay()"
        aria-label="播放或暂停"
        class="absolute inset-0 flex items-center justify-center transition-opacity duration-200 cursor-pointer focus-visible:outline-none group/centerbtn"
        :class="localIsPlaying ? 'opacity-0 hover:opacity-100 focus-visible:opacity-100' : 'opacity-100'"
      >
        <div class="w-16 h-16 rounded-full bg-black/50 backdrop-blur-sm border border-white/30 flex items-center justify-center text-white hover:scale-110 active:scale-95 group-focus-visible/centerbtn:ring-2 group-focus-visible/centerbtn:ring-white group-focus-visible/centerbtn:ring-offset-2 group-focus-visible/centerbtn:ring-offset-black/60 transition-all duration-150 shadow-2xl">
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
        :class="[
          (localIsPlaying && !isFocused && !isDragging)
            ? 'opacity-0 group-hover:opacity-100 focus-within:opacity-100'
            : 'opacity-100'
        ]"
      >
        <!-- Progress Bar (Slider) -->
        <div
          ref="progressBarRef"
          role="slider"
          tabindex="0"
          aria-label="音频播放进度"
          :aria-valuemin="0"
          :aria-valuemax="localDuration ? Math.floor(localDuration) : 0"
          :aria-valuenow="localDuration ? Math.floor(displayTime) : 0"
          :aria-valuetext="`${formatTime(displayTime)} / ${formatTime(localDuration)}`"
          class="h-1 bg-white/30 rounded-full cursor-pointer mb-3 hover:h-1.5 focus-visible:h-1.5 transition-all duration-150 pointer-events-auto relative group/bar select-none before:absolute before:-top-3.5 before:-bottom-3.5 before:left-0 before:right-0 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-black/60"
          @mousedown="onMouseDown"
          @keydown="onKeyDown"
          @focus="isFocused = true"
          @blur="isFocused = false"
        >
          <!-- Floating Target Time Badge when dragging -->
          <div
            v-if="isDragging"
            class="absolute -top-7 -translate-x-1/2 px-1.5 py-0.5 bg-black/80 backdrop-blur-sm border border-white/20 text-white text-[10px] font-mono font-bold rounded-md shadow-md pointer-events-none select-none"
            :style="{ left: `${progressPercent}%` }"
          >
            {{ formatTime(displayTime) }}
          </div>

          <!-- Progress Fill -->
          <div
            class="h-full bg-white rounded-full pointer-events-none"
            :class="isDragging ? 'transition-none' : 'transition-all duration-150'"
            :style="{ width: `${progressPercent}%` }"
          ></div>

          <!-- Thumb Knob -->
          <div
            class="absolute top-1/2 -translate-y-1/2 w-3.5 h-3.5 bg-white rounded-full shadow-md pointer-events-none transition-opacity duration-150"
            :class="[
              (isDragging || isFocused)
                ? 'opacity-100 scale-110'
                : 'opacity-0 group-hover/bar:opacity-100'
            ]"
            :style="{ left: `calc(${progressPercent}% - 7px)` }"
          ></div>
        </div>

        <!-- Controls Row -->
        <div class="flex items-center justify-between text-white pointer-events-auto">
          <div class="flex items-center gap-3">
            <button
              @click="audioPlayerRef?.togglePlay()"
              aria-label="播放或暂停"
              class="w-8 h-8 rounded-full flex items-center justify-center text-white hover:bg-white/20 active:scale-90 transition-all duration-150 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
            >
              <svg v-if="!localIsPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
              </svg>
            </button>
            <span class="text-xs font-mono text-white/80">
              {{ formatTime(displayTime) }} / {{ formatTime(localDuration) }}
            </span>
          </div>

          <div class="flex items-center gap-2">
            <div v-if="localIsPlaying" class="flex gap-0.5 h-3 items-end">
              <div class="w-0.5 bg-btn animate-[waveBar_0.8s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-btn animate-[waveBar_1.2s_ease-in-out_infinite]"></div>
              <div class="w-0.5 bg-btn animate-[waveBar_1s_ease-in-out_infinite]"></div>
            </div>
            <span class="text-[10px] font-bold text-white/50 uppercase tracking-wider">{{ lessonTitle }}</span>
          </div>
        </div>
      </div>

      <!-- Segment Progress Line (top of bottom bar) -->
      <div class="absolute bottom-0 left-0 right-0 h-0.5 pointer-events-none">
        <div
          class="h-full bg-ink transition-all duration-300"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>

      <!-- Top Badge -->
      <div class="absolute top-4 left-4 pointer-events-none">
        <div class="backdrop-blur-xl bg-black/40 px-3 py-1.5 rounded-full flex items-center gap-2">
          <div class="w-1.5 h-1.5 rounded-full bg-btn animate-pulse"></div>
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
      <div class="absolute -inset-4 bg-gradient-to-r from-zinc-500/10 via-zinc-400/10 to-zinc-500/10 rounded-[2rem] blur-2xl opacity-0 group-hover:opacity-60 transition-opacity duration-700 -z-10 pointer-events-none"></div>

      <!-- Headless Audio Player (logic only) -->
      <AudioPlayer
        :hidden="true"
        ref="audioPlayerRef"
        :src="audioSrc"
        :playback-rate="playbackRate"
        :loop="loop"
        @timeupdate="handleTimeUpdate"
        @play="localIsPlaying = true; emit('play')"
        @pause="localIsPlaying = false; emit('pause')"
        @durationchange="(d) => localDuration = d"
        @ended="emit('ended')"
      />
    </div>

    <!-- Keyboard Shortcuts: 压缩成一行小字，把左栏空间让给语法地图 -->
    <div class="mt-5 pt-4 border-t border-line flex items-center flex-wrap gap-x-4 gap-y-1.5 text-[10px] font-bold text-ink-mute">
      <span class="flex items-center gap-1.5">
        <kbd class="px-1.5 py-0.5 rounded border border-line bg-raised text-[9px] font-black text-ink-soft shadow-sm">Space</kbd>
        播放/暂停
      </span>
      <span class="flex items-center gap-1.5">
        <kbd class="px-1 py-0.5 rounded border border-line bg-raised text-[9px] font-black text-ink-soft shadow-sm">←</kbd>
        <kbd class="px-1 py-0.5 rounded border border-line bg-raised text-[9px] font-black text-ink-soft shadow-sm">→</kbd>
        上/下句
      </span>
      <span class="flex items-center gap-1.5">
        <kbd class="px-1.5 py-0.5 rounded border border-line bg-raised text-[9px] font-black text-ink-soft shadow-sm">R</kbd>
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
