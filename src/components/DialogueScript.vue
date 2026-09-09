<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import type { Segment } from '../types/lesson';

/**
 * DialogueScript 组件
 * 显示对话脚本，支持播放控制、翻译切换、盲听遮罩和点词查词典
 * @author xiaobin
 */

const props = withDefaults(defineProps<{
  segments: Segment[];
  activeSegmentId: string | null;
  playMode: 'continuous' | 'single' | 'repeat' | 'shadowing';
  playbackRate: number;
  showTranslation: boolean;
  blindMode: boolean;
  playbackRates: number[];
  isPlaying?: boolean;
}>(), {
  isPlaying: false
});

const emit = defineEmits([
  'update:playMode',
  'update:playbackRate',
  'update:showTranslation',
  'update:blindMode',
  'segmentClick'
]);

const handlePlayButtonClick = (s: Segment, event: Event) => {
  event.stopPropagation();
  resumeAutoScroll(false);
  emit('segmentClick', s);
};

// 盲听模式：已手动揭示的句子集合；切换课程或关闭盲听时重置
const revealedIds = ref(new Set<string>());

watch(() => props.segments, () => {
  revealedIds.value = new Set();
  resumeAutoScroll(false);
});
watch(() => props.blindMode, () => { revealedIds.value = new Set(); });

const isMasked = (s: Segment) => props.blindMode && !revealedIds.value.has(s.id);

const revealSegment = (s: Segment, event: Event) => {
  // 点击被遮罩的文字只揭示，不触发跳播
  event.stopPropagation();
  const next = new Set(revealedIds.value);
  next.add(s.id);
  revealedIds.value = next;
};

// 预定义的说话人颜色调色板（每个人一个独特颜色）
// 说话人标签一律中性灰，靠深浅区分出场顺序（配色原则：黑白灰为主，不用彩色做装饰）
const speakerColorPalette = [
  { bg: 'bg-hovered', text: 'text-ink' },
  { bg: 'bg-hovered', text: 'text-ink-soft' },
  { bg: 'bg-line-strong', text: 'text-ink' },
  { bg: 'bg-line-strong', text: 'text-ink-soft' },
  { bg: 'bg-hovered', text: 'text-ink-mute' },
  { bg: 'bg-line-strong', text: 'text-ink-mute' },
];

// 台词的角色名：数据里存于 role 字段（speaker 为历史字段，兼容读取）。
// Narrator（叙述/报课名）不显示标签，避免叙述课每行重复噪音。
const roleOf = (s: Segment): string | null => {
  const r = (s as any).speaker || (s as any).role;
  return r && r !== 'Narrator' ? r : null;
};

// 计算说话人与颜色的映射关系（按出场顺序分配）
const speakerColorMap = computed(() => {
  const map = new Map<string, { bg: string; text: string }>();
  let colorIndex = 0;

  for (const segment of props.segments) {
    const speaker = roleOf(segment);
    if (speaker && !map.has(speaker)) {
      map.set(speaker, speakerColorPalette[colorIndex % speakerColorPalette.length]!);
      colorIndex++;
    }
  }

  return map;
});

// 获取说话人的颜色类
const getSpeakerColorClass = (speaker: string): string => {
  const color = speakerColorMap.value.get(speaker);
  return color ? `${color.bg} ${color.text}` : 'bg-hovered text-ink-soft';
};


const copiedId = ref<string | null>(null);

// 把句子切成「单词 / 非单词」token，单词渲染成可点击查词的 span
const tokenize = (text: string) =>
  text.split(/([A-Za-z]+(?:[’'-][A-Za-z]+)*)/g).filter(t => t !== '');

const isWordToken = (t: string) => /^[A-Za-z]/.test(t);

// 查词：优先唤起本机欧路（eudic://），未安装时页面不会失焦，降级打开网页词典
const lookupWord = (word: string) => {
  const w = word.replace(/’/g, "'");
  window.location.href = `eudic://dict/${encodeURIComponent(w)}`;
  setTimeout(() => {
    if (document.hasFocus()) {
      window.open(`https://dict.eudic.net/dicts/en/${encodeURIComponent(w)}`, '_blank');
    }
  }, 1200);
};

const handleWordClick = (s: Segment, token: string, e: Event) => {
  // 盲听遮罩下不查词，让点击冒泡到外层做揭示
  if (isMasked(s)) return;
  e.stopPropagation();
  lookupWord(token);
};

const handleCopy = (segment: Segment, event: Event) => {
  event.stopPropagation();
  if (!segment.text) return;
  
  navigator.clipboard.writeText(segment.text).then(() => {
    copiedId.value = segment.id;
    setTimeout(() => {
      if (copiedId.value === segment.id) {
        copiedId.value = null;
      }
    }, 2000);
  });
};

// 滚动容器与自动滚动控制
const scrollContainerRef = ref<HTMLElement | null>(null);
const isAutoScrollPaused = ref(false);
const isCurrentOutOfView = ref(false);
const outOfViewDirection = ref<'up' | 'down'>('up');

let resumeTimer: number | null = null;
let isProgrammaticScrolling = false;
let programmaticScrollTimer: number | null = null;
let visibilityRafId: number | null = null;
const PAUSE_DURATION_MS = 5000;

// 检查当前活跃句子是否在滚动容器可视区内
const updateActiveVisibility = () => {
  if (!isAutoScrollPaused.value || !props.activeSegmentId || !scrollContainerRef.value) {
    isCurrentOutOfView.value = false;
    return;
  }

  const container = scrollContainerRef.value;
  const el = document.getElementById(`segment-${props.activeSegmentId}`);
  if (!el) {
    isCurrentOutOfView.value = false;
    return;
  }

  const containerRect = container.getBoundingClientRect();
  const elRect = el.getBoundingClientRect();

  // 当前句完全或大部分已滑出可视区上方
  if (elRect.bottom < containerRect.top + 16) {
    isCurrentOutOfView.value = true;
    outOfViewDirection.value = 'up';
  } else if (elRect.top > containerRect.bottom - 16) {
    // 当前句在可视区下方尚未进入
    isCurrentOutOfView.value = true;
    outOfViewDirection.value = 'down';
  } else {
    // 当前句依然在可视区域内
    isCurrentOutOfView.value = false;
  }
};

const scheduleVisibilityUpdate = () => {
  if (visibilityRafId !== null) return;
  visibilityRafId = requestAnimationFrame(() => {
    visibilityRafId = null;
    updateActiveVisibility();
  });
};

// 暂停自动滚动（用户手动操作触发）
const pauseAutoScroll = () => {
  isAutoScrollPaused.value = true;
  if (resumeTimer !== null) {
    clearTimeout(resumeTimer);
  }
  resumeTimer = window.setTimeout(() => {
    resumeAutoScroll(true);
  }, PAUSE_DURATION_MS);
};

// 恢复自动滚动
const resumeAutoScroll = (shouldScrollIfPlaying = true) => {
  isAutoScrollPaused.value = false;
  if (resumeTimer !== null) {
    clearTimeout(resumeTimer);
    resumeTimer = null;
  }
  isCurrentOutOfView.value = false;

  if (shouldScrollIfPlaying && props.isPlaying && props.activeSegmentId) {
    const el = document.getElementById(`segment-${props.activeSegmentId}`);
    if (el) {
      performProgrammaticScroll(el);
    }
  }
};

// 执行程序化平滑滚动，并标记 programmatic 状态以区分用户手动滚动
const performProgrammaticScroll = (el: HTMLElement) => {
  isProgrammaticScrolling = true;
  if (programmaticScrollTimer !== null) {
    clearTimeout(programmaticScrollTimer);
  }

  el.scrollIntoView({ behavior: 'smooth', block: 'center' });

  // 设置安全超时（平滑滚动通常在 300~600ms 内完成）
  programmaticScrollTimer = window.setTimeout(() => {
    isProgrammaticScrolling = false;
    programmaticScrollTimer = null;
    updateActiveVisibility();
  }, 800);
};

// 用户主动交互（鼠标滚轮、触摸滑动、拖动滚动条等）
const handleUserInteraction = () => {
  // 用户发生操作时，若正处于程序滚动的平滑动画中，立即打断并交还控制权
  if (isProgrammaticScrolling) {
    isProgrammaticScrolling = false;
    if (programmaticScrollTimer !== null) {
      clearTimeout(programmaticScrollTimer);
      programmaticScrollTimer = null;
    }
  }
  pauseAutoScroll();
};

// 监听键盘按键引起的滚动
const handleUserKeydown = (e: KeyboardEvent) => {
  const scrollKeys = ['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '];
  if (scrollKeys.includes(e.key)) {
    handleUserInteraction();
  }
};

// 容器滚动事件监听
const handleContainerScroll = () => {
  if (isProgrammaticScrolling) {
    // 程序引起的平滑滚动过程中：重置 debounce 计时器
    if (programmaticScrollTimer !== null) {
      clearTimeout(programmaticScrollTimer);
    }
    programmaticScrollTimer = window.setTimeout(() => {
      isProgrammaticScrolling = false;
      programmaticScrollTimer = null;
      updateActiveVisibility();
    }, 200);
    return;
  }

  // 非程序触发的滚动（如拖动滚动条等）
  pauseAutoScroll();
  scheduleVisibilityUpdate();
};

// 标准 scrollend 事件
const handleScrollEnd = () => {
  if (isProgrammaticScrolling) {
    isProgrammaticScrolling = false;
    if (programmaticScrollTimer !== null) {
      clearTimeout(programmaticScrollTimer);
      programmaticScrollTimer = null;
    }
    updateActiveVisibility();
  }
};

// 点击卡片：用户主动选择某一句，立即恢复自动滚动
const handleCardClick = (s: Segment) => {
  resumeAutoScroll(false);
  emit('segmentClick', s);
};

// 点击回到当前句按钮
const handleBackToActive = () => {
  if (props.activeSegmentId) {
    isAutoScrollPaused.value = false;
    if (resumeTimer !== null) {
      clearTimeout(resumeTimer);
      resumeTimer = null;
    }
    isCurrentOutOfView.value = false;
    const el = document.getElementById(`segment-${props.activeSegmentId}`);
    if (el) {
      performProgrammaticScroll(el);
    }
  }
};

const scrollToActive = (id: string) => {
  if (isAutoScrollPaused.value) {
    // 用户手动滚动暂停期间，不强行把视口拽回，仅更新提示状态
    nextTick(() => {
      updateActiveVisibility();
    });
    return;
  }

  const el = document.getElementById(`segment-${id}`);
  if (el) {
    performProgrammaticScroll(el);
  }
};

// 监听活跃片段变化，在暂停期间动态刷新提示显隐及方向
watch(() => props.activeSegmentId, () => {
  if (isAutoScrollPaused.value) {
    nextTick(() => {
      updateActiveVisibility();
    });
  }
});

onMounted(() => {
  const container = scrollContainerRef.value;
  if (container) {
    container.addEventListener('wheel', handleUserInteraction, { passive: true });
    container.addEventListener('pointerdown', handleUserInteraction, { passive: true });
    container.addEventListener('touchstart', handleUserInteraction, { passive: true });
    container.addEventListener('keydown', handleUserKeydown, { passive: true });
    container.addEventListener('scroll', handleContainerScroll, { passive: true });
    container.addEventListener('scrollend', handleScrollEnd);
  }
});

onUnmounted(() => {
  if (visibilityRafId !== null) {
    cancelAnimationFrame(visibilityRafId);
    visibilityRafId = null;
  }
  if (resumeTimer !== null) {
    clearTimeout(resumeTimer);
    resumeTimer = null;
  }
  if (programmaticScrollTimer !== null) {
    clearTimeout(programmaticScrollTimer);
    programmaticScrollTimer = null;
  }
  const container = scrollContainerRef.value;
  if (container) {
    container.removeEventListener('wheel', handleUserInteraction);
    container.removeEventListener('pointerdown', handleUserInteraction);
    container.removeEventListener('touchstart', handleUserInteraction);
    container.removeEventListener('keydown', handleUserKeydown);
    container.removeEventListener('scroll', handleContainerScroll);
    container.removeEventListener('scrollend', handleScrollEnd);
  }
});

defineExpose({
  scrollToActive
});
</script>

<template>
  <div class="col-span-7">
    <!-- Section Title & Controls: 单行布局，高频的播放模式用分段控件，低频设置降级为小图标 -->
    <div class="flex flex-row items-center justify-between gap-3 mb-4">
      <div class="flex items-baseline gap-2 whitespace-nowrap min-w-0">
        <h2 class="text-sm font-bold text-ink uppercase tracking-wide">Dialogue Script</h2>
        <span class="text-[11px] text-ink-mute font-medium truncate">点击单词查欧路词典</span>
      </div>

      <div class="flex items-center gap-2">
        <!-- Play Mode Toggle (高频操作，保留分段控件) -->
        <div class="flex items-center bg-hovered p-0.5 rounded-md border border-line">
          <button
            @click="emit('update:playMode', 'continuous')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'continuous' ? 'bg-raised text-ink shadow-sm' : 'text-ink-mute hover:text-ink-soft'"
          >
            连读
          </button>
          <button
            @click="emit('update:playMode', 'single')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'single' ? 'bg-raised text-ink shadow-sm' : 'text-ink-mute hover:text-ink-soft'"
          >
            点读
          </button>
          <button
            @click="emit('update:playMode', 'repeat')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'repeat' ? 'bg-raised text-ink shadow-sm' : 'text-ink-mute hover:text-ink-soft'"
          >
            循环
          </button>
          <button
            @click="emit('update:playMode', 'shadowing')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'shadowing' ? 'bg-raised text-ink shadow-sm' : 'text-ink-mute hover:text-ink-soft'"
            title="每句播完自动停顿，留出开口跟读的时间"
          >
            跟读
          </button>
        </div>

        <div class="w-px h-5 bg-line-strong"></div>

        <!-- Blind Listening (低频设置，图标按钮) -->
        <button
          @click="emit('update:blindMode', !blindMode)"
          class="w-8 h-8 rounded-md flex items-center justify-center transition-all duration-200"
          :class="blindMode ? 'bg-hovered text-ink' : 'text-ink-mute hover:text-ink-soft hover:bg-hovered'"
          title="盲听模式：隐藏字幕，先听后看；点击句子文字可单独揭示"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
            <path v-if="blindMode" stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
            <template v-else>
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </template>
          </svg>
        </button>

        <!-- Speed Selector (低频设置，无边框下拉) -->
        <select
          :value="playbackRate"
          @change="(e) => emit('update:playbackRate', parseFloat((e.target as HTMLSelectElement).value))"
          class="appearance-none bg-transparent h-8 px-1.5 text-xs font-bold text-ink-mute hover:text-ink rounded-md hover:bg-hovered transition-all cursor-pointer outline-none"
          title="播放速度"
        >
          <option v-for="rate in playbackRates" :key="rate" :value="rate">
            {{ rate === 1.0 ? '1.0x' : rate + 'x' }}
          </option>
        </select>

        <!-- Translation Toggle (低频设置，图标按钮) -->
        <button
          @click="emit('update:showTranslation', !showTranslation)"
          class="w-8 h-8 rounded-md flex items-center justify-center text-xs font-bold transition-all duration-200"
          :class="showTranslation ? 'bg-hovered text-ink' : 'text-ink-mute hover:text-ink-soft hover:bg-hovered'"
          title="显示中文译文"
        >
          中
        </button>
      </div>
    </div>

    <!-- Script Cards Container -->
    <div class="relative">
      <div 
        ref="scrollContainerRef"
        class="max-h-[620px] overflow-y-auto px-1.5 py-1 pr-3.5 -mr-3.5 space-y-2.5"
      >
        <div 
          v-for="s in segments" 
          :key="s.id"
          :id="`segment-${s.id}`"
          class="script-card group relative cursor-pointer"
          @click="handleCardClick(s)"
        >
        <div 
          class="relative p-3.5 rounded-xl transition-all duration-300 border flex items-start gap-3"
          :class="[
            activeSegmentId === s.id
              ? 'bg-raised border-accent ring-2 ring-accent/30 shadow-md shadow-accent/10'
              : 'bg-raised border-transparent hover:bg-raised hover:shadow-lg hover:border-line'
          ]"
        >
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p 
                class="text-sm leading-relaxed transition-colors duration-300"
                :class="activeSegmentId === s.id ? 'text-ink font-semibold' : 'text-ink-soft'"
              >
                <span
                  v-if="roleOf(s)"
                  class="inline-block mr-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase shadow-sm select-none"
                  :class="getSpeakerColorClass(roleOf(s)!)"
                >
                  {{ roleOf(s) }}
                </span>
                <span
                  :class="isMasked(s) ? 'blur-[6px] select-none cursor-help transition-all duration-300' : 'transition-all duration-300'"
                  :title="isMasked(s) ? '点击揭示这句' : undefined"
                  @click="isMasked(s) && revealSegment(s, $event)"
                ><template v-for="(t, i) in tokenize(s.text)" :key="i"><span
                    v-if="isWordToken(t)"
                    :class="isMasked(s) ? undefined : 'lookup-word'"
                    :title="isMasked(s) ? undefined : `查词典：${t}`"
                    @click="handleWordClick(s, t, $event)"
                  >{{ t }}</span><template v-else>{{ t }}</template></template></span>
              </p>
              <p
                v-if="showTranslation && !isMasked(s)"
                class="text-[11px] mt-1 text-ink-mute font-medium leading-relaxed animate-fade-in"
              >
                {{ s.translation }}</p>
            </div>
            
            <!-- Copy Button -->
            <button 
              @click="handleCopy(s, $event)"
              class="flex-shrink-0 w-8 h-8 rounded-md flex items-center justify-center transition-all duration-300 hover:bg-hovered group/copy"
              :class="[copiedId === s.id ? 'text-green-500' : 'text-ink-mute opacity-0 group-hover:opacity-100 group-hover:text-ink-mute']"
              title="复制句子"
            >
              <svg v-if="copiedId !== s.id" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </button>

            <!-- Play Button / Indicator -->
            <button 
              v-if="s.startTime !== undefined"
              type="button"
              @click="handlePlayButtonClick(s, $event)"
              :title="activeSegmentId === s.id && isPlaying ? '暂停' : '播放此句'"
              class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center transition-all duration-300 cursor-pointer shadow-sm active:scale-95 group/playbtn"
              :class="[
                activeSegmentId === s.id
                  ? 'bg-accent text-white shadow-accent/25 ring-2 ring-accent/30'
                  : 'bg-hovered text-ink-mute opacity-0 group-hover:opacity-100 hover:bg-accent/10 hover:text-accent'
              ]"
            >
              <!-- If active AND is playing: show equalizer animation, and show pause on hover -->
              <template v-if="activeSegmentId === s.id && isPlaying">
                <div class="flex gap-0.5 items-end h-3 group-hover/playbtn:hidden">
                  <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_infinite]"></div>
                  <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.2s_infinite]"></div>
                  <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.4s_infinite]"></div>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5 hidden group-hover/playbtn:block">
                  <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
                </svg>
              </template>
              <!-- If not active OR paused: show play arrow -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5 ml-0.5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Floating "Back to Current" button -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 translate-y-2 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0 scale-100"
        leave-to-class="opacity-0 translate-y-2 scale-95"
      >
        <button
          v-if="isAutoScrollPaused && isCurrentOutOfView"
          type="button"
          @click="handleBackToActive"
          class="absolute bottom-3 left-1/2 -translate-x-1/2 z-10 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-raised/95 backdrop-blur-md border border-line shadow-lg hover:border-line-strong hover:bg-hovered text-xs font-semibold text-ink cursor-pointer transition-all duration-200 select-none group"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-accent animate-pulse"></span>
          <svg
            v-if="outOfViewDirection === 'up'"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2.5"
            stroke="currentColor"
            class="w-3.5 h-3.5 text-accent transition-transform group-hover:-translate-y-0.5"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" />
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2.5"
            stroke="currentColor"
            class="w-3.5 h-3.5 text-accent transition-transform group-hover:translate-y-0.5"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
          </svg>
          <span>回到当前句</span>
        </button>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.script-card {
  -webkit-tap-highlight-color: transparent;
}
/* 可查词的单词：悬停句子时全句单词浮现浅虚线（提示可点），
   悬停单词本身时琥珀色高亮 + 加深虚线 */
.lookup-word {
  cursor: pointer;
  border-bottom: 1px dotted transparent;
  border-radius: 2px;
  transition: color 0.2s, background-color 0.2s, border-color 0.2s;
}
.script-card:hover .lookup-word {
  border-bottom-color: #cbd5e1; /* zinc-300 */
}
.lookup-word:hover {
  color: #b45309;               /* amber-700 */
  background-color: rgb(254 243 199 / 0.7); /* amber-100/70 */
  border-bottom-color: #d97706; /* amber-600 */
}
@keyframes eq {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
