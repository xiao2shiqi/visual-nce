<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue';

interface Segment {
  id: string;
  text: string;
  translation?: string;
  startTime?: number;
  endTime?: number;
}

interface Item {
  seg: Segment;
  words: string[];      // 原句分词（含标点，按空格切）
  shuffled: number[];   // 词库展示顺序（索引）
}

type ItemStatus = 'pending' | 'correct' | 'revealed';

const props = defineProps<{
  lessonTitle: string;
  segments: Segment[];
}>();

const emit = defineEmits<{
  (e: 'replay-segment', seg: Segment): void;
}>();

// ---- 出题：课文正句，剔除课号/标题/听前指令/听前问题等元信息 ----
const normalize = (s: string) => s.trim().toLowerCase().replace(/[^a-z ]/g, '').replace(/\s+/g, ' ');

const challengeSegments = computed<Segment[]>(() => {
  const titlePart = normalize(props.lessonTitle.replace(/^lesson \d+:\s*/i, ''));
  const listenIdx = props.segments.findIndex((s) => /^listen to the tape/i.test(s.text.trim()));
  return props.segments.filter((s, i) => {
    const t = s.text.trim();
    if (!s.translation) return false;
    if (t.split(/\s+/).length < 2) return false;
    if (/^lesson \d+$/i.test(t)) return false;
    if (/^listen to the tape/i.test(t)) return false;
    if (normalize(t) === titlePart) return false;
    if (listenIdx !== -1 && i === listenIdx + 1) return false; // 听前理解问题
    return true;
  });
});

const shuffle = (n: number): number[] => {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = arr[i]!;
    arr[i] = arr[j]!;
    arr[j] = tmp;
  }
  return arr;
};

const buildItems = (): Item[] =>
  challengeSegments.value.map((seg) => {
    const words = seg.text.trim().split(/\s+/);
    let shuffled = shuffle(words.length);
    // 避免一上来就是正确顺序
    let guard = 0;
    while (words.length > 2 && shuffled.every((v, i) => words[v] === words[i]) && guard++ < 10) {
      shuffled = shuffle(words.length);
    }
    return { seg, words, shuffled };
  });

// ---- 挑战状态 ----
const show = ref(false);
const items = ref<Item[]>([]);
const cur = ref(0);
const finished = ref(false);
const chosen = ref<number[]>([]);
const status = ref<ItemStatus[]>([]);
const wrongFlash = ref(false);

const open = () => {
  items.value = buildItems();
  status.value = items.value.map(() => 'pending');
  cur.value = 0;
  chosen.value = [];
  finished.value = false;
  show.value = true;
};

const close = () => { show.value = false; };

watch(show, (v) => { document.body.style.overflow = v ? 'hidden' : ''; });
onUnmounted(() => { document.body.style.overflow = ''; });

defineExpose({ open });

const item = computed(() => items.value[cur.value]);
const curStatus = computed(() => status.value[cur.value]);

const sentence = (it: Item, indices: number[]) => indices.map((i) => it.words[i]).join(' ');

const pick = (wi: number) => {
  if (curStatus.value !== 'pending' || chosen.value.includes(wi)) return;
  const it = item.value;
  if (!it) return;
  chosen.value.push(wi);
  // 拼满自动判定（按词序列比对，重复词等价）
  if (chosen.value.length === it.words.length) {
    if (sentence(it, chosen.value) === it.words.join(' ')) {
      status.value[cur.value] = 'correct';
    } else {
      wrongFlash.value = true;
      setTimeout(() => { wrongFlash.value = false; }, 600);
    }
  }
};

const unpick = (pos: number) => {
  if (curStatus.value !== 'pending') return;
  chosen.value.splice(pos, 1);
};

const reveal = () => {
  if (curStatus.value !== 'pending') return;
  status.value[cur.value] = 'revealed';
};

const next = () => {
  if (cur.value < items.value.length - 1) {
    cur.value++;
    chosen.value = [];
  } else {
    finished.value = true;
  }
};

const retry = () => { open(); };

const correctCount = computed(() => status.value.filter((s) => s === 'correct').length);
const failedItems = computed(() => items.value.filter((_, i) => status.value[i] === 'revealed'));

const replay = (seg: Segment) => {
  close();
  // 等弹窗淡出动画（0.3s）结束再触发音频跳转，
  // 否则父组件在离场过渡期间重渲染会卡住 Transition 的移除
  setTimeout(() => emit('replay-segment', seg), 350);
};

defineOptions({ inheritAttrs: false });
</script>

<template>
  <!-- 入口按钮（放在语法预习卡片下方） -->
  <button
    v-if="challengeSegments.length"
    v-bind="$attrs"
    @click="open"
    class="mt-3 w-full flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition-all bg-emerald-500 text-white hover:bg-emerald-600 shadow-md shadow-emerald-500/20"
  >
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
    </svg>
    回译挑战：看中文，说英文
  </button>

  <Teleport to="body">
    <Transition name="fade" :duration="200">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="close">
        <div class="bg-white w-full max-w-2xl max-h-[88vh] rounded-3xl shadow-2xl relative overflow-hidden animate-scale-up flex flex-col">

          <button @click="close" class="absolute top-4 right-4 z-10 p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Header -->
          <div class="px-8 pt-8 pb-4 border-b border-slate-100">
            <div class="flex items-center gap-2 mb-1">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 text-emerald-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
              </svg>
              <h2 class="text-lg font-black text-slate-800">回译挑战</h2>
            </div>
            <p class="text-xs text-slate-400 font-medium">看中文，把英文原句拼回来——选做的练习，不计成绩，也不影响本课的完成标记</p>
            <!-- 进度条 -->
            <div v-if="!finished" class="mt-4 flex items-center gap-3">
              <div class="flex-1 h-1.5 rounded-full bg-slate-100 overflow-hidden">
                <div class="h-full rounded-full bg-emerald-500 transition-all duration-500" :style="{ width: `${(cur + (curStatus !== 'pending' ? 1 : 0)) / items.length * 100}%` }"></div>
              </div>
              <span class="text-xs font-black text-slate-400 tabular-nums">{{ cur + 1 }} / {{ items.length }}</span>
            </div>
          </div>

          <!-- 挑战中 -->
          <div v-if="!finished && item" class="overflow-y-auto overscroll-contain px-8 py-6">
            <!-- 中文题面 -->
            <p class="text-base font-bold text-slate-800 mb-4">{{ item.seg.translation }}</p>

            <!-- 已拼句子 -->
            <div
              class="min-h-[3.5rem] flex flex-wrap items-center gap-1.5 px-3 py-2.5 mb-3 rounded-2xl border-2 border-dashed transition-colors"
              :class="wrongFlash ? 'border-rose-300 bg-rose-50/50 animate-shake'
                : curStatus === 'correct' ? 'border-emerald-300 bg-emerald-50/50'
                : 'border-slate-200 bg-slate-50'"
            >
              <span v-if="!chosen.length && curStatus === 'pending'" class="text-xs text-slate-400">点下面的词，按顺序拼出英文原句</span>
              <template v-if="curStatus !== 'revealed'">
                <button
                  v-for="(wi, pos) in chosen"
                  :key="pos"
                  @click="unpick(pos)"
                  :disabled="curStatus === 'correct'"
                  class="px-2.5 py-1 rounded-lg text-sm font-bold border transition-colors"
                  :class="curStatus === 'correct'
                    ? 'bg-white border-emerald-200 text-emerald-700'
                    : 'bg-white border-slate-300 text-slate-700 hover:border-rose-300 hover:text-rose-500'"
                >{{ item.words[wi] }}</button>
              </template>
              <span v-else class="text-sm font-bold text-slate-700">{{ item.seg.text }}</span>
            </div>

            <!-- 词库 -->
            <div v-if="curStatus === 'pending'" class="flex flex-wrap gap-1.5 mb-4">
              <button
                v-for="wi in item.shuffled"
                :key="wi"
                v-show="!chosen.includes(wi)"
                @click="pick(wi)"
                class="px-2.5 py-1 rounded-lg text-sm font-bold bg-emerald-50 border border-emerald-200 text-emerald-800 hover:bg-emerald-100 transition-colors"
              >{{ item.words[wi] }}</button>
            </div>

            <!-- 判定反馈 -->
            <div v-if="curStatus === 'correct'" class="mb-4 text-sm">
              <p class="font-bold text-emerald-600">✓ 拼对了！</p>
              <p class="text-slate-500 mt-1">{{ item.seg.text }}</p>
            </div>
            <div v-else-if="curStatus === 'revealed'" class="mb-4 text-sm">
              <p class="font-bold text-slate-400">原句已揭晓——这句先记下，结束后回去多听几遍</p>
            </div>
            <p v-else-if="wrongFlash" class="mb-4 text-sm font-bold text-rose-500">✗ 顺序不对，点亮红的词块拆回来调整</p>

            <!-- 操作 -->
            <div class="flex gap-2">
              <button
                v-if="curStatus !== 'pending'"
                @click="next"
                class="px-5 py-2 rounded-xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 shadow-md shadow-emerald-500/20 transition-all"
              >{{ cur < items.length - 1 ? '下一句' : '看结果' }}</button>
              <button
                v-if="curStatus === 'pending'"
                @click="reveal"
                class="px-4 py-2 rounded-xl text-sm font-bold bg-white border border-slate-200 text-slate-400 hover:border-slate-300 hover:text-slate-600 transition-colors"
              >拼不出来，看答案</button>
            </div>
          </div>

          <!-- 结果页 -->
          <div v-else-if="finished" class="overflow-y-auto overscroll-contain px-8 py-6">
            <div class="text-center py-4">
              <div class="text-5xl font-black mb-2" :class="correctCount === items.length ? 'text-emerald-500' : 'text-slate-700'">
                {{ correctCount }} <span class="text-2xl text-slate-300">/ {{ items.length }}</span>
              </div>
              <p v-if="correctCount === items.length" class="text-sm font-bold text-emerald-600">
                全部独立重构 ✓
              </p>
              <p v-else class="text-sm font-medium text-slate-500">
                还有 {{ items.length - correctCount }} 句没拼出来——回去把这几句多听几遍，再来一次
              </p>
            </div>

            <!-- 未通过的句子 -->
            <div v-if="failedItems.length" class="space-y-2 mt-4">
              <div
                v-for="f in failedItems"
                :key="f.seg.id"
                class="flex items-center justify-between gap-3 rounded-2xl border border-slate-200 px-4 py-3"
              >
                <div class="min-w-0">
                  <p class="text-sm font-bold text-slate-700 truncate">{{ f.seg.text }}</p>
                  <p class="text-xs text-slate-400 truncate">{{ f.seg.translation }}</p>
                </div>
                <button
                  @click="replay(f.seg)"
                  class="shrink-0 flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-50 border border-amber-200 text-amber-700 hover:bg-amber-100 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
                  </svg>
                  回去听这句
                </button>
              </div>
            </div>

            <div class="flex gap-2 justify-center mt-6">
              <button @click="retry" class="px-5 py-2 rounded-xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 shadow-md shadow-emerald-500/20 transition-all">再来一次</button>
              <button @click="close" class="px-5 py-2 rounded-xl text-sm font-bold bg-white border border-slate-200 text-slate-500 hover:border-slate-300 transition-colors">完成</button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.animate-scale-up {
  animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-shake {
  animation: shake 0.5s;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
</style>
