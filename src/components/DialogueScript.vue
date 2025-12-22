<script setup lang="ts">
/**
 * @author xiaobin
 */
interface Segment {
  id: string;
  role: string;
  text: string;
  translation: string;
  startTime: number;
  endTime: number;
}

const props = defineProps<{
  segments: Segment[];
  activeSegmentId: string | null;
  playMode: 'continuous' | 'single' | 'repeat';
  playbackRate: number;
  showTranslation: boolean;
  playbackRates: number[];
}>();

const emit = defineEmits([
  'update:playMode', 
  'update:playbackRate', 
  'update:showTranslation', 
  'segmentClick'
]);

const scrollToActive = (id: string) => {
  const el = document.getElementById(`segment-${id}`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
};

defineExpose({
  scrollToActive
});
</script>

<template>
  <div class="lg:col-span-7">
    <!-- Section Title & Controls -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-gray-100 to-gray-50 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4 text-gray-600">
            <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 0 1 .865-.501 48.172 48.172 0 0 0 3.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0 0 12 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018Z" />
          </svg>
        </div>
        <h2 class="text-sm font-bold text-gray-900 uppercase tracking-wide">Dialogue Script</h2>
      </div>
      
      <div class="flex items-center gap-3">
        <!-- Play Mode Toggle -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <button 
            @click="emit('update:playMode', 'continuous')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'continuous' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            连读
          </button>
          <button 
            @click="emit('update:playMode', 'single')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'single' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            点读
          </button>
          <button 
            @click="emit('update:playMode', 'repeat')"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="playMode === 'repeat' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            循环
          </button>
        </div>

        <!-- Speed Selector -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <select 
            :value="playbackRate"
            @change="(e) => emit('update:playbackRate', parseFloat((e.target as HTMLSelectElement).value))"
            class="appearance-none bg-transparent px-2.5 py-1 text-[10px] font-bold text-gray-500 hover:text-blue-600 transition-all cursor-pointer outline-none"
          >
            <option v-for="rate in playbackRates" :key="rate" :value="rate">
              {{ rate === 1.0 ? '1.0x' : rate + 'x' }}
            </option>
          </select>
        </div>

        <!-- Language Toggle -->
        <div class="flex items-center bg-gray-100/80 p-0.5 rounded-lg border border-gray-200/50">
          <button 
            @click="emit('update:showTranslation', false)"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="!showTranslation ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            EN
          </button>
          <button 
            @click="emit('update:showTranslation', true)"
            class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all duration-200"
            :class="showTranslation ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
          >
            EN+CN
          </button>
        </div>
      </div>
    </div>

    <!-- Script Cards -->
    <div class="max-h-[620px] overflow-y-auto pr-4 -mr-4 space-y-2.5">
      <div 
        v-for="s in segments" 
        :key="s.id"
        :id="`segment-${s.id}`"
        class="script-card group relative cursor-pointer"
        @click="emit('segmentClick', s)"
      >
        <div 
          class="relative p-3.5 rounded-xl transition-all duration-300 border"
          :class="[
            activeSegmentId === s.id 
              ? 'bg-white shadow-xl shadow-blue-500/5 border-blue-100 scale-[1.01]' 
              : 'bg-white/50 border-transparent hover:bg-white hover:shadow-lg hover:border-gray-100'
          ]"
        >
          <div class="flex items-start gap-3">
            <!-- Avatar -->
            <div 
              class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-bold shadow-sm transition-transform duration-300 group-hover:scale-110"
              :class="[
                s.role === 'Man' ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' : 
                s.role === 'Woman' ? 'bg-gradient-to-br from-indigo-500 to-violet-600 text-white' :
                'bg-gradient-to-br from-slate-500 to-slate-600 text-white'
              ]"
            >
              {{ s.role[0] }}
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-baseline gap-2">
                <span class="flex-shrink-0 text-[10px] font-black text-gray-400 uppercase tracking-wide">{{ s.role }}:</span>
                <p 
                  class="text-sm leading-relaxed transition-colors duration-300"
                  :class="activeSegmentId === s.id ? 'text-gray-900 font-semibold' : 'text-gray-600'"
                >
                  {{ s.text }}
                </p>
              </div>
              <p 
                v-if="showTranslation" 
                class="text-[11px] mt-1 ml-0 text-gray-400 font-medium leading-relaxed animate-fade-in"
              >
                {{ s.translation }}
              </p>
            </div>
            
            <!-- Play Indicator (Removed for static segments) -->
            <div 
              v-if="s.startTime !== undefined"
              class="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center transition-all duration-300"
              :class="activeSegmentId === s.id ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-400 opacity-0 group-hover:opacity-100'"
            >
              <svg v-if="activeSegmentId !== s.id" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
              </svg>
              <div v-else class="flex gap-0.5 items-end h-3">
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.2s_infinite]"></div>
                <div class="w-0.5 bg-white rounded-full animate-[eq_0.8s_ease-in-out_0.4s_infinite]"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.script-card {
  -webkit-tap-highlight-color: transparent;
}
@keyframes eq {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
