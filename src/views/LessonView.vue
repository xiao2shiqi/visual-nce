<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted, shallowRef } from 'vue';
import LessonHeader from '../components/LessonHeader.vue';
import SceneViewer from '../components/SceneViewer.vue';
import DialogueScript from '../components/DialogueScript.vue';
import DonationModal from '../components/DonationModal.vue';
import curriculum from '../data/curriculum.json';
import { resolvePath } from '../utils/resolvePath';

/**
 * @author xiaobin
 */
const props = defineProps<{
  lesson: any;
}>();

const emit = defineEmits(['back', 'select-course']);
const sceneViewerRef = ref<any>(null);
const scriptRef = ref<any>(null);
const donationModalRef = ref<any>(null);

const currentTime = ref(0);
const playbackRate = ref(1.0);
const playbackRates = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
const playMode = ref<'continuous' | 'single' | 'repeat'>('continuous');
const showTranslation = ref(false);

// 响应式加载课程数据
const lessonData = shallowRef<any>(null);

const loadLessonData = async (id: string) => {
  try {
    // 映射 ID 到文件名，例如 l1 -> l1.json, l127 -> l127.json
    const data = await import(`../data/lessons/${id}.json`);
    lessonData.value = data.default;
    
    // 重置状态
    currentTime.value = 0;
    singlePlayStartTime.value = null;
    singlePlayEndTime.value = null;
    stopMonitoring();
  } catch (err) {
    console.error(`Failed to load lesson data for ${id}:`, err);
  }
};

onMounted(() => {
  if (props.lesson?.id) {
    loadLessonData(props.lesson.id);
  }
});

watch(() => props.lesson?.id, (newId) => {
  if (newId) loadLessonData(newId);
});


// 计算当前活跃的片段 ID
const activeSegmentId = computed(() => {
  if (!lessonData.value || !lessonData.value.segments) return null;
  const segment = lessonData.value.segments.find(
    (s: any) => s.startTime !== undefined && currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  return segment ? segment.id : null;
});

// 计算当前应显示的图片
const currentImage = computed(() => {
  if (!lessonData.value) return '';
  
  // 优先使用根节点的图片
  if (lessonData.value.image) {
    return resolvePath(lessonData.value.image);
  }
  
  const segment = lessonData.value.segments.find(
    (s: any) => s.startTime !== undefined && currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  
  let rawImg = '';
  if (segment && segment.image) {
    rawImg = segment.image;
  } else {
    // 保持显示最后一张匹配的图片，避免空白
    const pastSegments = lessonData.value.segments.filter((s: any) => s.startTime !== undefined && s.startTime <= currentTime.value);
    if (pastSegments.length > 0) {
      rawImg = pastSegments[pastSegments.length - 1].image;
    } else {
      rawImg = lessonData.value.segments[0]?.image || '';
    }
  }
  
  return resolvePath(rawImg);
});

// 记录当前点击的句子起止时间
const singlePlayStartTime = ref<number | null>(null);
const singlePlayEndTime = ref<number | null>(null);

const handleTimeUpdate = (time: number) => {
  currentTime.value = time;
};

// 核心逻辑：利用 requestAnimationFrame 实现高精度的停止控制
let rafId: number | null = null;

const startMonitoring = () => {
  const monitor = () => {
    const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
    if (!audioPlayer || playMode.value === 'continuous' || singlePlayEndTime.value === null) {
      stopMonitoring();
      return;
    }
    
    const audioEl = audioPlayer.innerAudio;
    if (audioEl) {
      if (audioEl.currentTime >= singlePlayEndTime.value - 0.1) {
        if (playMode.value === 'single') {
          audioPlayer.pause();
          singlePlayEndTime.value = null;
          stopMonitoring();
          return;
        } else if (playMode.value === 'repeat' && singlePlayStartTime.value !== null) {
          audioPlayer.playAt(singlePlayStartTime.value);
        }
      }
    }
    rafId = requestAnimationFrame(monitor);
  };
  rafId = requestAnimationFrame(monitor);
};

const stopMonitoring = () => {
  if (rafId !== null) {
    cancelAnimationFrame(rafId);
    rafId = null;
  }
};

const handleSegmentClick = (segment: any) => {
  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  if (!audioPlayer) return;

  if (segment.startTime !== undefined) {
    stopMonitoring(); 
    if (playMode.value === 'single' || playMode.value === 'repeat') {
      singlePlayStartTime.value = segment.startTime;
      singlePlayEndTime.value = segment.endTime;
      audioPlayer.playAt(segment.startTime);
      nextTick(() => startMonitoring());
    } else {
      singlePlayStartTime.value = null;
      singlePlayEndTime.value = null;
      audioPlayer.playAt(segment.startTime);
    }
  } else {
    // If no timing, clicking a segment just toggles main playback
    if (audioPlayer.innerAudio?.paused) {
      audioPlayer.innerAudio.play();
    } else {
      audioPlayer.innerAudio?.pause();
    }
  }
};

// 模式切换时清理
watch(playMode, (newMode) => {
  if (newMode === 'continuous') {
    singlePlayStartTime.value = null;
    singlePlayEndTime.value = null;
    stopMonitoring();
  } else if (activeSegmentId.value && lessonData.value) {
    const segment = lessonData.value.segments.find((s: any) => s.id === activeSegmentId.value);
    if (segment) {
      singlePlayStartTime.value = segment.startTime;
      singlePlayEndTime.value = segment.endTime;
      startMonitoring();
    }
  }
});

// 监听活跃片段变化，自动滚动
watch(activeSegmentId, async (newId) => {
  if (newId) {
    await nextTick();
    scriptRef.value?.scrollToActive(newId);
  }
});

// 计算上一课和下一课
const navigation = computed(() => {
  if (!props.lesson?.id) return { prev: null, next: null };
  
  // 查找当前课程所在的课本
  const book = curriculum.books.find(b => b.lessons.some(l => l.id === props.lesson.id));
  if (!book) return { prev: null, next: null };
  
  const allLessons = book.lessons;
  const currentIdx = allLessons.findIndex(l => l.id === props.lesson.id);
  
  return {
    prev: currentIdx > 0 ? allLessons[currentIdx - 1] : null,
    next: currentIdx < allLessons.length - 1 ? allLessons[currentIdx + 1] : null
  };
});

// 快捷键处理
const handleKeyDown = (e: KeyboardEvent) => {
  if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) return;

  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  if (!audioPlayer || !lessonData.value) return;

  const segments = lessonData.value.segments;
  const currentIndex = segments.findIndex((s: any) => s.id === activeSegmentId.value);

  switch (e.code) {
    case 'Space':
      e.preventDefault();
      if (audioPlayer.innerAudio?.paused) {
        audioPlayer.innerAudio.play();
      } else {
        audioPlayer.innerAudio?.pause();
      }
      break;

    case 'ArrowLeft':
      e.preventDefault();
      if (currentIndex > 0) {
        handleSegmentClick(segments[currentIndex - 1]);
      } else if (currentIndex === 0) {
        audioPlayer.playAt(0);
      } else {
        // 如果当前不在任何片段中，找到前一个最近的片段
        const prevIdx = segments.reduce((acc: number, s: any, idx: number) => 
          s.startTime < currentTime.value ? idx : acc, -1);
        if (prevIdx !== -1) handleSegmentClick(segments[prevIdx]);
      }
      break;

    case 'ArrowRight':
      e.preventDefault();
      if (currentIndex !== -1 && currentIndex < segments.length - 1) {
        handleSegmentClick(segments[currentIndex + 1]);
      } else if (currentIndex === -1) {
        // 如果当前不在任何片段中，找到后一个最近的片段
        const nextIdx = segments.findIndex((s: any) => s.startTime > currentTime.value);
        if (nextIdx !== -1) handleSegmentClick(segments[nextIdx]);
      }
      break;

    case 'KeyR':
      e.preventDefault();
      if (currentIndex !== -1) {
        handleSegmentClick(segments[currentIndex]);
      } else {
        audioPlayer.playAt(0);
      }
      break;
  }
};

onMounted(() => {
  if (props.lesson?.id) {
    loadLessonData(props.lesson.id);
  }
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
  <div class="lesson-page min-h-screen pb-44">
    <!-- Ambient Background -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-bl from-blue-400/10 via-indigo-300/5 to-transparent rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-violet-400/10 via-pink-300/5 to-transparent rounded-full blur-3xl"></div>
    </div>

    <LessonHeader 
      v-if="lessonData"
      :title="lessonData.title"
      @back="emit('back')"
      @support-click="donationModalRef?.openDonation()"
    />

    <main v-if="lessonData" class="max-w-6xl mx-auto px-6 py-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <SceneViewer 
          ref="sceneViewerRef"
          :current-image="currentImage"
          :active-segment-id="activeSegmentId"
          :audio-src="resolvePath(lessonData.audio)"
          :playback-rate="playbackRate"
          :progress="(lessonData.segments.findIndex((s: any) => s.id === activeSegmentId) + 1) / lessonData.segments.length * 100"
          :segments-count="lessonData.segments.length"
          :lesson-title="lessonData.title"
          :loop="playMode === 'continuous'"
          @timeupdate="handleTimeUpdate"
        />

        <DialogueScript 
          ref="scriptRef"
          :segments="lessonData.segments"
          :active-segment-id="activeSegmentId"
          v-model:play-mode="playMode"
          v-model:playback-rate="playbackRate"
          v-model:show-translation="showTranslation"
          :playback-rates="playbackRates"
          @segment-click="handleSegmentClick"
        />
      </div>

      <!-- Quick Navigation -->
      <div class="mt-20 pt-10 border-t border-slate-200/60 grid grid-cols-1 sm:grid-cols-2 gap-6 animate-fade-in">
        <button 
          v-if="navigation.prev"
          @click="emit('select-course', navigation.prev)"
          class="flex items-center gap-4 p-5 rounded-2xl bg-white/50 backdrop-blur-sm border border-slate-200 hover:border-blue-400 hover:bg-white hover:shadow-xl hover:shadow-blue-500/5 transition-all duration-500 group text-left"
        >
          <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition-all duration-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </div>
          <div class="overflow-hidden">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1 group-hover:text-blue-400 transition-colors">Previous Lesson</div>
            <div class="text-base font-bold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
              {{ navigation.prev.title }}: {{ navigation.prev.subtitle }}
            </div>
          </div>
        </button>
        <div v-else class="hidden sm:block"></div>

        <button 
          v-if="navigation.next"
          @click="emit('select-course', navigation.next)"
          class="flex items-center justify-end gap-4 p-5 rounded-2xl bg-white/50 backdrop-blur-sm border border-slate-200 hover:border-indigo-400 hover:bg-white hover:shadow-xl hover:shadow-indigo-500/5 transition-all duration-500 group text-right"
        >
          <div class="overflow-hidden">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1 group-hover:text-indigo-400 transition-colors">Next Lesson</div>
            <div class="text-base font-bold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
              {{ navigation.next.title }}: {{ navigation.next.subtitle }}
            </div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-indigo-50 group-hover:text-indigo-500 transition-all duration-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </div>
        </button>
      </div>
    </main>

    <!-- Loading State -->
    <div v-else class="flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin"></div>
        <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">Loading Lesson...</p>
      </div>
    </div>
    <DonationModal ref="donationModalRef" />
  </div>
</template>

<style scoped>
.lesson-page {
  background: linear-gradient(to bottom, #fafbfc, #f5f7fa);
}
</style>
