<script setup lang="ts">
import courses from '../data/courses.json';

defineEmits(['select-course']);
</script>

<template>
  <div class="home-container min-h-screen">
    <div class="hero-section py-20 px-6">
      <div class="max-w-6xl mx-auto text-center">
        <h1 class="text-5xl md:text-7xl font-black text-gray-900 mb-6 tracking-tight">
          Visual <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">NCE</span>
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto font-medium">
          Master New Concept English with immersive visual scenes and interactive scripts. Choose your course to begin.
        </p>
      </div>
    </div>

    <div class="courses-grid max-w-6xl mx-auto px-6 pb-20">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div 
          v-for="course in courses" 
          :key="course.id"
          class="course-card group cursor-pointer"
          @click="$emit('select-course', course)"
        >
          <div class="relative overflow-hidden rounded-[2.5rem] bg-white shadow-xl transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 ring-1 ring-gray-100">
            <!-- Image Section -->
            <div class="aspect-[4/5] overflow-hidden">
              <img 
                :src="course.image" 
                :alt="course.title"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 transition-opacity group-hover:opacity-80"></div>
            </div>

            <!-- Content Overlay -->
            <div class="absolute inset-0 p-8 flex flex-col justify-end text-white">
              <div class="mb-4">
                <span class="px-3 py-1 rounded-full bg-blue-500/20 backdrop-blur-md border border-white/20 text-[10px] font-bold tracking-widest uppercase">
                  {{ course.level }}
                </span>
              </div>
              <h3 class="text-2xl font-bold mb-2">{{ course.title }}</h3>
              <p class="text-sm text-gray-200 line-clamp-2 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-4 group-hover:translate-y-0">
                {{ course.description }}
              </p>
              
              <div class="mt-6 flex items-center gap-2 text-blue-400 font-bold text-sm transform transition-all duration-300 opacity-0 group-hover:opacity-100">
                START LEARNING
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.05), transparent),
              radial-gradient(circle at bottom left, rgba(99, 102, 241, 0.05), transparent);
}

.course-card {
  perspective: 1000px;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.hero-section h1 {
  animation: float 6s ease-in-out infinite;
}
</style>
