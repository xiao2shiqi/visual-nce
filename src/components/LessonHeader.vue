<script setup lang="ts">
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
  <header class="sticky top-0 z-30 backdrop-blur-xl bg-white/70 border-b border-zinc-100/50">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-5">
        <!-- Back Button -->
        <button 
          @click="emit('back')"
          class="group flex items-center gap-2.5 text-zinc-400 hover:text-zinc-900 transition-all duration-300"
        >
          <div class="w-9 h-9 rounded-xl bg-zinc-50 border border-zinc-100 flex items-center justify-center group-hover:bg-zinc-100 group-hover:border-zinc-200 group-hover:scale-105 transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 group-hover:text-zinc-900">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
            </svg>
          </div>
        </button>
        
        <!-- Divider -->
        <div class="h-5 w-px bg-zinc-200"></div>

        <!-- Title Area -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-zinc-900 to-zinc-700 rounded-xl flex items-center justify-center shadow-lg shadow-zinc-900/20">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="white" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-black tracking-tight text-zinc-900">{{ title }}</h1>
            <p class="text-xs text-zinc-400 font-medium">{{ subtitle || 'New Concept English' }}</p>
          </div>
        </div>
      </div>
      
      <!-- Right Side Actions -->
      <div class="flex items-center gap-3">
        <!-- Support Button -->
        <button 
          @click="emit('supportClick')"
          class="flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 backdrop-blur-sm border border-zinc-200 shadow-sm hover:shadow-md hover:scale-105 transition-all duration-300 group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-400 transition-colors">
            <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
          </svg>
          <span class="text-xs font-bold text-zinc-500 group-hover:text-zinc-700">Support</span>
        </button>

        <!-- Original Badge (optional, hidden on mobile) -->
        <div v-if="badge" class="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-zinc-50 to-zinc-100 rounded-full border border-zinc-200/60">
          <div class="w-1.5 h-1.5 rounded-full bg-zinc-900 animate-pulse"></div>
          <span class="text-[10px] font-bold text-zinc-900 uppercase tracking-wider">{{ badge }}</span>
        </div>
      </div>
    </div>
  </header>
</template>
