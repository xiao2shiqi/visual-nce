<script setup lang="ts">
import ThemeToggle from './ThemeToggle.vue';
/**
 * @author xiaobin
 */
defineProps<{
  title: string;
  subtitle?: string;
  badge?: string;
}>();

const emit = defineEmits(['back', 'supportClick']);
</script>

<template>
  <header class="sticky top-0 z-30 backdrop-blur-xl bg-raised border-b border-line/50">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-5">
        <!-- Back Button -->
        <ThemeToggle />
        <button 
          @click="emit('back')"
          class="group flex items-center gap-2.5 text-ink-mute hover:text-ink transition-all duration-300"
        >
          <div class="w-9 h-9 rounded-xl bg-hovered border border-line flex items-center justify-center group-hover:bg-hovered group-hover:border-line group-hover:scale-105 transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 group-hover:text-ink">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
            </svg>
          </div>
        </button>
        
        <!-- Divider -->
        <div class="h-5 w-px bg-line-strong"></div>

        <!-- Title Area -->
        <div class="flex items-center gap-3.5">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-indigo-600 to-blue-600 flex items-center justify-center shadow-md shadow-indigo-500/20 text-white shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <div>
            <h1 class="text-xl sm:text-2xl font-black tracking-tight text-ink flex items-center gap-2 flex-wrap">
              <span v-if="title.match(/^(Lesson\s+\d+):\s*(.*)/i)">
                <span class="inline-flex items-center px-2 py-0.5 rounded-lg text-xs font-black bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400 border border-indigo-200/80 dark:border-indigo-800/60 uppercase tracking-wider mr-1.5 align-middle">
                  {{ title.match(/^(Lesson\s+\d+):\s*(.*)/i)![1] }}
                </span>
                <span class="align-middle">{{ title.match(/^(Lesson\s+\d+):\s*(.*)/i)![2] }}</span>
              </span>
              <span v-else class="align-middle">{{ title }}</span>
            </h1>
            <p class="text-xs text-ink-mute font-medium flex items-center gap-1.5 mt-0.5">
              <span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
              <span>{{ subtitle || 'New Concept English' }}</span>
            </p>
          </div>
        </div>
      </div>
      
      <!-- Right Side Actions -->
      <div class="flex items-center gap-3">
        <!-- Support Button -->
        <button 
          @click="emit('supportClick')"
          class="flex items-center gap-2 px-4 py-2 rounded-full bg-raised backdrop-blur-sm border border-line shadow-sm hover:shadow-md hover:scale-105 transition-all duration-300 group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-ink-mute group-hover:text-ink-mute transition-colors">
            <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
          </svg>
          <span class="text-xs font-bold text-ink-soft group-hover:text-ink">Support</span>
        </button>

        <!-- Original Badge (optional, hidden on mobile) -->
        <div v-if="badge" class="flex items-center gap-2 px-3 py-1.5 bg-hovered rounded-full border border-line">
          <div class="w-1.5 h-1.5 rounded-full bg-btn animate-pulse"></div>
          <span class="text-[10px] font-bold text-ink uppercase tracking-wider">{{ badge }}</span>
        </div>
      </div>
    </div>
  </header>
</template>
