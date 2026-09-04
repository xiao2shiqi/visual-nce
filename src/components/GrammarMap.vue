<script setup lang="ts">
import { computed, ref } from 'vue';
import grammarMap from '../data/grammar-map.json';
import GrammarStudy from './GrammarStudy.vue';
import InfoTip from './InfoTip.vue';

const props = defineProps<{
  lessonId: string;
}>();

// 有原创讲练数据的课，Unit 徽章可点击直接学
const studyModules = import.meta.glob('../data/grammar/*.json');
const hasStudy = computed(() => `../data/grammar/${props.lessonId}.json` in studyModules);
const studyRef = ref<InstanceType<typeof GrammarStudy> | null>(null);

// 供学习动线步骤条直接打开预习弹窗
defineExpose({ openStudy: () => studyRef.value?.open() });

type BookId = 'elem' | 'int';

interface GrammarRef {
  unit: number;
  title: string;
}

interface GrammarPoint {
  point: string;
  refs: GrammarRef[];
}

const books = grammarMap.books as Record<BookId, { name: string; edition: string; en: string }>;

// NCE1 只对应剑桥初级英语语法，NCE2 只对应剑桥中级英语语法
const bookId = computed<BookId>(() => (props.lessonId.startsWith('nce1') ? 'elem' : 'int'));
const book = computed(() => books[bookId.value]);

const points = computed<GrammarPoint[]>(() => {
  const raw = (grammarMap.lessons as Record<string, any[]>)[props.lessonId];
  if (!raw) return [];
  return raw.map((p) => ({
    point: p.point,
    refs: (p.refs[bookId.value] || []).map((unit: number) => ({
      unit,
      title: (grammarMap.unitTitles as Record<BookId, Record<string, string>>)[bookId.value][String(unit)] || ''
    }))
  }));
});
</script>

<template>
  <!-- 紧凑侧栏卡片：放在播放器下方，作为学完后的延伸阅读 -->
  <section v-if="points.length" class="mt-5 pt-4 border-t border-line animate-fade-in">
    <div class="flex items-center gap-1.5 mb-3">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-ink-mute">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
      </svg>
      <span class="text-[10px] font-black text-ink-mute uppercase tracking-widest">{{ hasStudy ? '课前语法预习' : '本课语法地图' }}</span>
      <InfoTip
        :text="hasStudy
          ? `听课前先花 3 分钟看完讲解，听课文时你会「对上号」。讲解为本站原创编写；想系统深入，可翻《${book.name}》（${book.edition}）对应 Unit。`
          : `学完本课后，可翻到《${book.name}》（${book.edition}）对应 Unit 做配套练习。`"
      />
    </div>

    <div class="space-y-3">
      <div v-for="(p, i) in points" :key="i">
        <h3 class="text-xs font-bold text-ink-soft mb-1.5 leading-relaxed">{{ p.point }}</h3>
        <div class="flex flex-wrap gap-1.5">
          <component
            :is="hasStudy ? 'button' : 'span'"
            v-for="ref in p.refs"
            :key="ref.unit"
            class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold border bg-hovered text-ink-soft border-line"
            :class="hasStudy ? 'cursor-pointer hover:bg-hovered hover:border-line-strong hover:shadow-sm transition-all' : ''"
            :title="hasStudy ? '点击看本课语法讲解' : `${book.name}（${book.edition}）Unit ${ref.unit}`"
            @click="hasStudy && studyRef?.open(ref.unit)"
          >
            <span class="font-black">Unit {{ ref.unit }}</span>
            <span class="opacity-70 font-medium">{{ ref.title }}</span>
            <svg v-if="hasStudy" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-2.5 h-2.5 opacity-60">
              <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
            </svg>
          </component>
        </div>
      </div>
    </div>

    <button
      v-if="hasStudy"
      @click="studyRef?.open()"
      class="mt-3 w-full flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold bg-btn text-btn-fg shadow-md shadow-zinc-900/15 transition-all"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
      </svg>
      先学语法，再听故事
    </button>

    <GrammarStudy ref="studyRef" :lesson-id="lessonId" />
  </section>
</template>
