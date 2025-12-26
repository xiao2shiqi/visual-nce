<script setup lang="ts">
import { ref, computed } from 'vue';
import curriculum from '../data/curriculum.json';
import { resolvePath } from '../utils/resolvePath';
import AboutModal from '../components/AboutModal.vue';
import DonationModal from '../components/DonationModal.vue';
import FeedbackModal from '../components/FeedbackModal.vue';

const activeBookId = ref('nce1');
const aboutModalRef = ref<any>(null);
const donationModalRef = ref<any>(null);
const feedbackModalRef = ref<any>(null);

const activeBook = computed(() => {
  const book = curriculum.books.find(b => b.id === activeBookId.value);
  return (book || curriculum.books[0]) as typeof curriculum.books[0];
});

defineEmits(['select-course']);
</script>

<template>
  <div class="home-container min-h-screen">
    <!-- Feedback Floating Button -->
    <div class="fixed bottom-6 right-6 z-40 animate-fade-in-up">
      <button 
        @click="feedbackModalRef?.openFeedback()"
        class="flex items-center gap-2 px-5 py-3 rounded-full bg-slate-800 text-white font-bold shadow-lg shadow-slate-900/20 hover:bg-slate-700 hover:scale-105 active:scale-95 transition-all duration-300 group"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5 group-hover:rotate-12 transition-transform">
          <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
        </svg>
        <span>建议 / 反馈</span>
      </button>
    </div>

    <!-- Hero / Vision Section -->
    <section class="hero-section relative py-12 px-6 overflow-hidden">
      <!-- Ambient background decorations -->
      <div class="absolute top-0 left-0 w-full h-full -z-10 bg-gradient-to-b from-blue-50/50 to-transparent"></div>
      
      <!-- Top Right Actions -->
      <div class="absolute top-6 right-6 z-10">
        <button 
          @click="donationModalRef?.openDonation()"
          class="flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 backdrop-blur-sm border border-slate-200 shadow-sm hover:shadow-md hover:scale-105 transition-all duration-300 group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-slate-400 group-hover:text-amber-500 transition-colors">
             <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
          </svg>
          <span class="text-xs font-bold text-slate-500 group-hover:text-slate-700">Support</span>
        </button>
      </div>

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
            融合 AI 与现代 Web 技术重构经典。通过沉浸式的场景与音频交互，让《新概念英语》的学习不再枯燥。也让老教材焕发出新的活力。
          </p>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="max-w-6xl mx-auto px-6 mb-16 animate-fade-in">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Feature 1: Ghibli Style -->
        <div class="group p-6 rounded-3xl bg-white shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
          <div class="w-12 h-12 rounded-2xl bg-blue-50 group-hover:bg-blue-500 transition-colors duration-300 flex items-center justify-center text-blue-500 group-hover:text-white mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.146 6.32a15.996 15.996 0 0 0-4.649 4.763m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" />
            </svg>
          </div>
          <h3 class="text-lg font-black text-slate-800 mb-2 group-hover:text-blue-600 transition-colors">吉卜力视觉重制</h3>
          <p class="text-sm text-slate-500 font-medium leading-relaxed">
            告别枯燥的原版插图。每一课场景都以<span class="text-blue-500 font-bold">温暖治愈的吉卜力风格</span>重新绘制，让英语学习变成一场赏心悦目的视觉之旅。
          </p>
        </div>
        
        <!-- Feature 2: Sentence Analysis -->
        <div class="group p-6 rounded-3xl bg-white shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 group-hover:bg-indigo-500 transition-colors duration-300 flex items-center justify-center text-indigo-500 group-hover:text-white mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
            </svg>
          </div>
          <h3 class="text-lg font-black text-slate-800 mb-2 group-hover:text-indigo-600 transition-colors">逐句深度解析</h3>
          <p class="text-sm text-slate-500 font-medium leading-relaxed">
            不留任何知识盲区。内置<span class="text-indigo-500 font-bold">详细的句子分析</span>功能，智能拆解每一句话的语法结构、核心词汇与发音重点，助你真正吃透课文。
          </p>
        </div>

        <!-- Feature 3: Professional Tools -->
        <div class="group p-6 rounded-3xl bg-white shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
          <div class="w-12 h-12 rounded-2xl bg-cyan-50 group-hover:bg-cyan-500 transition-colors duration-300 flex items-center justify-center text-cyan-500 group-hover:text-white mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
            </svg>
          </div>
          <h3 class="text-lg font-black text-slate-800 mb-2 group-hover:text-cyan-600 transition-colors">专业级听读工具</h3>
          <p class="text-sm text-slate-500 font-medium leading-relaxed">
            为精听与跟读量身打造。支持<span class="text-cyan-500 font-bold">无级变速、单句循环</span>与键盘快捷键控制，配合滚动高亮与双语切换，让语言训练更高效。
          </p>
        </div>
      </div>
    </section>

    <!-- Course Selection Section -->
    <section class="max-w-6xl mx-auto px-6 pb-32">
      <!-- Book Tabs -->
      <div class="flex flex-wrap justify-center gap-3 mb-8 px-4 py-2 rounded-3xl bg-slate-100/50 backdrop-blur-sm w-fit mx-auto border border-white/50">
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

      <!-- Active Book Highlight -->
      <div class="text-center animate-fade-in mb-12" :key="activeBookId">
        <h2 class="text-3xl font-black text-slate-900 mb-3">{{ activeBook.title }}</h2>
        <p class="text-slate-500 font-medium">{{ activeBook.description }}</p>
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
              :src="resolvePath(lesson.image)" 
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
            <span class="hover:text-blue-500 cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">About & Disclaimer</span>
            <a href="https://github.com/xiao2shiqi/visual-nce" target="_blank" class="hover:text-blue-500 cursor-pointer transition-colors">GitHub</a>
            <span class="hover:text-blue-500 cursor-pointer transition-colors" @click="aboutModalRef?.openAbout()">Author: xiaobin</span>
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
