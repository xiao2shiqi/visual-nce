<script setup lang="ts">
import { ref } from 'vue';
import { exportToMp4, type VideoSegment } from '../utils/videoExporter';
import DownloadProgressModal from './DownloadProgressModal.vue';

/**
 * @author antigravity
 * Premium download button with Ghibli-inspired aesthetics.
 * Supports icon-only mode for overlay placement and progress modal.
 */

const props = defineProps<{
  title: string;
  audioSrc: string;
  segments: VideoSegment[];
  iconOnly?: boolean;
}>();

const isExporting = ref(false);
const progress = ref(0);
const progressModalRef = ref<any>(null);

const handleDownload = async (e: MouseEvent) => {
  e.stopPropagation(); // Prevent player play/pause toggle when clicking icon
  if (isExporting.value) return;
  
  try {
    isExporting.value = true;
    progress.value = 0;
    progressModalRef.value?.open();
    
    const blob = await exportToMp4({
      title: props.title,
      audioSrc: props.audioSrc,
      segments: props.segments,
      onProgress: (p) => {
        progress.value = Math.round(p);
      }
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const extension = blob.type.includes('mp4') ? 'mp4' : 'webm';
    a.download = `${props.title}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Video export failed:', err);
    alert('Failed to generate video. Please try again.');
  } finally {
    isExporting.value = false;
    progress.value = 0;
    setTimeout(() => {
      progressModalRef.value?.close();
    }, 500);
  }
};
</script>

<template>
  <div :class="['download-container', iconOnly ? 'absolute top-4 right-4 z-50' : 'mt-6']">
    <DownloadProgressModal 
      ref="progressModalRef"
      :progress="progress"
      :is-exporting="isExporting"
    />
    <button 
      @click="handleDownload"
      :disabled="isExporting"
      :title="isExporting ? `Generating Video ${progress}%` : 'Download Lesson Video (MP4)'"
      class="group relative overflow-hidden flex items-center justify-center cursor-pointer transition-all duration-300 disabled:opacity-70 disabled:translate-y-0 disabled:cursor-not-allowed"
      :class="[
        iconOnly 
          ? 'w-8 h-8 rounded-full bg-black/40 backdrop-blur-xl border border-white/20 hover:bg-black/60 hover:scale-110 active:scale-95' 
          : 'w-full gap-3 px-6 py-4 rounded-2xl bg-gradient-to-br from-teal-500/90 to-emerald-600/90 text-white font-bold shadow-xl shadow-teal-500/20 hover:shadow-2xl hover:shadow-teal-500/30 hover:-translate-y-0.5'
      ]"
    >
      <!-- Background Decorative Elements -->
      <div v-if="!iconOnly" class="absolute inset-0 opacity-20 pointer-events-none">
        <div class="absolute -top-4 -right-4 w-12 h-12 bg-white rounded-full blur-xl"></div>
        <div class="absolute -bottom-4 -left-4 w-16 h-16 bg-teal-200 rounded-full blur-2xl"></div>
      </div>

      <!-- Icon -->
      <div class="relative z-10 flex items-center justify-center">
        <svg v-if="!isExporting" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" :class="[iconOnly ? 'w-3.5 h-3.5 text-white/90' : 'w-5 h-5 group-hover:bounce transition-transform']">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        <div v-else class="relative">
             <div :class="[iconOnly ? 'w-3.5 h-3.5' : 'w-5 h-5', 'border-2 border-white/30 border-t-white rounded-full animate-spin']"></div>
             <span v-if="iconOnly" class="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[7px] font-bold text-white whitespace-nowrap bg-black/60 px-1 rounded shadow-sm">{{ progress }}%</span>
        </div>
      </div>

      <!-- Text (only in non-icon mode) -->
      <span v-if="!iconOnly" class="relative z-10 text-sm tracking-wide uppercase">
        {{ isExporting ? `Generating Video ${progress}%` : 'Download Lesson Video (MP4)' }}
      </span>

      <!-- Progress Overlay -->
      <div 
        v-if="isExporting && !iconOnly"
        class="absolute inset-0 bg-white/10 origin-left transition-transform duration-300"
        :style="{ transform: `scaleX(${progress / 100})` }"
      ></div>

      <!-- Shine Effect -->
      <div class="absolute inset-0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-[-20deg]"></div>
    </button>
    
    <p v-if="!iconOnly" class="mt-2 text-[10px] text-center text-slate-400 font-medium uppercase tracking-widest opacity-60">
      Combines current lesson's illustrations and audio
    </p>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.group-hover\:bounce {
  animation: bounce 1s infinite;
}

button {
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
