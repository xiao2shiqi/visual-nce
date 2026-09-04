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
      <div class="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
        <SiteMark name="Visual NCE" />
        <div class="flex items-center gap-3">
          <ThemeToggle />
          <button
            @click="donationModalRef?.openDonation()"
            class="flex items-center gap-2 px-4 py-2 rounded-md bg-raised border border-line hover:border-line-strong transition-colors duration-300 group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-ink-mute group-hover:text-ink transition-colors">
              <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
            </svg>
            <span class="text-xs font-semibold text-ink-soft group-hover:text-ink">Support</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Hero：一张大图撑门面 -->
    <section class="hero-section relative pt-10 pb-8 px-6">
      <div class="max-w-5xl mx-auto animate-fade-in">
        <!-- 门面插画：整站只在这里出现一次，其余插画进入课程页才加载 -->
        <div class="relative rounded-xl overflow-hidden ring-1 ring-line">
          <img
            src="/images/nce1/l121/scene1.webp"
            alt="Visual NCE"
            width="1280"
            height="548"
            fetchpriority="high"
            class="w-full aspect-[21/9] object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-zinc-950/90 via-zinc-950/45 to-zinc-950/10"></div>

          <div class="absolute inset-0 flex flex-col items-center justify-end pb-10 px-6 text-center">
            <h1 class="font-display text-5xl text-white tracking-tight mb-3">Visual NCE</h1>
            <p class="text-sm text-zinc-200 mb-1">用 AI 重构《新概念英语》</p>
            <p class="text-xs text-zinc-300">吉卜力插画 × 音画同步 × 深度解析</p>
          </div>
        </div>

        <!-- Stats -->
        <div class="flex items-center justify-center gap-8 mt-6 text-xs text-ink-soft">
          <span><strong class="text-ink font-semibold">4</strong> 册全收录</span>
          <span class="w-px h-3 bg-line-strong"></span>
          <span><strong class="text-ink font-semibold">500+</strong> 课时覆盖</span>
          <span class="w-px h-3 bg-line-strong"></span>
          <span><strong class="text-ink font-semibold">AI</strong> 吉卜力插画</span>
        </div>
      </div>
    </section>


    <!-- Course Selection Section -->
    <section class="max-w-6xl mx-auto px-6 pb-24 pt-4">
      <!-- Continue Learning -->
      <div v-if="lastStudy" class="flex justify-center mb-8 animate-fade-in">
        <button
          @click="continueStudy"
          class="group flex items-center gap-3 pl-4 pr-5 py-2.5 rounded-full bg-raised border border-line shadow-sm hover:shadow-md hover:border-line-strong transition-all duration-300"
        >
          <span class="w-8 h-8 rounded-full bg-hovered flex items-center justify-center text-ink">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 translate-x-[1px]">
              <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
            </svg>
          </span>
          <span class="text-left">
            <span class="block text-[10px] font-bold text-ink-mute uppercase tracking-widest">继续学习 · 上次到 {{ formatTime(lastStudy.time) }}</span>
            <span class="block text-sm font-bold text-ink-soft group-hover:text-ink transition-colors">{{ lastStudy.lesson.title }}: {{ lastStudy.lesson.subtitle }}</span>
          </span>
        </button>
      </div>

      <!-- Book Tabs -->
      <div class="flex flex-wrap justify-center gap-2 mb-10 px-2 py-2 rounded-full bg-raised backdrop-blur-sm w-fit mx-auto border border-line shadow-sm">
        <button
          v-for="book in curriculum.books"
          :key="book.id"
          @click="activeBookId = book.id"
          class="px-6 py-2.5 rounded-full text-sm font-bold transition-colors duration-300"
          :class="activeBookId === book.id
            ? 'bg-btn text-btn-fg shadow-md'
            : 'text-ink-soft hover:text-ink hover:bg-raised'"
        >
          {{ book.subtitle }}
        </button>
      </div>

      <!-- Active Book Highlight -->
      <div class="text-center animate-fade-in mb-12" :key="activeBookId">
        <h2 class="font-display text-3xl text-ink mb-3">{{ activeBook.title }}</h2>
        <p class="text-ink-soft">{{ activeBook.description }}</p>

        <!-- 学习进度（有记录才显示，保持首屏干净） -->
        <div v-if="bookProgress.done > 0" class="mt-5 flex items-center justify-center gap-3">
          <div class="w-48 h-1.5 rounded-full bg-line-strong/80 overflow-hidden">
            <div class="h-full rounded-full bg-btn transition-all duration-500" :style="{ width: bookProgress.pct + '%' }"></div>
          </div>
          <span class="text-xs font-semibold text-ink-soft">已学 {{ bookProgress.done }} / {{ bookProgress.total }}</span>
        </div>
      </div>

      <!-- Lessons List：纯文字列表，插画进入课程页才加载 -->
      <div class="animate-slide-up" :key="activeBookId + 'list'">
        <div v-if="activeBook.lessons.length" class="grid grid-cols-2 gap-x-10 border-t border-line">
          <button
            v-for="lesson in activeBook.lessons"
            :key="lesson.id"
            @click="handleLessonClick(lesson)"
            class="group flex items-center gap-4 py-3 px-3 -mx-3 text-left border-b border-line hover:bg-hovered transition-colors duration-200"
          >
            <span class="w-12 shrink-0 font-mono text-xs text-ink-mute group-hover:text-ink-soft transition-colors">
              {{ lesson.title.replace('Lesson ', 'L') }}
            </span>
            <span class="flex-1 text-sm text-ink-soft group-hover:text-ink transition-colors truncate">
              {{ lesson.subtitle }}
            </span>
            <span v-if="isCompleted(lesson.id)" class="shrink-0 text-ink-mute" title="已完成">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3.5 h-3.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </span>
            <span class="shrink-0 w-3 text-ink-mute opacity-0 group-hover:opacity-100 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-3 h-3">
                <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </span>
          </button>
        </div>

        <!-- 空册占位 -->
        <div v-else class="py-20 text-center">
          <p class="text-ink-mute text-sm">该册内容制作中</p>
        </div>
      </div>


      <!-- Coming Soon Toast -->
      <Transition name="toast">
        <div
          v-if="showComingSoonToast"
          class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 px-8 py-5 bg-hovered/95 backdrop-blur-sm text-white rounded-xl shadow-2xl flex items-center gap-4"
        >
          <div class="w-12 h-12 bg-btn/20 rounded-xl flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6 text-ink-mute">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
          </div>
          <div>
            <p class="font-black text-lg">敬请期待</p>
            <p class="text-ink-mute text-sm">该课程正在制作中...</p>
          </div>
        </div>
      </Transition>

    </section>

    <!-- Features Section -->
    <section class="border-t border-line bg-raised py-16 px-6">
      <div class="max-w-4xl mx-auto animate-fade-in">
        <div class="text-center mb-10">
          <h2 class="font-display text-2xl text-ink">为什么选择 Visual NCE？</h2>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div
            v-for="f in features"
            :key="f.title"
            class="flex gap-4 p-5 rounded-xl bg-raised border border-line shadow-sm hover:shadow-md transition-shadow duration-300"
          >
            <div class="w-10 h-10 shrink-0 rounded-xl bg-hovered flex items-center justify-center text-ink mt-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" :d="f.icon" />
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-bold text-ink mb-1">{{ f.title }}</h3>
              <p class="text-xs text-ink-soft leading-relaxed">{{ f.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer / Project Info Section -->
    <footer class="border-t border-line bg-raised py-8 px-6">
      <div class="max-w-6xl mx-auto">
        <div class="flex flex-row justify-between items-center gap-4 text-ink-mute">
          <p class="text-xs font-bold uppercase tracking-tighter">© 2025 Visual NCE Project</p>
          <div class="flex items-center gap-6 text-xs font-bold uppercase tracking-tighter">
            <span class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">About & Disclaimer</span>
            <span class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">作者微信</span>
            <a href="https://xiao27.com" class="hover:text-ink cursor-pointer transition-colors">← xiao27 hub</a>
            <a href="https://github.com/xiao2shiqi/visual-nce" target="_blank" class="hover:text-ink cursor-pointer transition-colors">GitHub</a>
            <span class="hover:text-ink cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">Author: xiaobin</span>
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
  animation: fadeIn 0.8s ease-out forwards;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out forwards;
}

/* Toast animation */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.9);
}

.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
