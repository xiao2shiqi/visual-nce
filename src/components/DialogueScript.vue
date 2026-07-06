<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { Segment } from '../types/lesson';

/**
 * DialogueScript 组件
 * 显示对话脚本，支持播放控制、翻译切换、盲听遮罩和点词查词典
 * @author xiaobin
 */

const props = defineProps<{
  segments: Segment[];
  activeSegmentId: string | null;
  playMode: 'continuous' | 'single' | 'repeat' | 'shadowing';
  playbackRate: number;
  showTranslation: boolean;
  blindMode: boolean;
  playbackRates: number[];
}>();

const emit = defineEmits([
  'update:playMode',
  'update:playbackRate',
  'update:showTranslation',
  'update:blindMode',
  'segmentClick'
]);

// 盲听模式：已手动揭示的句子集合；切换课程或关闭盲听时重置
const revealedIds = ref(new Set<string>());

watch(() => props.segments, () => { revealedIds.value = new Set(); });
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
const speakerColorPalette = [
  { bg: 'bg-blue-100', text: 'text-blue-600' },      // 第1个说话人
  { bg: 'bg-rose-100', text: 'text-rose-600' },      // 第2个说话人
  { bg: 'bg-emerald-100', text: 'text-emerald-600' },// 第3个说话人
  { bg: 'bg-violet-100', text: 'text-violet-600' },  // 第4个说话人
  { bg: 'bg-amber-100', text: 'text-amber-600' },    // 第5个说话人
  { bg: 'bg-cyan-100', text: 'text-cyan-600' },      // 第6个说话人
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
  return color ? `${color.bg} ${color.text}` : 'bg-slate-100 text-slate-500';
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

const scrollToActive = (id: string) => {
  const el = document.getElementById(`segment-${id}`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};

defineExpose({
  scrollToActive
});
</script>

<template>
  <div class="col-span-7">
    <!-- Section Title & Controls: 单行布局，高频的播放模式用分段控件，低频设置降级为小图标 -->
    <div class="flex flex-row items-center justify-between gap-3 mb-4">
      <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide whitespace-nowrap">Dialogue Script</h2>

      <div class="flex items-center gap-2">
        <!-- Play Mode Toggle (高频操作，保留分段控件) -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <button
            @click="emit('update:playMode', 'continuous')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'continuous' ? 'bg-white text-amber-700 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            连读
          </button>
          <button
            @click="emit('update:playMode', 'single')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'single' ? 'bg-white text-amber-700 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            点读
          </button>
          <button
            @click="emit('update:playMode', 'repeat')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'repeat' ? 'bg-white text-amber-700 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            循环
          </button>
          <button
            @click="emit('update:playMode', 'shadowing')"
            class="px-2.5 py-1.5 text-xs font-bold rounded-md transition-all duration-200"
            :class="playMode === 'shadowing' ? 'bg-white text-amber-700 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
            title="每句播完自动停顿，留出开口跟读的时间"
          >
            跟读
          </button>
        </div>

        <div class="w-px h-5 bg-gray-200"></div>

        <!-- Blind Listening (低频设置，图标按钮) -->
        <button
          @click="emit('update:blindMode', !blindMode)"
          class="w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-200"
          :class="blindMode ? 'bg-amber-50 text-amber-700' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'"
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
          class="appearance-none bg-transparent h-8 px-1.5 text-xs font-bold text-gray-400 hover:text-amber-700 rounded-lg hover:bg-gray-100 transition-all cursor-pointer outline-none"
          title="播放速度"
        >
          <option v-for="rate in playbackRates" :key="rate" :value="rate">
            {{ rate === 1.0 ? '1.0x' : rate + 'x' }}
          </option>
        </select>

        <!-- Translation Toggle (低频设置，图标按钮) -->
        <button
          @click="emit('update:showTranslation', !showTranslation)"
          class="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold transition-all duration-200"
          :class="showTranslation ? 'bg-amber-50 text-amber-700' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'"
          title="显示中文译文"
        >
          中
        </button>
      </div>
    </div>

    <!-- Script Cards -->
    <div class="max-h-[620px] overflow-y-auto pr-4 -mr-4 space-y-2.5">
      <div 
        v-for="s in segments" 
        :key="s.id"
        :id="`segment-${s.id}`"
        class="script-card group relative cursor-pointer"
        @click="emit('segmentClick', s)"
      >
        <div 
          class="relative p-3.5 rounded-xl transition-all duration-300 border flex items-start gap-3"
          :class="[
            activeSegmentId === s.id 
              ? 'bg-white shadow-xl shadow-amber-500/5 border-amber-100 scale-[1.01]' 
              : 'bg-white/50 border-transparent hover:bg-white hover:shadow-lg hover:border-gray-100'
          ]"
        >
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <p 
                class="text-sm leading-relaxed transition-colors duration-300"
                :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-600'"
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
                    class="cursor-pointer rounded-sm transition-colors hover:text-amber-700 hover:bg-amber-100/70"
                    :title="isMasked(s) ? undefined : `查词典：${t}`"
                    @click="handleWordClick(s, t, $event)"
                  >{{ t }}</span><template v-else>{{ t }}</template></template></span>
              </p>
              <p
                v-if="showTranslation && !isMasked(s)"
                class="text-[11px] mt-1 text-gray-400 font-medium leading-relaxed animate-fade-in"
              >
                {{ s.translation }}</p>
            </div>
            
            <!-- Copy Button -->
            <button 
              @click="handleCopy(s, $event)"
              class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300 hover:bg-amber-50 group/copy"
              :class="[copiedId === s.id ? 'text-green-500' : 'text-slate-300 opacity-0 group-hover:opacity-100 group-hover:text-amber-500']"
              title="复制句子"
            >
              <svg v-if="copiedId !== s.id" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </button>

            <!-- Play Indicator -->
            <div 
              v-if="s.startTime !== undefined"
              class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center transition-all duration-300"
              :class="activeSegmentId === s.id ? 'bg-amber-600 text-white' : 'bg-gray-100 text-gray-400 opacity-0 group-hover:opacity-100'"
            >
              <svg v-if="activeSegmentId !== s.id" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
              <div v-else class="flex gap-0.5 items-end h-3">
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.2s_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.4s_infinite]"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.script-card {
  -webkit-tap-highlight-color: transparent;
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
