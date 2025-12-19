<script setup lang="ts">
import { ref } from 'vue';
import HomeView from './views/HomeView.vue';
import LessonView from './views/LessonView.vue';

const currentView = ref('home');
const selectedCourse = ref(null);

const handleSelectCourse = (course: any) => {
  selectedCourse.value = course;
  currentView.value = 'lesson';
};

const handleBackToHome = () => {
  currentView.value = 'home';
  selectedCourse.value = null;
};
</script>

<template>
  <main class="app-container">
    <Transition name="page" mode="out-in">
      <HomeView 
        v-if="currentView === 'home'" 
        @select-course="handleSelectCourse" 
      />
      <LessonView 
        v-else 
        :lesson="selectedCourse"
        @back="handleBackToHome"
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

