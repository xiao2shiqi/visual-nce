<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, shallowRef } from 'vue';
import LessonHeader from '../components/LessonHeader.vue';
import SceneViewer from '../components/SceneViewer.vue';
import DialogueScript from '../components/DialogueScript.vue';
import { resolvePath } from '../utils/resolvePath';

/**
 * @author xiaobin
 */
const props = defineProps<{
  lesson: any;
}>();

const emit = defineEmits(['back']);
const sceneViewerRef = ref<any>(null);
const scriptRef = ref<any>(null);

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
  if (!lessonData.value) return null;
  const segment = lessonData.value.segments.find(
    (s: any) => currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  return segment ? segment.id : null;
});

// 计算当前应显示的图片
const currentImage = computed(() => {
  if (!lessonData.value) return '';
  
  const segment = lessonData.value.segments.find(
    (s: any) => currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  
  let rawImg = '';
  if (segment && segment.image) {
    rawImg = segment.image;
  } else {
    // 保持显示最后一张匹配的图片，避免空白
    const pastSegments = lessonData.value.segments.filter((s: any) => s.startTime <= currentTime.value);
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
  stopMonitoring(); 
  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  
  if (playMode.value === 'single' || playMode.value === 'repeat') {
    singlePlayStartTime.value = segment.startTime;
    singlePlayEndTime.value = segment.endTime;
    audioPlayer?.playAt(segment.startTime);
    nextTick(() => startMonitoring());
  } else {
    singlePlayStartTime.value = null;
    singlePlayEndTime.value = null;
    audioPlayer?.playAt(segment.startTime);
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
      badge="Visual NCE"
      @back="emit('back')"
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
    </main>

    <!-- Loading State -->
    <div v-else class="flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin"></div>
        <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">Loading Lesson...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lesson-page {
  background: linear-gradient(to bottom, #fafbfc, #f5f7fa);
}
</style>
