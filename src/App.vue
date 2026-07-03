<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import HomeView from './views/HomeView.vue';
import LessonView from './views/LessonView.vue';
import curriculum from './data/curriculum.json';

// 从 curriculum 中通过 lessonId 查找课程对象和所属 bookId
const findLesson = (lessonId: string) => {
  for (const book of curriculum.books) {
    const lesson = book.lessons.find((l: any) => l.id === lessonId);
    if (lesson) return { lesson, bookId: book.id };
  }
  return null;
};

const BOOK_IDS = curriculum.books.map(b => b.id);

// 解析 hash：#nce1-l1 → 课程页；#nce2 → 首页对应册；其他 → 首页
const parseHash = () => {
  const hash = window.location.hash.slice(1);
  if (!hash) return null;
  if (BOOK_IDS.includes(hash)) return { view: 'home', bookId: hash, lesson: null };
  const found = findLesson(hash);
  if (found) return { view: 'lesson', bookId: found.bookId, lesson: found.lesson };
  return null;
};

// 同步读取 hash，避免首帧渲染主页导致闪烁
const _init = parseHash();
const currentView = ref(_init?.view === 'lesson' ? 'lesson' : 'home');
const selectedCourse = ref<any>(_init?.lesson || null);
const activeBookId = ref(_init?.bookId || 'nce1');

// 从 URL hash 恢复状态
const restoreFromHash = () => {
  const parsed = parseHash();
  if (parsed?.view === 'lesson') {
    selectedCourse.value = parsed.lesson;
    activeBookId.value = parsed.bookId;
    currentView.value = 'lesson';
    return;
  }
  if (parsed?.view === 'home') {
    activeBookId.value = parsed.bookId;
  }
  currentView.value = 'home';
  selectedCourse.value = null;
};

// 首页切换册数时同步到 URL（replace，避免污染历史记录）
const handleBookChange = (bookId: string) => {
  activeBookId.value = bookId;
  if (currentView.value === 'home') {
    history.replaceState(null, '', `#${bookId}`);
  }
};

const handleSelectCourse = (payload: any) => {
  if (payload?.lesson) {
    selectedCourse.value = payload.lesson;
    if (payload.bookId) {
      activeBookId.value = payload.bookId;
    }
    window.location.hash = payload.lesson.id;
  } else {
    selectedCourse.value = payload;
    window.location.hash = payload.id;
  }
  currentView.value = 'lesson';
};

const handleBackToHome = () => {
  currentView.value = 'home';
  selectedCourse.value = null;
  // 回首页保留当前册数，便于继续浏览和分享目录
  history.pushState(null, '', `#${activeBookId.value}`);
};

// 支持浏览器前进/后退
const onHashChange = () => restoreFromHash();

onMounted(() => {
  restoreFromHash();
  window.addEventListener('hashchange', onHashChange);
});

onUnmounted(() => {
  window.removeEventListener('hashchange', onHashChange);
});
</script>

<template>
  <main class="app-container">
    <Transition name="page" mode="out-in">
      <HomeView
        v-if="currentView === 'home'"
        :active-book-id="activeBookId"
        @update:active-book-id="handleBookChange"
        @select-course="handleSelectCourse"
      />
      <LessonView 
        v-else 
        :lesson="selectedCourse"
        @back="handleBackToHome"
        @select-course="handleSelectCourse"
      />
    </Transition>
  </main>
</template>

<style>
/* 底色、文字色、body 最小宽度统一由 style.css 管理，这里不再重复声明 */
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
}

#app {
  width: 100%;
}

.app-container {
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

.page-enter-active,
.page-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
