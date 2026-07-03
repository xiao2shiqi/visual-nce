<script setup lang="ts">
import { computed } from 'vue';
import grammarMap from '../data/grammar-map.json';

const props = defineProps<{
  lessonId: string;
}>();

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
  <section v-if="points.length" class="mt-5 pt-4 border-t border-slate-200/60 animate-fade-in">
    <div class="flex items-center gap-2 mb-3">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3 text-amber-500">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
      </svg>
      <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">本课语法地图</span>
    </div>

    <div class="space-y-3">
      <div v-for="(p, i) in points" :key="i">
        <h3 class="text-xs font-bold text-slate-700 mb-1.5 leading-relaxed">{{ p.point }}</h3>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="ref in p.refs"
            :key="ref.unit"
            class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold border bg-amber-50 text-amber-800 border-amber-200/70"
            :title="`${book.name}（${book.edition}）Unit ${ref.unit}`"
          >
            <span class="font-black">Unit {{ ref.unit }}</span>
            <span class="opacity-70 font-medium">{{ ref.title }}</span>
          </span>
        </div>
      </div>
    </div>

    <p class="mt-3 text-[10px] text-slate-400 leading-relaxed">
      学完本课后，可翻到《{{ book.name }}》（{{ book.edition }}）对应 Unit 做配套练习。
    </p>
  </section>
</template>
