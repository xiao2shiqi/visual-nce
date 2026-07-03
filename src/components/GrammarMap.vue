<script setup lang="ts">
import { computed } from 'vue';
import grammarMap from '../data/grammar-map.json';

const props = defineProps<{
  lessonId: string;
}>();

type BookId = 'elem' | 'int';

interface GrammarRef {
  book: BookId;
  unit: number;
  title: string;
}

interface GrammarPoint {
  point: string;
  refs: GrammarRef[];
}

const books = grammarMap.books as Record<BookId, { name: string; edition: string; en: string }>;

const points = computed<GrammarPoint[]>(() => {
  const raw = (grammarMap.lessons as Record<string, any[]>)[props.lessonId];
  if (!raw) return [];
  return raw.map((p) => ({
    point: p.point,
    refs: (Object.entries(p.refs) as [BookId, number[]][]).flatMap(([book, units]) =>
      units.map((unit) => ({
        book,
        unit,
        title: (grammarMap.unitTitles as Record<BookId, Record<string, string>>)[book][String(unit)] || ''
      }))
    )
  }));
});
</script>

<template>
  <section v-if="points.length" class="mt-16 animate-fade-in">
    <div class="flex items-baseline justify-between mb-5 flex-wrap gap-2">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-amber-100 flex items-center justify-center text-amber-600">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
          </svg>
        </div>
        <h2 class="text-lg font-black text-slate-800">本课语法地图</h2>
      </div>
      <p class="text-xs text-slate-400">
        对应《{{ books.elem.name }}》（{{ books.elem.edition }}）与《{{ books.int.name }}》（{{ books.int.edition }}）的章节
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="(p, i) in points"
        :key="i"
        class="p-5 rounded-2xl bg-white/70 backdrop-blur-sm border border-slate-200/70 shadow-sm"
      >
        <h3 class="text-sm font-bold text-slate-800 mb-3 leading-relaxed">{{ p.point }}</h3>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="ref in p.refs"
            :key="ref.book + ref.unit"
            class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] font-semibold border"
            :class="ref.book === 'elem'
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200/70'
              : 'bg-indigo-50 text-indigo-700 border-indigo-200/70'"
            :title="`${books[ref.book].name}（${books[ref.book].edition}）Unit ${ref.unit}`"
          >
            <span class="font-black">{{ ref.book === 'elem' ? '初级' : '中级' }} U{{ ref.unit }}</span>
            <span class="opacity-70 font-medium">{{ ref.title }}</span>
          </span>
        </div>
      </div>
    </div>

    <p class="mt-4 text-[11px] text-slate-400 leading-relaxed">
      标签含义：<span class="font-semibold text-emerald-600">初级</span> = 剑桥初级英语语法（第三版），
      <span class="font-semibold text-indigo-600">中级</span> = 剑桥中级英语语法（第四版）。学完本课后，可翻到对应 Unit 做配套练习加深理解。
    </p>
  </section>
</template>
