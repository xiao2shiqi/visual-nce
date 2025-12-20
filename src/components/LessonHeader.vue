<script setup lang="ts">
/**
 * @author xiaobin
 */
defineProps<{
  title: string;
  subtitle?: string;
  badge?: string;
}>();

const emit = defineEmits(['back']);
</script>

<template>
  <header class="sticky top-0 z-30 backdrop-blur-xl bg-white/70 border-b border-gray-100/50">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-5">
        <!-- Back Button -->
        <button 
          @click="emit('back')"
          class="group flex items-center gap-2.5 text-gray-400 hover:text-gray-900 transition-all duration-300"
        >
          <div class="w-9 h-9 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center group-hover:bg-blue-50 group-hover:border-blue-100 group-hover:scale-105 transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 group-hover:text-blue-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
            </svg>
          </div>
        </button>
        
        <!-- Divider -->
        <div class="h-5 w-px bg-gray-200"></div>

        <!-- Title Area -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="white" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-black tracking-tight text-gray-900">{{ title }}</h1>
            <p class="text-xs text-gray-400 font-medium">{{ subtitle || 'New Concept English' }}</p>
          </div>
        </div>
      </div>
      
      <!-- Badge -->
      <div v-if="badge" class="hidden md:flex items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-full border border-blue-100/50">
          <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></div>
          <span class="text-[10px] font-bold text-blue-600 uppercase tracking-wider">{{ badge }}</span>
        </div>
      </div>
    </div>
  </header>
</template>
