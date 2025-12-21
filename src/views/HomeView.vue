<script setup lang="ts">
import { ref, computed } from 'vue';
import curriculum from '../data/curriculum.json';

const activeBookId = ref('nce1');

const activeBook = computed(() => {
  const book = curriculum.books.find(b => b.id === activeBookId.value);
  return (book || curriculum.books[0]) as typeof curriculum.books[0];
});

defineEmits(['select-course']);
</script>

<template>
  <div class="home-container min-h-screen">
    <!-- Hero / Vision Section -->
    <section class="hero-section relative py-12 px-6 overflow-hidden">
      <!-- Ambient background decorations -->
      <div class="absolute top-0 left-0 w-full h-full -z-10 bg-gradient-to-b from-blue-50/50 to-transparent"></div>
      
      <div class="max-w-5xl mx-auto text-center relative">
        <h1 class="text-5xl md:text-6xl font-black text-slate-900 mb-4 tracking-tight leading-tight animate-fade-in">
          Visual <span class="text-gradient">NCE</span>
        </h1>

        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white shadow-sm border border-blue-50 mb-8 animate-fade-in scale-90">
          <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
          <span class="text-[10px] font-bold text-blue-600 uppercase tracking-widest">Immersive Learning Experience</span>
        </div>
        
        <div class="max-w-3xl mx-auto">
          <p class="text-lg text-slate-600 font-medium leading-relaxed">
            项目愿景：重新定义经典。通过沉浸式的视觉场景与音频交互，让《新概念英语》的学习不再枯燥。
          </p>
        </div>
      </div>
    </section>

    <!-- Course Selection Section -->
    <section class="max-w-6xl mx-auto px-6 pb-32">
      <!-- Book Tabs -->
      <div class="flex flex-wrap justify-center gap-3 mb-16 px-4 py-2 rounded-3xl bg-slate-100/50 backdrop-blur-sm w-fit mx-auto border border-white/50">
        <button 
          v-for="book in curriculum.books" 
          :key="book.id"
          @click="activeBookId = book.id"
          class="px-6 py-2.5 rounded-2xl text-sm font-bold transition-all duration-300"
          :class="activeBookId === book.id 
            ? 'bg-white text-blue-600 shadow-md scale-105' 
            : 'text-slate-500 hover:text-slate-900 hover:bg-white/50'"
        >
          {{ book.subtitle }}
        </button>
      </div>

      <!-- Lessons Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 animate-slide-up" :key="activeBookId + 'grid'">
        <div 
          v-for="lesson in activeBook.lessons" 
          :key="lesson.id"
          class="lesson-item group cursor-pointer"
          @click="$emit('select-course', lesson)"
        >
          <div class="relative aspect-[3/4] rounded-2xl overflow-hidden bg-white shadow-lg ring-1 ring-slate-200/50 transition-all duration-500 group-hover:shadow-blue-200 group-hover:-translate-y-2 group-hover:ring-blue-500/30">
            <!-- Lesson Image -->
            <img 
              :src="lesson.image" 
              :alt="lesson.title"
              class="w-full h-full object-cover grayscale-[0.3] group-hover:grayscale-0 transition-all duration-700 group-hover:scale-110"
            />
            
            <!-- Overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/20 to-transparent opacity-80 group-hover:opacity-90"></div>
            
            <!-- Content -->
            <div class="absolute inset-0 p-4 flex flex-col justify-end">
              <span class="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">{{ lesson.title }}</span>
              <h4 class="text-sm font-bold text-white leading-tight group-hover:text-blue-300 transition-colors">{{ lesson.subtitle }}</h4>
              
              <div class="mt-3 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
                <span class="text-[9px] font-black text-white uppercase tracking-tighter">Enter Lesson</span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="3" stroke="currentColor" class="w-3 h-3 text-white">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Placeholder for empty books -->
        <div v-if="activeBook.lessons.length === 0" class="col-span-full py-20 text-center">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-300">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <p class="text-slate-400 font-bold uppercase tracking-widest text-xs">Waiting for Content Update</p>
        </div>
      </div>

      <!-- Active Book Highlight (Moved to bottom) -->
      <div class="mt-16 text-center animate-fade-in" :key="activeBookId">
        <h2 class="text-3xl font-black text-slate-900 mb-3">{{ activeBook.title }}</h2>
        <p class="text-slate-500 font-medium">{{ activeBook.description }}</p>
      </div>
    </section>

    <!-- Footer / Project Info Section -->
    <footer class="border-t border-slate-100 bg-slate-50/50 py-20 px-6">
      <div class="max-w-6xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div>
            <h3 class="text-xs font-black text-blue-600 uppercase tracking-widest mb-4">项目背景 / Background</h3>
            <p class="text-sm text-slate-500 leading-relaxed font-medium">
              《新概念英语》作为全球最经典的英语教材之一，陪伴了几代人的成长。然而，传统的“录音+课本”模式在移动互联网时代显得有些力不从心。Visual NCE 旨在利用现代 Web 技术，赋予这套经典教材全新的视觉生命力。
            </p>
          </div>
          <div>
            <h3 class="text-xs font-black text-indigo-600 uppercase tracking-widest mb-4">核心技术 / Technology</h3>
            <p class="text-sm text-slate-500 leading-relaxed font-medium">
              基于 Vue 3 和滚动驱动的精准交互，我们实现了毫秒级的音画同步。通过原子化样式与沉浸式 UI 设计，为学习者打造一个无干扰、高效率的数字化语言学习空间。
            </p>
          </div>
        </div>
        
        <div class="mt-16 pt-8 border-t border-slate-200/60 flex flex-col md:flex-row justify-between items-center gap-4 text-slate-400">
          <p class="text-xs font-bold uppercase tracking-tighter">© 2025 Visual NCE Project</p>
          <div class="flex items-center gap-6 text-xs font-bold uppercase tracking-tighter">
            <span class="hover:text-blue-500 cursor-pointer transition-colors">Documentation</span>
            <span class="hover:text-blue-500 cursor-pointer transition-colors">GitHub</span>
            <span class="hover:text-blue-500 cursor-pointer transition-colors">Author: xiaobin</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.text-gradient {
  background: linear-gradient(to right, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

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

/* Ensure smooth card transitions */
.lesson-item {
  perspective: 1000px;
}
</style>
