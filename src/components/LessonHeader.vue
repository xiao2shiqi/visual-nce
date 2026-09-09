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
  <header class="sticky top-0 z-30 backdrop-blur-md bg-base/85 border-b border-line">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-4 sm:gap-5">
        <!-- Back Button & Theme Toggle -->
        <ThemeToggle />
        <button 
          @click="emit('back')"
          class="flex items-center gap-1.5 p-2 -ml-1 rounded-md hover:bg-hovered text-ink-soft hover:text-ink transition-colors cursor-pointer group"
          title="返回课程目录"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4 group-hover:-translate-x-0.5 transition-transform">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
          </svg>
          <span class="text-xs font-bold hidden sm:inline text-ink-soft group-hover:text-ink">目录</span>
        </button>
        
        <!-- Divider -->
        <div class="h-4 w-px bg-line-strong"></div>

        <!-- Title Area：对齐首页字阶，英文课名采用 font-display 衬线 -->
        <div>
          <h1 class="flex items-center gap-2 flex-wrap leading-tight">
            <template v-if="title.match(/^(Lesson\s+\d+):\s*(.*)/i)">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-hovered text-ink-soft border border-line align-middle shrink-0">
                {{ title.match(/^(Lesson\s+\d+):\s*(.*)/i)![1] }}
              </span>
              <span class="font-display text-xl sm:text-2xl font-bold tracking-tight text-ink align-middle">
                {{ title.match(/^(Lesson\s+\d+):\s*(.*)/i)![2] }}
              </span>
            </template>
            <span v-else class="font-display text-xl sm:text-2xl font-bold tracking-tight text-ink align-middle">
              {{ title }}
            </span>
          </h1>
          <p class="text-[11px] font-mono text-ink-soft flex items-center gap-1.5 mt-0.5">
            <span class="w-1.5 h-1.5 rounded-full bg-btn"></span>
            <span>{{ subtitle || 'New Concept English' }}</span>
          </p>
        </div>
      </div>
      
      <!-- Right Side Actions -->
      <div class="flex items-center gap-3">
        <!-- Support Button -->
        <button 
          @click="emit('supportClick')"
          class="flex items-center gap-2 px-3.5 py-1.5 rounded-md bg-raised border border-line hover:border-line-strong text-xs font-semibold text-ink-soft hover:text-ink transition-colors cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-ink-mute">
            <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
          </svg>
          <span>Support</span>
        </button>

        <!-- Optional Badge -->
        <div v-if="badge" class="hidden sm:flex items-center gap-2 px-3 py-1 bg-hovered rounded-full border border-line">
          <div class="w-1.5 h-1.5 rounded-full bg-btn animate-pulse"></div>
          <span class="text-xs font-mono font-bold text-ink-soft uppercase tracking-wider">{{ badge }}</span>
        </div>
      </div>
    </div>
  </header>
</template>
