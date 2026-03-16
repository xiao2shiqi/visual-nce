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

// 同步读取 hash，避免首帧渲染主页导致闪烁
const initFromHash = () => {
  const hash = window.location.hash.slice(1);
  if (hash) {
    const found = findLesson(hash);
    if (found) return found;
  }
  return null;
};

const _init = initFromHash();
const currentView = ref(_init ? 'lesson' : 'home');
const selectedCourse = ref<any>(_init ? _init.lesson : null);
const activeBookId = ref(_init ? _init.bookId : 'nce1');

// 从 URL hash 恢复状态（格式：#nce1-l1）
const restoreFromHash = () => {
  const hash = window.location.hash.slice(1);
  if (hash) {
    const found = findLesson(hash);
    if (found) {
      selectedCourse.value = found.lesson;
      activeBookId.value = found.bookId;
      currentView.value = 'lesson';
      return;
    }
  }
  currentView.value = 'home';
  selectedCourse.value = null;
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
  history.pushState(null, '', window.location.pathname); // 清除 hash
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
        @update:active-book-id="activeBookId = $event"
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
:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  background-color: #f8fafc;
  color: #1e293b;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
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
