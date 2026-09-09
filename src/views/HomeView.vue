<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import curriculum from '../data/curriculum.json';
import AboutModal from '../components/AboutModal.vue';
import DonationModal from '../components/DonationModal.vue';
import FeedbackModal from '../components/FeedbackModal.vue';
import SiteMark from '../components/SiteMark.vue';
import ThemeToggle from '../components/ThemeToggle.vue';

const props = withDefaults(defineProps<{
  activeBookId?: string;
}>(), {
  activeBookId: 'nce1'
});

const emit = defineEmits(['select-course', 'update:active-book-id']);
const activeBookId = ref(props.activeBookId);

watch(() => props.activeBookId, (newId) => {
  if (newId && newId !== activeBookId.value) {
    activeBookId.value = newId;
  }
});

watch(activeBookId, (newId) => {
  emit('update:active-book-id', newId);
});

const aboutModalRef = ref<any>(null);
const donationModalRef = ref<any>(null);
const feedbackModalRef = ref<any>(null);
const showComingSoonToast = ref(false);

const activeBook = computed(() => {
  const book = curriculum.books.find(b => b.id === activeBookId.value);
  return (book || curriculum.books[0]) as typeof curriculum.books[0];
});

// 继续学习：读取上次学习记录（由 LessonView 写入 localStorage）
const lastStudy = (() => {
  try {
    const raw = localStorage.getItem('vnce_last_lesson');
    if (!raw) return null;
    const saved = JSON.parse(raw);
    for (const book of curriculum.books) {
      const lesson = book.lessons.find((l: any) => l.id === saved.id);
      if (lesson) return { lesson, bookId: book.id, time: saved.time as number };
    }
  } catch { /* 记录损坏则忽略 */ }
  return null;
})();

const formatTime = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

// 已完成课程集合（学习者在课程页手动标记，LessonView 写入）
const completedSet = (() => {
  try {
    return new Set<string>(JSON.parse(localStorage.getItem('vnce_completed') || '[]'));
  } catch {
    return new Set<string>();
  }
})();

const isCompleted = (lessonId: string) => completedSet.has(lessonId);

// 当前册的学习进度
const bookProgress = computed(() => {
  const lessons = activeBook.value.lessons;
  const done = lessons.filter((l: any) => completedSet.has(l.id)).length;
  return { done, total: lessons.length, pct: lessons.length ? Math.round(done / lessons.length * 100) : 0 };
});

const continueStudy = () => {
  if (!lastStudy) return;
  emit('select-course', { lesson: lastStudy.lesson, bookId: lastStudy.bookId });
};

const handleLessonClick = (lesson: any) => {
  if (lesson.image && lesson.image.includes('coming-soon')) {
    showComingSoonToast.value = true;
    setTimeout(() => {
      showComingSoonToast.value = false;
    }, 2000);
  } else {
    emit('select-course', {
      lesson,
      bookId: activeBookId.value
    });
  }
};

const features = [
  {
    title: '吉卜力视觉重制',
    desc: '告别枯燥原版插图。每一课场景以温暖治愈的吉卜力风格重新绘制，学习变成一场视觉之旅。',
    icon: 'M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42'
  },
  {
    title: '音画实时同步',
    desc: '听到哪里，画面跟到哪里。音频播放时插画自动随台词切换，每句对话都有对应场景。',
    icon: 'm15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z'
  },
  {
    title: '逐句深度解析',
    desc: '不留知识盲区。内置句子分析功能，智能拆解语法结构、核心词汇与发音重点，真正吃透课文。',
    icon: 'M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5'
  },
  {
    title: '专业级听读工具',
    desc: '为精听与跟读量身打造。支持无级变速、单句循环与键盘快捷键，滚动高亮 + 双语切换。',
    icon: 'M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z'
  },
  {
    title: '剑桥语法地图',
    desc: '每课标注对应《剑桥初级/中级英语语法》的核心章节，课文与语法书互相印证，练习有的放矢。',
    icon: 'M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z'
  },
  {
    title: '词典一键直达',
    desc: '点击任意单词即可一键唤起欧路词典深度查询，省去复制粘贴，学习更流畅高效。',
    icon: 'M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25'
  }
];
</script>


<template>
  <div class="home-container min-h-screen">
    <!-- Feedback Floating Button -->
    <div class="fixed bottom-6 right-6 z-40 animate-fade-in-up">
      <button
        @click="feedbackModalRef?.openFeedback()"
        class="flex items-center gap-2 px-5 py-3 rounded-full btn-primary font-bold shadow-lg transition-colors duration-300 group"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
        </svg>
        <span>建议 / 反馈</span>
      </button>
    </div>

    <!-- 顶栏：与 xiao27-hub / tube-shadowing 同一套壳 -->
    <header class="sticky top-0 z-40 w-full border-b border-line bg-base/85 backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-6 sm:px-8 h-16 flex items-center justify-between">
        <SiteMark name="Visual NCE" />
        <div class="flex items-center gap-3">
          <ThemeToggle />
          <button
            @click="donationModalRef?.openDonation()"
            class="flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-raised border border-line hover:border-line-strong transition-colors duration-300 group cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-ink-mute group-hover:text-ink transition-colors">
              <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
            </svg>
            <span class="text-xs font-semibold text-ink-soft group-hover:text-ink">Support</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Hero：全幅铺满主视觉（顶到屏幕两侧，无圆角无留白，高度 70~80vh） -->
    <section class="hero-section relative w-full h-[72vh] min-h-[560px] max-h-[820px] overflow-hidden flex items-end">
      <div class="absolute inset-0 w-full h-full">
        <img
          src="/images/nce1/l121/scene1.webp"
          alt="Visual NCE - 吉卜力风格插画重制版新概念英语"
          width="1920"
          height="1080"
          fetchpriority="high"
          class="w-full h-full object-cover object-center"
        />
        <!-- 渐变遮罩：保证文字在任何底图上都具备极高可读性（符合 BRAND.md 图片压字例外） -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/95 via-black/45 to-black/10"></div>
      </div>

      <div class="relative z-10 w-full max-w-7xl mx-auto px-6 sm:px-8 pb-16 pt-20 flex flex-col items-start justify-end">
        <div class="animate-fade-in max-w-3xl">
          <span class="inline-block px-3 py-1 rounded-full text-xs font-mono font-medium bg-black/45 text-white backdrop-blur-md mb-4 border border-white/25">
            Studio Ghibli Style · AI Remastered
          </span>
          <h1 class="font-display text-5xl sm:text-6xl md:text-7xl lg:text-8xl text-white font-normal tracking-tight leading-[1.05] mb-4">
            Visual NCE
          </h1>
          <p class="text-xl sm:text-2xl text-zinc-200 font-light tracking-wide leading-relaxed mb-6">
            用吉卜力艺术重构《新概念英语》
          </p>
          <div class="flex flex-wrap items-center gap-6 sm:gap-10 text-xs sm:text-sm text-zinc-300 font-medium tracking-wide">
            <span class="flex items-center gap-2">
              <strong class="text-white text-base font-bold font-mono">4</strong> 册全量收录
            </span>
            <span class="w-1 h-1 rounded-full bg-white/40"></span>
            <span class="flex items-center gap-2">
              <strong class="text-white text-base font-bold font-mono">276</strong> 篇经典课文
            </span>
            <span class="w-1 h-1 rounded-full bg-white/40"></span>
            <span class="flex items-center gap-2">
              <strong class="text-white text-base font-bold font-mono">100%</strong> 逐句音画同步
            </span>
          </div>
        </div>
      </div>
    </section>


    <!-- Course Selection Section -->
    <section class="max-w-7xl mx-auto px-6 sm:px-8 py-20">
      <!-- Continue Learning -->
      <div v-if="lastStudy" class="flex justify-center mb-12 animate-fade-in">
        <button
          @click="continueStudy"
          class="group flex items-center gap-3.5 pl-4 pr-6 py-2.5 rounded-full bg-raised border border-line shadow-xs hover:shadow-md hover:border-line-strong transition-all duration-300 cursor-pointer"
        >
          <span class="w-8 h-8 rounded-full bg-btn flex items-center justify-center text-btn-fg shadow-xs">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5 translate-x-0.5">
              <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
            </svg>
          </span>
          <span class="text-left">
            <span class="block text-[11px] font-mono font-medium text-ink-mute">继续学习 · 上次进度 {{ formatTime(lastStudy.time) }}</span>
            <span class="block text-sm font-bold text-ink group-hover:text-ink transition-colors truncate max-w-xs sm:max-w-md">
              {{ lastStudy.lesson.title }} · {{ lastStudy.lesson.subtitle }}
            </span>
          </span>
        </button>
      </div>

      <!-- Book Switcher Tabs -->
      <div class="flex justify-center mb-14">
        <div class="inline-flex p-1.5 rounded-full bg-raised border border-line shadow-xs gap-1.5">
          <button
            v-for="book in curriculum.books"
            :key="book.id"
            @click="activeBookId = book.id"
            class="px-6 py-2 rounded-full text-sm font-bold transition-all duration-200 cursor-pointer"
            :class="activeBookId === book.id
              ? 'bg-btn text-btn-fg shadow-xs'
              : 'text-ink-soft hover:text-ink hover:bg-hovered'"
          >
            {{ book.subtitle }}
          </button>
        </div>
      </div>

      <!-- Active Book Headline & Info -->
      <div class="text-center mb-14 animate-fade-in" :key="activeBookId">
        <span class="inline-block text-xs font-mono font-bold tracking-widest text-ink-mute uppercase mb-2">
          {{ activeBook.subtitle }} · {{ activeBook.level || 'Course Syllabus' }}
        </span>
        <h2 class="font-display text-4xl sm:text-5xl md:text-6xl font-bold text-ink tracking-tight mb-3">
          {{ activeBook.title }}
        </h2>
        <p class="text-base sm:text-lg text-ink-soft max-w-xl mx-auto leading-relaxed">
          {{ activeBook.description }}
        </p>

        <!-- 学习进度 -->
        <div v-if="bookProgress.done > 0" class="mt-6 flex flex-col items-center gap-2">
          <div class="w-56 h-1.5 rounded-full bg-hovered border border-line overflow-hidden">
            <div class="h-full rounded-full bg-btn transition-all duration-500" :style="{ width: bookProgress.pct + '%' }"></div>
          </div>
          <span class="text-xs font-mono text-ink-mute">已完成 {{ bookProgress.done }} / {{ bookProgress.total }} 课 ({{ bookProgress.pct }}%)</span>
        </div>
      </div>

      <!-- Lessons Grid：缩略图网格卡片（懒加载 + 异步解码 + 避免布局抖动） -->
      <div class="animate-slide-up" :key="activeBookId + 'list'">
        <div v-if="activeBook.lessons.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 sm:gap-7">
          <button
            v-for="lesson in activeBook.lessons"
            :key="lesson.id"
            @click="handleLessonClick(lesson)"
            class="group flex flex-col text-left cursor-pointer transition-all duration-300"
          >
            <!-- 缩略图容器（固定 480x262 比例，防 CLS） -->
            <div class="relative w-full aspect-[480/262] rounded-xl overflow-hidden bg-hovered border border-line shadow-xs group-hover:border-line-strong group-hover:shadow-xl transition-all duration-300">
              <img
                :src="lesson.image"
                :alt="lesson.title + ' ' + lesson.subtitle"
                loading="lazy"
                decoding="async"
                width="480"
                height="262"
                class="w-full h-full object-cover object-center transition-transform duration-500 group-hover:scale-[1.04]"
              />

              <!-- 课程编号标签 -->
              <div class="absolute top-2.5 left-2.5 px-2.5 py-1 rounded-full text-[11px] font-mono font-bold bg-black/65 text-white/95 backdrop-blur-md border border-white/10 shadow-xs">
                {{ lesson.title.replace('Lesson ', 'L') }}
              </div>

              <!-- 已完成勾选徽章 -->
              <div
                v-if="isCompleted(lesson.id)"
                class="absolute top-2.5 right-2.5 w-6 h-6 rounded-full bg-[var(--color-success)] text-white flex items-center justify-center shadow-md"
                title="已完成"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-3.5 h-3.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                </svg>
              </div>

              <!-- Hover 播放微动效指示器 -->
              <div class="absolute bottom-2.5 right-2.5 w-7 h-7 rounded-full bg-black/60 text-white/90 backdrop-blur-md flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 border border-white/10 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5 translate-x-0.5">
                  <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>

            <!-- 课程文本 -->
            <div class="pt-3 px-1">
              <h3 class="text-base font-bold text-ink group-hover:text-ink transition-colors truncate">
                {{ lesson.subtitle }}
              </h3>
              <p class="text-xs font-mono text-ink-mute mt-0.5">
                {{ lesson.title }}
              </p>
            </div>
          </button>
        </div>

        <!-- 空册占位 -->
        <div v-else class="py-24 text-center">
          <p class="text-base text-ink-mute font-medium">该册内容正在由 AI 画师精心重制中，敬请期待</p>
        </div>
      </div>

      <!-- Coming Soon Toast -->
      <Transition name="toast">
        <div
          v-if="showComingSoonToast"
          class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 px-7 py-4 bg-raised text-ink border border-line rounded-xl shadow-2xl flex items-center gap-3.5 backdrop-blur-md"
        >
          <div class="w-10 h-10 bg-hovered rounded-xl flex items-center justify-center text-ink shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 text-ink">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
          <div>
            <p class="font-bold text-base text-ink">敬请期待</p>
            <p class="text-xs text-ink-soft">该课程内容正在制作中...</p>
          </div>
        </div>
      </Transition>
    </section>

    <!-- Features Section：去掉所有盒子与多余边框，依靠呼吸感大留白浮现 -->
    <section class="border-t border-line py-28 px-6 sm:px-8">
      <div class="max-w-7xl mx-auto">
        <!-- Section Title with Apple scale contrast -->
        <div class="text-center max-w-3xl mx-auto mb-20">
          <span class="text-xs font-mono font-bold tracking-widest text-ink-mute uppercase mb-3 block">
            Core Highlights · 核心特性
          </span>
          <h2 class="font-display text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-4">
            为什么选择 Visual NCE？
          </h2>
          <p class="text-base sm:text-lg text-ink-soft leading-relaxed">
            告别枯燥的黑白排版。结合前沿生成式 AI 与经典教材，打造沉浸式英语精听体验。
          </p>
        </div>

        <!-- Features Grid：无边框无背景，靠间距与排版建立秩序 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-16">
          <div
            v-for="f in features"
            :key="f.title"
            class="flex flex-col text-left group"
          >
            <!-- 图标直接浮在页面上，去掉厚重底座 -->
            <div class="w-8 h-8 text-ink mb-4 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.75" stroke="currentColor" class="w-7 h-7">
                <path stroke-linecap="round" stroke-linejoin="round" :d="f.icon" />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-ink mb-2 tracking-tight">
              {{ f.title }}
            </h3>
            <p class="text-sm text-ink-soft leading-relaxed">
              {{ f.desc }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer / Project Info Section -->
    <footer class="border-t border-line bg-raised py-12 px-6 sm:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-6 text-ink-mute">
          <p class="text-xs font-mono font-medium tracking-tight">© 2025–2026 Visual NCE Project</p>
          <div class="flex flex-wrap items-center justify-center gap-6 text-xs font-medium">
            <button class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">About & Disclaimer</button>
            <button class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">作者微信</button>
            <a href="https://xiao27.com" class="hover:text-ink cursor-pointer transition-colors">← xiao27 hub</a>
            <a href="https://github.com/xiao2shiqi/visual-nce" target="_blank" class="hover:text-ink cursor-pointer transition-colors">GitHub</a>
            <button class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">Author: xiaobin</button>
          </div>
        </div>
      </div>
    </footer>

    <AboutModal ref="aboutModalRef" />
    <DonationModal ref="donationModalRef" />
    <FeedbackModal ref="feedbackModalRef" />
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-slide-up {
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Toast animation */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.95);
}

.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.home-container {
  background: var(--bg-base);
}
</style>
