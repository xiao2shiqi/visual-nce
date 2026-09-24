<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted, shallowRef } from 'vue';
import LessonHeader from '../components/LessonHeader.vue';
import SceneViewer from '../components/SceneViewer.vue';
import DialogueScript from '../components/DialogueScript.vue';
import DonationModal from '../components/DonationModal.vue';
import GrammarMap from '../components/GrammarMap.vue';
import BackTranslation from '../components/BackTranslation.vue';
import LearningPath from '../components/LearningPath.vue';
import ShortcutHelp from '../components/ShortcutHelp.vue';
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
const isPlaying = ref(false);
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

// ==========================================
// 性能优化：按需滑动窗口预加载 + 网络感知 + 空闲调度 + 中止控制
// ==========================================

// 1. 网络感知（实验性 API 防御性检测，不支持时静默回退）
const isSaveDataOrSlowNetwork = (): boolean => {
  if (typeof navigator === 'undefined') return false;
  const conn = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection;
  if (!conn) return false;
  if (conn.saveData === true) return true;
  const effectiveType = conn.effectiveType;
  if (effectiveType === 'slow-2g' || effectiveType === '2g' || effectiveType === '3g') return true;
  return false;
};

// 2. 空闲调度（requestIdleCallback + Safari/老浏览器 setTimeout 兜底）
const runWhenIdle = (cb: () => void, timeout = 2000): number => {
  const win = typeof window !== 'undefined' ? (window as any) : null;
  if (win && typeof win.requestIdleCallback === 'function') {
    return win.requestIdleCallback(cb, { timeout });
  }
  return setTimeout(cb, Math.min(timeout, 300)) as unknown as number;
};

const cancelIdle = (id: number) => {
  const win = typeof window !== 'undefined' ? (window as any) : null;
  if (win && typeof win.cancelIdleCallback === 'function') {
    win.cancelIdleCallback(id);
  } else {
    clearTimeout(id);
  }
};

// 3. 预加载状态管理与取消机制
let preloadGeneration = 0;
let idleCallbackId: number | null = null;
let preloadAbortController: AbortController | null = null;
const prefetchedUrls = new Set<string>();
const PRELOAD_WINDOW_SIZE = 2; // 预取后续 1~2 张不重复插图

const cancelCurrentPreload = () => {
  preloadGeneration++;
  if (idleCallbackId !== null) {
    cancelIdle(idleCallbackId);
    idleCallbackId = null;
  }
  if (preloadAbortController) {
    preloadAbortController.abort();
    preloadAbortController = null;
  }
  prefetchedUrls.clear();
};

const prefetchImage = async (url: string, signal: AbortSignal): Promise<void> => {
  if (prefetchedUrls.has(url) || signal.aborted) return;
  prefetchedUrls.add(url);

  try {
    const response = await fetch(url, { signal, priority: 'low' as any });
    if (response.ok && !signal.aborted) {
      // 触发底层解码缓存，保证视口切图时 0 延迟渲染
      const img = new Image();
      img.src = url;
    } else {
      prefetchedUrls.delete(url);
    }
  } catch (err: any) {
    if (err?.name !== 'AbortError') {
      // 非主动中止的偶发网络错误允许后续重试
      prefetchedUrls.delete(url);
    }
  }
};

// 4. 滑动窗口计算：基于当前播放句，向后查找后续 1~2 张未缓存插图
const preloadUpcomingImages = async () => {
  if (!lessonData.value || !lessonData.value.segments) return;
  if (isSaveDataOrSlowNetwork()) return;

  const currentGen = preloadGeneration;
  const signal = preloadAbortController?.signal;
  if (!signal || signal.aborted) return;

  const segments = lessonData.value.segments;
  // 查找当前句所在的序号；若未播放则从首句开始
  const curId = activeSegmentId.value;
  let curIdx = segments.findIndex((s: any) => s.id === curId);
  if (curIdx === -1) {
    curIdx = segments.findIndex((s: any) => s.startTime !== undefined && currentTime.value <= s.endTime);
    if (curIdx === -1) curIdx = 0;
  }

  const curImgUrl = currentImage.value;
  const targetsToFetch: string[] = [];

  for (let i = curIdx + 1; i < segments.length; i++) {
    const rawImg = segments[i]?.image;
    if (!rawImg) continue;
    const resolved = resolvePath(rawImg);
    if (!resolved || resolved === curImgUrl) continue;
    if (prefetchedUrls.has(resolved)) continue;
    if (!targetsToFetch.includes(resolved)) {
      targetsToFetch.push(resolved);
      if (targetsToFetch.length >= PRELOAD_WINDOW_SIZE) break;
    }
  }

  if (targetsToFetch.length === 0) return;

  for (const url of targetsToFetch) {
    if (currentGen !== preloadGeneration || signal.aborted) return;
    await prefetchImage(url, signal);
  }
};

// 5. 空闲时机调度（防抖避免频繁触发）
const scheduleIdlePreload = (delay = 1500) => {
  if (isSaveDataOrSlowNetwork()) return;

  if (idleCallbackId !== null) {
    cancelIdle(idleCallbackId);
    idleCallbackId = null;
  }

  const currentGen = preloadGeneration;
  idleCallbackId = runWhenIdle(() => {
    idleCallbackId = null;
    if (currentGen !== preloadGeneration) return;
    preloadUpcomingImages();
  }, delay);
};

const loadLessonData = async (id: string) => {
  // 切课时立即中止上一课正在进行的预加载网络请求和定时器
  cancelCurrentPreload();
  preloadAbortController = new AbortController();
  const currentGen = preloadGeneration;

  try {
    // 映射 ID 到文件名，例如 l1 -> l1.json, l127 -> l127.json
    const data = await import(`../data/lessons/${id}.json`);
    // 如果异步加载期间用户已切到其他课，丢弃已过期的旧课数据
    if (currentGen !== preloadGeneration) return;

    lessonData.value = data.default;
    loadCompleted(data.default.id);

    // 重置状态
    currentTime.value = 0;
    isPlaying.value = false;
    singlePlayStartTime.value = null;
    singlePlayEndTime.value = null;
    stopMonitoring();
    clearShadowTimer();
    shadowLastSegId = null;
    lastProgressSave = 0;
    showCompletionCard.value = false;
    showWechatQr.value = false;

    // 让路给关键路径：首屏只渲染当前主图/首句图。
    // 后续图片的预取等待音频就绪（canplaythrough）或浏览器处于空闲时再启动
    nextTick(() => {
      const audioEl = sceneViewerRef.value?.audioPlayerRef?.innerAudio;
      if (audioEl && !isSaveDataOrSlowNetwork()) {
        if (audioEl.readyState >= 4) {
          scheduleIdlePreload(600);
        } else {
          audioEl.addEventListener('canplaythrough', () => {
            if (currentGen === preloadGeneration) {
              scheduleIdlePreload(600);
            }
          }, { once: true });
          // 兜底超时：避免音频因外部网络挂起导致永远不触发预加载
          scheduleIdlePreload(2500);
        }
      } else {
        scheduleIdlePreload(1500);
      }
    });

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

// 当前画面对应的动画：取最近一个已开始的有图句子，若它配了 video 或 animation 就播放
// 动画时间 = 音频时间 - 该句 startTime；video 播完停在最后一帧，animation 为代码绘制的场景
const currentClip = computed(() => {
  if (!lessonData.value) return null;
  const source = [...lessonData.value.segments]
    .reverse()
    .find((s: any) => s.image && s.startTime !== undefined && s.startTime <= currentTime.value);
  if (source?.animation) return { animation: source.animation as string, start: source.startTime as number };
  if (source?.video) return { src: resolvePath(source.video), start: source.startTime as number };
  return null;
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
    const audioEl = audioPlayer.innerAudio;
    // 如果点击的是当前正在播放的句子，再次点击则暂停
    if (activeSegmentId.value === segment.id && audioEl && !audioEl.paused) {
      audioPlayer.pause();
      return;
    }

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

// 监听活跃片段变化，自动滚动与滑动窗口预取
watch(activeSegmentId, async (newId) => {
  if (newId) {
    await nextTick();
    scriptRef.value?.scrollToActive(newId);
    scheduleIdlePreload(300);
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

// 快捷键帮助浮层状态
const showShortcutHelp = ref(false);

// 快捷键轻量视觉反馈 Toast
const toastText = ref('');
const showToastNotification = ref(false);
let toastTimer: number | null = null;

const showToast = (msg: string) => {
  toastText.value = msg;
  showToastNotification.value = true;
  if (toastTimer !== null) {
    clearTimeout(toastTimer);
  }
  toastTimer = window.setTimeout(() => {
    showToastNotification.value = false;
    toastTimer = null;
  }, 1000);
};

// 档位变速调节（0.75x ~ 2.0x）
const changePlaybackRate = (delta: number) => {
  let currentIdx = playbackRates.indexOf(playbackRate.value);
  if (currentIdx === -1) {
    let minDiff = Infinity;
    playbackRates.forEach((r, idx) => {
      const diff = Math.abs(r - playbackRate.value);
      if (diff < minDiff) {
        minDiff = diff;
        currentIdx = idx;
      }
    });
  }
  const newIdx = Math.max(0, Math.min(playbackRates.length - 1, currentIdx + delta));
  playbackRate.value = playbackRates[newIdx]!;
  showToast(`播放速度：${playbackRate.value === 1.0 ? '1.0x' : playbackRate.value + 'x'}`);
};

// 重听当前句（从当前句起始位置重新播放）
const replaySegment = (segment: any) => {
  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  if (!audioPlayer) return;

  if (segment && segment.startTime !== undefined) {
    stopMonitoring();
    if (playMode.value === 'single' || playMode.value === 'repeat') {
      lastClickedSegmentId.value = segment.id;
      singlePlayStartTime.value = segment.startTime;
      singlePlayEndTime.value = segment.endTime;
      audioPlayer.playAt(segment.startTime);
      nextTick(() => startMonitoring());
    } else {
      lastClickedSegmentId.value = null;
      singlePlayStartTime.value = null;
      singlePlayEndTime.value = null;
      clearShadowTimer();
      shadowLastSegId = segment.id;
      audioPlayer.playAt(segment.startTime);
    }
  } else {
    audioPlayer.playAt(0);
  }
};

// 快捷键处理
const handleKeyDown = (e: KeyboardEvent) => {
  if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement).tagName)) return;

  // 快捷键帮助浮层打开时，按 Escape 或 ? 键关闭
  if (showShortcutHelp.value) {
    if (e.key === 'Escape' || e.code === 'Escape' || e.key === '?') {
      e.preventDefault();
      showShortcutHelp.value = false;
      return;
    }
  }

  // 问号键：打开/关闭快捷键帮助浮层
  if (e.key === '?' || (e.shiftKey && e.code === 'Slash')) {
    e.preventDefault();
    showShortcutHelp.value = !showShortcutHelp.value;
    return;
  }

  const audioPlayer = sceneViewerRef.value?.audioPlayerRef;
  if (!audioPlayer || !lessonData.value) return;

  const segments = lessonData.value.segments;
  const currentIndex = segments.findIndex((s: any) => s.id === activeSegmentId.value);

  // 减号键降速 / 等号键升速
  if (e.key === '-' || e.key === '_' || e.code === 'Minus' || e.code === 'NumpadSubtract') {
    e.preventDefault();
    changePlaybackRate(-1);
    return;
  }
  if (e.key === '=' || e.key === '+' || e.code === 'Equal' || e.code === 'NumpadAdd') {
    e.preventDefault();
    changePlaybackRate(1);
    return;
  }

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

    case 'KeyR': {
      e.preventDefault();
      if (currentIndex !== -1) {
        replaySegment(segments[currentIndex]);
      } else {
        const prevIdx = segments.reduce((acc: number, s: any, idx: number) => 
          s.startTime < currentTime.value ? idx : acc, -1);
        if (prevIdx !== -1) {
          replaySegment(segments[prevIdx]);
        } else if (segments.length > 0) {
          replaySegment(segments[0]);
        } else {
          audioPlayer.playAt(0);
        }
      }
      showToast('重听当前句');
      break;
    }

    case 'KeyL': {
      e.preventDefault();
      const modes: Array<'continuous' | 'single' | 'repeat' | 'shadowing'> = [
        'continuous',
        'single',
        'repeat',
        'shadowing'
      ];
      const modeLabels: Record<string, string> = {
        continuous: '连读模式',
        single: '点读模式',
        repeat: '循环模式',
        shadowing: '跟读模式'
      };
      const idx = modes.indexOf(playMode.value);
      const nextMode = modes[(idx + 1) % modes.length]!;
      playMode.value = nextMode;
      showToast(`播放模式：${modeLabels[nextMode]}`);
      break;
    }

    case 'KeyT':
      e.preventDefault();
      showTranslation.value = !showTranslation.value;
      showToast(`译文显示：${showTranslation.value ? '已开启' : '已关闭'}`);
      break;

    case 'KeyB':
      e.preventDefault();
      blindMode.value = !blindMode.value;
      showToast(`盲听模式：${blindMode.value ? '已开启' : '已关闭'}`);
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
  cancelCurrentPreload();
  window.removeEventListener('keydown', handleKeyDown);
  clearShadowTimer();
  if (toastTimer !== null) {
    clearTimeout(toastTimer);
    toastTimer = null;
  }
  // 离开课程时保存最终进度
  saveProgress(currentTime.value);
});
</script>

<template>
  <div class="lesson-page min-h-screen pb-44">
    <LessonHeader 
      v-if="lessonData"
      :title="lessonData.title"
      @back="emit('back')"
      @support-click="donationModalRef?.openDonation()"
    />

    <main v-if="lessonData" class="max-w-7xl mx-auto px-6 sm:px-8 py-8">
      <!-- 学习动线：进入课程先看按什么顺序学（试点课程） -->
      <LearningPath
        v-if="hasFullLoop(lessonData.id)"
        :completed="completed"
        @open-grammar="grammarMapRef?.openStudy()"
        @open-challenge="backTranslationRef?.open()"
        @toggle-complete="toggleCompleted"
      />

      <div class="grid grid-cols-12 gap-8 lg:gap-10">
        <!-- 左栏：播放器 + 快捷键 + 语法地图，整体吸顶 -->
        <div class="col-span-5 sticky top-20 self-start">
        <SceneViewer
          ref="sceneViewerRef"
          :current-image="currentImage"
          :current-clip="currentClip"
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
          @play="isPlaying = true"
          @pause="isPlaying = false"
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
          :is-playing="isPlaying"
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
          class="!mt-0 !py-3 !text-sm !rounded-xl"
        />
      </div>

      <!-- Quick Navigation -->
      <div class="mt-14 pt-8 border-t border-line grid grid-cols-2 gap-6 animate-fade-in">
        <button 
          v-if="navigation.prev"
          @click="emit('select-course', navigation.prev)"
          class="flex items-center gap-4 p-5 rounded-xl bg-raised border border-line hover:border-line-strong hover:bg-hovered/40 shadow-xs hover:shadow-md transition-all duration-300 group text-left cursor-pointer"
        >
          <div class="w-11 h-11 rounded-xl bg-hovered border border-line flex items-center justify-center text-ink-mute group-hover:text-ink group-hover:border-line-strong transition-all duration-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 group-hover:-translate-x-0.5 transition-transform">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
          </div>
          <div class="overflow-hidden min-w-0">
            <div class="text-xs font-mono font-bold text-ink-mute uppercase tracking-wider mb-1">Previous Lesson</div>
            <div class="font-display text-lg sm:text-xl font-bold text-ink group-hover:text-ink transition-colors truncate">
              {{ navigation.prev.title }}: {{ navigation.prev.subtitle }}
            </div>
          </div>
        </button>
        <div v-else class="block"></div>

        <button 
          v-if="navigation.next"
          @click="emit('select-course', navigation.next)"
          class="flex items-center justify-end gap-4 p-5 rounded-xl bg-raised border border-line hover:border-line-strong hover:bg-hovered/40 shadow-xs hover:shadow-md transition-all duration-300 group text-right cursor-pointer"
        >
          <div class="overflow-hidden min-w-0">
            <div class="text-xs font-mono font-bold text-ink-mute uppercase tracking-wider mb-1">Next Lesson</div>
            <div class="font-display text-lg sm:text-xl font-bold text-ink group-hover:text-ink transition-colors truncate">
              {{ navigation.next.title }}: {{ navigation.next.subtitle }}
            </div>
          </div>
          <div class="w-11 h-11 rounded-xl bg-hovered border border-line flex items-center justify-center text-ink-mute group-hover:text-ink group-hover:border-line-strong transition-all duration-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 group-hover:translate-x-0.5 transition-transform">
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
        class="fixed bottom-6 right-6 z-40 w-72 rounded-xl bg-raised border border-line shadow-2xl p-5"
      >
        <button
          @click="showCompletionCard = false"
          class="absolute top-3 right-3 w-6 h-6 rounded-full flex items-center justify-center text-ink-mute hover:text-ink hover:bg-hovered transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="flex items-center gap-3 mb-4">
          <div class="w-9 h-9 rounded-full bg-btn flex items-center justify-center shadow-xs text-btn-fg shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-4.5 h-4.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-bold text-ink">已标记学完</p>
            <p class="text-xs text-ink-mute font-mono">已记入学习进度</p>
          </div>
        </div>

        <button
          v-if="navigation.next"
          @click="emit('select-course', navigation.next)"
          class="btn-primary w-full py-2.5 !rounded-xl text-xs font-bold transition-all cursor-pointer"
        >
          下一课：{{ navigation.next.title }} →
        </button>

        <button
          @click="showWechatQr = !showWechatQr"
          class="mt-3 w-full text-center text-xs text-ink-mute hover:text-ink transition-colors cursor-pointer"
        >
          觉得有用？加作者微信交流学习
        </button>
        <img
          v-if="showWechatQr"
          src="/images/wechat_qr.png"
          alt="作者微信"
          class="mt-2 w-40 mx-auto rounded-xl border border-line"
        />
      </div>
    </Transition>

    <!-- Loading State -->
    <div v-if="!lessonData" class="flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-line border-t-ink rounded-full animate-spin"></div>
        <p class="text-sm font-bold text-ink-mute uppercase tracking-widest">Loading Lesson...</p>
      </div>
    </div>
    <!-- 快捷键操作反馈 Toast（1秒后淡出） -->
    <Transition name="toast">
      <div
        v-if="showToastNotification"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 pointer-events-none flex items-center gap-2 px-4 py-2 rounded-full bg-raised border border-line shadow-lg backdrop-blur-md"
      >
        <span class="w-2 h-2 rounded-full bg-accent"></span>
        <span class="text-xs font-bold text-ink tracking-wide">{{ toastText }}</span>
      </div>
    </Transition>

    <!-- 快捷键帮助浮层 -->
    <ShortcutHelp
      :visible="showShortcutHelp"
      @close="showShortcutHelp = false"
      @update:visible="showShortcutHelp = $event"
    />

    <DonationModal ref="donationModalRef" />
  </div>
</template>

<style scoped>
/* 快捷键提示 Toast 动画 */
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -8px);
}

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
  /* 跟随主题，不写死颜色（BRAND.md §配色） */
  background: var(--bg-base);
}
</style>
