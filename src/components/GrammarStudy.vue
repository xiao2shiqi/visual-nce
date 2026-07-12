<script setup lang="ts">
import { ref, computed, reactive, watch, onUnmounted } from 'vue';

interface Example { en: string; zh?: string; note?: string }
interface Section { heading: string; body: string; examples?: Example[] }
interface Exercise {
  type: 'fill' | 'choice' | 'order';
  prompt: string;
  answers?: string[];
  options?: string[];
  answer?: number;
  words?: string[];
  explain: string;
}
interface Topic {
  id: string;
  title: string;
  subtitle: string;
  refUnit: number;
  sections: Section[];
  exercises: Exercise[];
}

interface ExerciseState {
  checked: boolean;
  correct: boolean;
  fillInput: string;
  choiceIdx: number | null;
  orderChosen: number[]; // word indices in chosen order
}

const props = defineProps<{ lessonId: string }>();

const show = ref(false);
const note = ref('');
const topics = ref<Topic[]>([]);
const activeIdx = ref(0);

// 每题独立状态，key = `${topicId}:${exerciseIndex}`
const states = reactive<Record<string, ExerciseState>>({});

const modules = import.meta.glob('../data/grammar/*.json');

const open = async (refUnit?: number) => {
  if (!topics.value.length) {
    const loader = modules[`../data/grammar/${props.lessonId}.json`];
    if (!loader) return;
    const data = (await loader()) as any;
    note.value = data.default?.note ?? data.note ?? '';
    topics.value = (data.default?.topics ?? data.topics ?? []) as Topic[];
    topics.value.forEach((t) => {
      t.exercises.forEach((_, i) => {
        states[`${t.id}:${i}`] = { checked: false, correct: false, fillInput: '', choiceIdx: null, orderChosen: [] };
      });
    });
  }
  if (refUnit != null) {
    const idx = topics.value.findIndex((t) => t.refUnit === refUnit);
    if (idx >= 0) activeIdx.value = idx;
  }
  show.value = true;
};

const close = () => { show.value = false; };

// 弹窗打开时锁住背景页面滚动
watch(show, (v) => {
  document.body.style.overflow = v ? 'hidden' : '';
});
onUnmounted(() => {
  document.body.style.overflow = '';
});

defineExpose({ open });

const activeTopic = computed(() => topics.value[activeIdx.value]);

const stateOf = (i: number) => states[`${activeTopic.value.id}:${i}`];

const normalize = (s: string) =>
  s.trim().toLowerCase().replace(/[.!?,'’]/g, '').replace(/\s+/g, ' ');

const checkFill = (ex: Exercise, i: number) => {
  const st = stateOf(i);
  if (!st.fillInput.trim()) return;
  st.correct = (ex.answers || []).some((a) => normalize(a) === normalize(st.fillInput));
  st.checked = true;
};

const pickChoice = (ex: Exercise, i: number, optIdx: number) => {
  const st = stateOf(i);
  if (st.checked && st.correct) return;
  st.choiceIdx = optIdx;
  st.correct = optIdx === ex.answer;
  st.checked = true;
};

const pickWord = (i: number, wordIdx: number) => {
  const st = stateOf(i);
  if (st.checked && st.correct) return;
  if (!st.orderChosen.includes(wordIdx)) st.orderChosen.push(wordIdx);
  st.checked = false;
};

const unpickWord = (i: number, pos: number) => {
  const st = stateOf(i);
  if (st.checked && st.correct) return;
  st.orderChosen.splice(pos, 1);
  st.checked = false;
};

const checkOrder = (ex: Exercise, i: number) => {
  const st = stateOf(i);
  if (st.orderChosen.length !== (ex.words || []).length) return;
  const sentence = st.orderChosen.map((w) => ex.words![w]).join(' ');
  st.correct = (ex.answers || []).some((a) => normalize(a) === normalize(sentence));
  st.checked = true;
};

const resetOrder = (i: number) => {
  const st = stateOf(i);
  st.orderChosen = [];
  st.checked = false;
  st.correct = false;
};

// 填空题把 ___ 拆成前后两段，中间渲染输入框
const fillParts = (prompt: string) => prompt.split('___');

const doneCount = computed(() => {
  if (!activeTopic.value) return 0;
  return activeTopic.value.exercises.filter((_, i) => stateOf(i)?.checked && stateOf(i)?.correct).length;
});
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="close">
        <div class="bg-white w-full max-w-3xl max-h-[88vh] rounded-3xl shadow-2xl relative overflow-hidden animate-scale-up flex flex-col">

          <!-- Close -->
          <button @click="close" class="absolute top-4 right-4 z-10 p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Header + Tabs -->
          <div class="px-8 pt-8 pb-4 border-b border-slate-100">
            <div class="flex items-center gap-2 mb-1">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 text-amber-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
              </svg>
              <h2 class="text-lg font-black text-slate-800">课前语法预习</h2>
            </div>
            <p class="text-xs text-slate-400 font-medium mb-4">先懂语法，再听故事——听的时候你会「对上号」</p>
            <div class="flex gap-2">
              <button
                v-for="(t, i) in topics"
                :key="t.id"
                @click="activeIdx = i"
                class="px-4 py-2 rounded-xl text-sm font-bold transition-all border"
                :class="i === activeIdx
                  ? 'bg-amber-500 text-white border-amber-500 shadow-md shadow-amber-500/20'
                  : 'bg-white text-slate-500 border-slate-200 hover:border-amber-300 hover:text-amber-600'"
              >
                {{ t.title }}
              </button>
            </div>
          </div>

          <!-- Body -->
          <div v-if="activeTopic" class="overflow-y-auto overscroll-contain px-8 py-6 space-y-8">

            <!-- 讲解 -->
            <div>
              <div class="flex items-baseline gap-2 mb-4">
                <h3 class="text-base font-black text-slate-800">{{ activeTopic.title }}</h3>
                <span class="text-xs font-semibold text-slate-400">{{ activeTopic.subtitle }}</span>
              </div>

              <div class="space-y-5">
                <div v-for="(sec, si) in activeTopic.sections" :key="si">
                  <h4 class="text-sm font-bold text-slate-700 mb-1.5 flex items-center gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                    {{ sec.heading }}
                  </h4>
                  <p class="text-sm text-slate-600 leading-relaxed mb-2">{{ sec.body }}</p>
                  <div v-if="sec.examples?.length" class="space-y-1.5 pl-3.5">
                    <div v-for="(ex, ei) in sec.examples" :key="ei" class="text-sm bg-amber-50/60 border border-amber-100 rounded-lg px-3 py-2">
                      <span class="font-semibold text-slate-800">{{ ex.en }}</span>
                      <span v-if="ex.zh" class="text-slate-500 ml-2">{{ ex.zh }}</span>
                      <div v-if="ex.note" class="text-xs text-rose-500 font-medium mt-0.5">{{ ex.note }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 练习 -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-base font-black text-slate-800">随堂练习</h3>
                <span class="text-xs font-bold text-slate-400">答对 {{ doneCount }} / {{ activeTopic.exercises.length }}</span>
              </div>

              <div class="space-y-4">
                <div
                  v-for="(ex, i) in activeTopic.exercises"
                  :key="i"
                  class="rounded-2xl border p-4 transition-colors"
                  :class="stateOf(i).checked
                    ? (stateOf(i).correct ? 'border-emerald-200 bg-emerald-50/40' : 'border-rose-200 bg-rose-50/40')
                    : 'border-slate-200 bg-white'"
                >
                  <div class="flex items-start gap-2">
                    <span class="shrink-0 w-5 h-5 rounded-md bg-slate-100 text-slate-500 text-[11px] font-black flex items-center justify-center mt-0.5">{{ i + 1 }}</span>
                    <div class="flex-1 min-w-0">

                      <!-- fill -->
                      <template v-if="ex.type === 'fill'">
                        <p class="text-sm text-slate-700 leading-loose">
                          <template v-for="(part, pi) in fillParts(ex.prompt)" :key="pi">
                            <span>{{ part }}</span>
                            <input
                              v-if="pi < fillParts(ex.prompt).length - 1"
                              v-model="stateOf(i).fillInput"
                              @keyup.enter="checkFill(ex, i)"
                              :disabled="stateOf(i).checked && stateOf(i).correct"
                              type="text"
                              autocomplete="off"
                              class="inline-block w-28 mx-1 px-2 py-0.5 text-center text-sm font-bold border-b-2 border-slate-300 focus:border-amber-500 outline-none bg-transparent disabled:text-emerald-600"
                            />
                          </template>
                        </p>
                        <button
                          v-if="!(stateOf(i).checked && stateOf(i).correct)"
                          @click="checkFill(ex, i)"
                          class="mt-2 px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-white hover:bg-slate-700 transition-colors"
                        >检查</button>
                      </template>

                      <!-- choice -->
                      <template v-else-if="ex.type === 'choice'">
                        <p class="text-sm text-slate-700 mb-2.5">{{ ex.prompt }}</p>
                        <div class="flex flex-col gap-1.5">
                          <button
                            v-for="(opt, oi) in ex.options"
                            :key="oi"
                            @click="pickChoice(ex, i, oi)"
                            class="text-left px-3 py-2 rounded-xl text-sm font-medium border transition-all"
                            :class="[
                              stateOf(i).checked && oi === stateOf(i).choiceIdx
                                ? (stateOf(i).correct ? 'border-emerald-400 bg-emerald-50 text-emerald-700' : 'border-rose-400 bg-rose-50 text-rose-700')
                                : 'border-slate-200 hover:border-amber-300 hover:bg-amber-50/50 text-slate-600',
                              stateOf(i).checked && stateOf(i).correct && oi === ex.answer ? 'border-emerald-400 bg-emerald-50 text-emerald-700' : ''
                            ]"
                          >{{ opt }}</button>
                        </div>
                      </template>

                      <!-- order -->
                      <template v-else-if="ex.type === 'order'">
                        <p class="text-sm text-slate-700 mb-2.5">{{ ex.prompt }}</p>
                        <!-- 已选 -->
                        <div class="min-h-[2.5rem] flex flex-wrap items-center gap-1.5 px-3 py-2 mb-2 rounded-xl bg-slate-50 border border-dashed border-slate-300">
                          <span v-if="!stateOf(i).orderChosen.length" class="text-xs text-slate-400">点下面的词，按顺序组成句子</span>
                          <button
                            v-for="(wi, pos) in stateOf(i).orderChosen"
                            :key="pos"
                            @click="unpickWord(i, pos)"
                            class="px-2.5 py-1 rounded-lg text-sm font-bold bg-white border border-slate-300 text-slate-700 hover:border-rose-300 hover:text-rose-500 transition-colors"
                          >{{ ex.words![wi] }}</button>
                        </div>
                        <!-- 词库 -->
                        <div class="flex flex-wrap gap-1.5 mb-2">
                          <button
                            v-for="(w, wi) in ex.words"
                            :key="wi"
                            v-show="!stateOf(i).orderChosen.includes(wi)"
                            @click="pickWord(i, wi)"
                            class="px-2.5 py-1 rounded-lg text-sm font-bold bg-amber-50 border border-amber-200 text-amber-800 hover:bg-amber-100 transition-colors"
                          >{{ w }}</button>
                        </div>
                        <div class="flex gap-2">
                          <button
                            v-if="!(stateOf(i).checked && stateOf(i).correct)"
                            @click="checkOrder(ex, i)"
                            :disabled="stateOf(i).orderChosen.length !== ex.words!.length"
                            class="px-3 py-1 rounded-lg text-xs font-bold bg-slate-800 text-white hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                          >检查</button>
                          <button
                            v-if="stateOf(i).orderChosen.length && !(stateOf(i).checked && stateOf(i).correct)"
                            @click="resetOrder(i)"
                            class="px-3 py-1 rounded-lg text-xs font-bold bg-white border border-slate-200 text-slate-500 hover:border-slate-300 transition-colors"
                          >重来</button>
                        </div>
                      </template>

                      <!-- 判定与解析 -->
                      <div v-if="stateOf(i).checked" class="mt-2.5 text-xs leading-relaxed">
                        <p v-if="stateOf(i).correct" class="font-bold text-emerald-600">✓ 正确！</p>
                        <p v-else class="font-bold text-rose-500">✗ 不对，再想想</p>
                        <p v-if="stateOf(i).correct || (stateOf(i).checked && ex.type === 'choice')" class="text-slate-500 mt-1">{{ ex.explain }}</p>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 学完闭环 -->
            <div class="border-t border-slate-100 pt-5 space-y-4">
              <button
                v-if="activeIdx < topics.length - 1"
                @click="activeIdx++"
                class="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-2xl text-sm font-bold bg-amber-500 text-white hover:bg-amber-600 shadow-md shadow-amber-500/20 transition-all"
              >
                下一个语法点：{{ topics[activeIdx + 1].title }}
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </button>
              <button
                v-else
                @click="close"
                class="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-2xl text-sm font-bold bg-emerald-500 text-white hover:bg-emerald-600 shadow-md shadow-emerald-500/20 transition-all"
              >
                学完了，开始听课
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
                </svg>
              </button>
              <p class="text-[11px] text-slate-400 leading-relaxed">{{ note }}</p>
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
</style>
