<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted, shallowRef } from 'vue';
import LessonHeader from '../components/LessonHeader.vue';
import SceneViewer from '../components/SceneViewer.vue';
import DialogueScript from '../components/DialogueScript.vue';
import DonationModal from '../components/DonationModal.vue';
import GrammarMap from '../components/GrammarMap.vue';
import BackTranslation from '../components/BackTranslation.vue';
import LearningPath from '../components/LearningPath.vue';
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

// 完整学习闭环（语法预习 + 回译挑战 + 学习动线）：NCE1、NCE2 全量开放（NCE3/4 暂无配套语法预习数据）
const hasFullLoop = (id: string) => id.startsWith('nce1-') || id.startsWith('nce2-');

// 学习动线的引用与完成状态
const grammarMapRef = ref<any>(null);
const backTranslationRef = ref<any>(null);
const completed = ref(false);
const donationModalRef = ref<any>(null);

const STORAGE_KEYS = {
  PLAYBACK_RATE: 'vnce_playback_rate',
  PLAY_MODE: 'vnce_play_mode',
  SHOW_TRANSLATION: 'vnce_show_translation',
  BLIND_MODE: 'vnce_blind_mode',
  LAST_LESSON: 'vnce_last_lesson',
  COMPLETED: 'vnce_completed'
};

// 旧版本另存了一份「已消化」（回译全对自动打勾），现已合并到同一份完成表
const LEGACY_DIGESTED_KEY = 'nce-digested-lessons';

const readCompleted = (): Set<string> => {
  try {
    return new Set<string>(JSON.parse(localStorage.getItem(STORAGE_KEYS.COMPLETED) || '[]'));
  } catch {
    return new Set<string>();
  }
};

try {
  const legacy = localStorage.getItem(LEGACY_DIGESTED_KEY);
  if (legacy) {
    const set = readCompleted();
    for (const id of JSON.parse(legacy) as string[]) set.add(id);
    localStorage.setItem(STORAGE_KEYS.COMPLETED, JSON.stringify([...set]));
    localStorage.removeItem(LEGACY_DIGESTED_KEY);
  }
} catch { /* 迁移失败则忽略，旧标记丢失不影响使用 */ }

const loadCompleted = (id: string) => {
  completed.value = readCompleted().has(id);
};

const currentTime = ref(0);
const playbackRate = ref(Number(localStorage.getItem(STORAGE_KEYS.PLAYBACK_RATE)) || 1.0);
const playbackRates = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0];
const playMode = ref((localStorage.getItem(STORAGE_KEYS.PLAY_MODE) as any) || 'continuous');
const showTranslation = ref(localStorage.getItem(STORAGE_KEYS.SHOW_TRANSLATION) === 'true');
const blindMode = ref(localStorage.getItem(STORAGE_KEYS.BLIND_MODE) === 'true');

// 持久化用户设置
watch(playbackRate, (val) => localStorage.setItem(STORAGE_KEYS.PLAYBACK_RATE, val.toString()));
watch(playMode, (val) => localStorage.setItem(STORAGE_KEYS.PLAY_MODE, val));
watch(showTranslation, (val) => localStorage.setItem(STORAGE_KEYS.SHOW_TRANSLATION, val.toString()));
watch(blindMode, (val) => localStorage.setItem(STORAGE_KEYS.BLIND_MODE, val.toString()));

// ---- 学习进度记忆（首页"继续学习"的数据源）----
let lastProgressSave = 0;
const saveProgress = (time: number) => {
  if (!lessonData.value?.id || time < 3) return;
  localStorage.setItem(STORAGE_KEYS.LAST_LESSON, JSON.stringify({
    id: lessonData.value.id,
    time: Math.floor(time),
    updatedAt: Date.now()
  }));
};

// ---- 课程完成：由学习者在学习动线末尾手动标记，系统只记账、不判定掌握程度 ----
const showCompletionCard = ref(false);
const showWechatQr = ref(false);

const toggleCompleted = () => {
  const id = lessonData.value?.id;
  if (!id) return;
  const set = readCompleted();
  const next = !set.has(id);
  if (next) set.add(id);
  else set.delete(id);
  completed.value = next;
  showCompletionCard.value = next;
  try {
    localStorage.setItem(STORAGE_KEYS.COMPLETED, JSON.stringify([...set]));
  } catch { /* 存储异常时静默跳过 */ }
};

// ---- 跟读模式：每句播完自动停顿一个句长，再续播 ----
let shadowTimer: number | null = null;
let shadowLastSegId: string | null = null;

const clearShadowTimer = () => {
  if (shadowTimer !== null) {
    clearTimeout(shadowTimer);
    shadowTimer = null;
  }
};

const handleShadowing = (time: number) => {
  const segs = lessonData.value?.segments || [];
  const cur = segs.find((s: any) => s.startTime !== undefined && time >= s.startTime && time <= s.endTime);
  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  const audioEl = audioPlayer?.innerAudio;

  // 刚离开上一句（播完或跨句）且没有等待中的停顿 → 暂停，留出跟读时间
  if (shadowLastSegId && cur?.id !== shadowLastSegId && shadowTimer === null && audioEl && !audioEl.paused) {
    const prev = segs.find((s: any) => s.id === shadowLastSegId);
    if (prev) {
      audioPlayer.pause();
      // 停顿时长 = 原句时长（随倍速换算），最少 1.5 秒
      const gapMs = Math.max(1.5, (prev.endTime - prev.startTime) / playbackRate.value) * 1000;
      shadowTimer = window.setTimeout(() => {
        shadowTimer = null;
        if (playMode.value === 'shadowing') audioEl.play();
      }, gapMs);
    }
  }
  shadowLastSegId = cur?.id ?? shadowLastSegId;
};

// 响应式加载课程数据
const lessonData = shallowRef<any>(null);

const preloadLessonImages = (data: any) => {
  const urls = new Set<string>();
  if (data.image) urls.add(resolvePath(data.image));
  data.segments?.forEach((s: any) => {
    if (s.image) urls.add(resolvePath(s.image));
  });
  urls.forEach(src => {
    const img = new Image();
    img.src = src;
  });
};

const loadLessonData = async (id: string) => {
  try {
    // 映射 ID 到文件名，例如 l1 -> l1.json, l127 -> l127.json
    const data = await import(`../data/lessons/${id}.json`);
    lessonData.value = data.default;
    preloadLessonImages(data.default);
    loadCompleted(data.default.id);

    // 重置状态
    currentTime.value = 0;
    singlePlayStartTime.value = null;
    singlePlayEndTime.value = null;
    stopMonitoring();
    clearShadowTimer();
    shadowLastSegId = null;
    lastProgressSave = 0;
    showCompletionCard.value = false;
    showWechatQr.value = false;

    // 续播：如果这就是上次学习的课，把音频定位到上次的位置（不自动播放）
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEYS.LAST_LESSON) || 'null');
      if (saved?.id === id && saved.time > 5) {
        nextTick(() => {
          const audioEl = sceneViewerRef.value?.audioPlayerRef?.innerAudio;
          if (!audioEl) return;
          const seek = () => {
            if (saved.time < (audioEl.duration || Infinity) - 3) {
              audioEl.currentTime = saved.time;
              currentTime.value = saved.time;
            }
          };
          if (audioEl.readyState > 0) seek();
          else audioEl.addEventListener('loadedmetadata', seek, { once: true });
        });
      }
    } catch { /* 记录损坏则忽略 */ }
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

// Track the last clicked segment for single/repeat mode highlight persistence
const lastClickedSegmentId = ref<string | null>(null);

// 计算当前活跃的片段 ID
const activeSegmentId = computed(() => {
  if (!lessonData.value || !lessonData.value.segments || lessonData.value.segments.length === 0) return null;
  const segments = lessonData.value.segments;
  const segment = segments.find(
    (s: any) => s.startTime !== undefined && currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );
  if (segment) return segment.id;

  // 如果当前时间超过了最后一个片段的结束时间，依然保持最后一个片段的高亮（为了体验连贯性）
  const lastSegment = segments[segments.length - 1];
  if (lastSegment && lastSegment.endTime !== undefined && currentTime.value > lastSegment.endTime) {
    return lastSegment.id;
  }

  // In single/repeat mode, keep the last clicked segment highlighted even after playback stops
  if ((playMode.value === 'single' || playMode.value === 'repeat') && lastClickedSegmentId.value) {
    return lastClickedSegmentId.value;
  }

  return null;
});

// 计算当前应显示的图片
const currentImage = computed(() => {
  if (!lessonData.value) return '';

  const segment = lessonData.value.segments.find(
    (s: any) => s.startTime !== undefined && currentTime.value >= s.startTime && currentTime.value <= s.endTime
  );

  // 优先使用当前句子的图片，实现按台词切图
  if (segment?.image) {
    return resolvePath(segment.image);
  }

  let rawImg = '';
  if (segment) {
    // 句子存在但没配置句子图时，回溯最近一个有图的句子；再回退课程主图
    const pastSegments = lessonData.value.segments.filter((s: any) => s.startTime !== undefined && s.startTime <= currentTime.value);
    const latestWithImage = [...pastSegments].reverse().find((s: any) => !!s.image);
    rawImg = latestWithImage?.image || lessonData.value.image || '';
  } else {
    // 不在任何句子时间段时，回溯最近一个有图的句子；再回退课程主图
    const pastSegments = lessonData.value.segments.filter((s: any) => s.startTime !== undefined && s.startTime <= currentTime.value);
    const latestWithImage = [...pastSegments].reverse().find((s: any) => !!s.image);
    if (latestWithImage?.image) {
      rawImg = latestWithImage.image;
    } else if (lessonData.value.segments[0]?.image) {
      rawImg = lessonData.value.segments[0].image;
    } else {
      rawImg = lessonData.value.image || '';
    }
  }

  return resolvePath(rawImg);
});

// 记录当前点击的句子起止时间
const singlePlayStartTime = ref<number | null>(null);
const singlePlayEndTime = ref<number | null>(null);

const handleTimeUpdate = (time: number) => {
  currentTime.value = time;

  // 每 5 秒记录一次学习进度
  if (Math.abs(time - lastProgressSave) > 5) {
    lastProgressSave = time;
    saveProgress(time);
  }

  if (playMode.value === 'shadowing') {
    handleShadowing(time);
  }
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
      // Buffer time before stopping/looping - set to minimal value for precise control
      const bufferTime = 0.05;
      if (audioEl.currentTime >= singlePlayEndTime.value + bufferTime) {
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
      lastClickedSegmentId.value = segment.id; // Track last clicked segment
      singlePlayStartTime.value = segment.startTime;
      singlePlayEndTime.value = segment.endTime;
      audioPlayer.playAt(segment.startTime);
      nextTick(() => startMonitoring());
    } else {
      // continuous / shadowing 模式：点句即从该句起连续播放
      lastClickedSegmentId.value = null;
      singlePlayStartTime.value = null;
      singlePlayEndTime.value = null;
      clearShadowTimer();
      shadowLastSegId = segment.id;
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
  if (newMode !== 'shadowing') {
    clearShadowTimer();
    shadowLastSegId = null;
  }
  if (newMode === 'continuous' || newMode === 'shadowing') {
    lastClickedSegmentId.value = null; // Clear highlight when switching to continuous
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
  clearShadowTimer();
  // 离开课程时保存最终进度
  saveProgress(currentTime.value);
});
</script>

<template>
  <div class="lesson-page min-h-screen pb-44">
    <!-- Ambient Background -->
    <div class="fixed inset-0 -z-10 overflow-hidden">
      <div class="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-bl from-amber-400/10 via-orange-300/5 to-transparent rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-rose-300/10 via-amber-200/5 to-transparent rounded-full blur-3xl"></div>
    </div>

    <LessonHeader 
      v-if="lessonData"
      :title="lessonData.title"
      @back="emit('back')"
      @support-click="donationModalRef?.openDonation()"
    />

    <main v-if="lessonData" class="max-w-6xl mx-auto px-6 py-10">
      <!-- 学习动线：进入课程先看按什么顺序学（试点课程） -->
      <LearningPath
        v-if="hasFullLoop(lessonData.id)"
        :completed="completed"
        @open-grammar="grammarMapRef?.openStudy()"
        @open-challenge="backTranslationRef?.open()"
        @toggle-complete="toggleCompleted"
      />

      <div class="grid grid-cols-12 gap-10">
        <!-- 左栏：播放器 + 快捷键 + 语法地图，整体吸顶 -->
        <div class="col-span-5 sticky top-24 self-start">
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
          :segments="lessonData.segments.map((s: any) => ({
            id: s.id,
            startTime: s.startTime,
            endTime: s.endTime,
            image: resolvePath(s.image || lessonData.image)
          }))"
          @timeupdate="handleTimeUpdate"
        />
        <GrammarMap ref="grammarMapRef" :lesson-id="lessonData.id" />
        </div>

        <DialogueScript
          ref="scriptRef"
          :segments="lessonData.segments"
          :active-segment-id="activeSegmentId"
          v-model:play-mode="playMode"
          v-model:playback-rate="playbackRate"
          v-model:show-translation="showTranslation"
          v-model:blind-mode="blindMode"
          :playback-rates="playbackRates"
          @segment-click="handleSegmentClick"
        />
      </div>

      <!-- 回译挑战：选做的输出练习，不参与完成标记 -->
      <div v-if="hasFullLoop(lessonData.id)" class="mt-10 max-w-xl mx-auto text-center animate-fade-in">
        <BackTranslation
          ref="backTranslationRef"
          :lesson-title="lessonData.title"
          :segments="lessonData.segments"
          @replay-segment="handleSegmentClick"
          class="!mt-0 !py-3 !text-sm !rounded-2xl"
        />
      </div>

      <!-- Quick Navigation -->
      <div class="mt-12 pt-8 border-t border-slate-200/60 grid grid-cols-2 gap-6 animate-fade-in">
        <button 
          v-if="navigation.prev"
          @click="emit('select-course', navigation.prev)"
          class="flex items-center gap-4 p-5 rounded-2xl bg-white/50 backdrop-blur-sm border border-slate-200 hover:border-amber-500/60 hover:bg-white hover:shadow-xl hover:shadow-amber-500/5 transition-all duration-500 group text-left"
        >
          <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-amber-50 group-hover:text-amber-600 transition-all duration-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </div>
          <div class="overflow-hidden">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1 group-hover:text-amber-500 transition-colors">Previous Lesson</div>
            <div class="text-base font-bold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
              {{ navigation.prev.title }}: {{ navigation.prev.subtitle }}
            </div>
          </div>
        </button>
        <div v-else class="block"></div>

        <button 
          v-if="navigation.next"
          @click="emit('select-course', navigation.next)"
          class="flex items-center justify-end gap-4 p-5 rounded-2xl bg-white/50 backdrop-blur-sm border border-slate-200 hover:border-amber-500/60 hover:bg-white hover:shadow-xl hover:shadow-amber-500/5 transition-all duration-500 group text-right"
        >
          <div class="overflow-hidden">
            <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1 group-hover:text-amber-500 transition-colors">Next Lesson</div>
            <div class="text-base font-bold text-slate-700 group-hover:text-slate-900 transition-colors truncate">
              {{ navigation.next.title }}: {{ navigation.next.subtitle }}
            </div>
          </div>
          <div class="w-12 h-12 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-amber-50 group-hover:text-amber-600 transition-all duration-500">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </div>
        </button>
      </div>
    </main>

    <!-- Completion Card：手动标记学完后的轻量提示，右下角滑入 -->
    <Transition name="completion">
      <div
        v-if="showCompletionCard"
        class="fixed bottom-6 right-6 z-40 w-72 rounded-2xl bg-white/95 backdrop-blur-sm border border-amber-200/70 shadow-xl shadow-amber-900/10 p-5"
      >
        <button
          @click="showCompletionCard = false"
          class="absolute top-3 right-3 w-6 h-6 rounded-full flex items-center justify-center text-slate-300 hover:text-slate-500 hover:bg-slate-100 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="flex items-center gap-3 mb-4">
          <div class="w-9 h-9 rounded-full bg-amber-600 flex items-center justify-center shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="white" class="w-4.5 h-4.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-black text-slate-800">已标记学完</p>
            <p class="text-[11px] text-slate-400">已记入学习进度</p>
          </div>
        </div>

        <button
          v-if="navigation.next"
          @click="emit('select-course', navigation.next)"
          class="w-full py-2.5 rounded-xl bg-amber-600 text-white text-sm font-bold hover:bg-amber-700 transition-colors"
        >
          下一课：{{ navigation.next.title }} →
        </button>

        <button
          @click="showWechatQr = !showWechatQr"
          class="mt-3 w-full text-center text-[11px] text-slate-400 hover:text-amber-700 transition-colors"
        >
          觉得有用？加作者微信交流学习
        </button>
        <img
          v-if="showWechatQr"
          src="/images/wechat_qr.png"
          alt="作者微信"
          class="mt-2 w-40 mx-auto rounded-xl border border-slate-100"
        />
      </div>
    </Transition>

    <!-- Loading State -->
    <div v-if="!lessonData" class="flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-amber-600/20 border-t-amber-600 rounded-full animate-spin"></div>
        <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">Loading Lesson...</p>
      </div>
    </div>
    <DonationModal ref="donationModalRef" />
  </div>
</template>

<style scoped>
/* 完成卡滑入动画 */
.completion-enter-active,
.completion-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.completion-enter-from,
.completion-leave-to {
  opacity: 0;
  transform: translateY(16px);
}

.lesson-page {
  background: linear-gradient(to bottom, #fafbfc, #f5f7fa);
}
</style>
