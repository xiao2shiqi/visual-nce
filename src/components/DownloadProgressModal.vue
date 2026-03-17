<script setup lang="ts">
import { ref } from 'vue';

/**
 * @author antigravity
 * Refined progress modal matching "Official Site" UI (Tailwind UI / Element Plus style).
 */

const props = defineProps<{
  progress: number;
  isExporting: boolean;
}>();

const isOpen = ref(false);

const open = () => {
  isOpen.value = true;
};

const close = () => {
  if (props.isExporting) return;
  isOpen.value = false;
};

defineExpose({
  open,
  close
});
</script>

<template>
  <teleport to="body">
    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 bg-slate-500/75 backdrop-blur-sm">
        
        <!-- Modal Panel -->
        <div class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-sm sm:p-6">
          <div>
            <!-- Success/Status Icon -->
            <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
              <svg v-if="progress < 100" class="h-6 w-6 text-green-600 animate-spin" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </div>

            <div class="mt-3 text-center sm:mt-5">
              <h3 class="text-base font-semibold leading-6 text-gray-900" id="modal-title">
                {{ progress < 100 ? 'Generating Video...' : 'Generation Complete' }}
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  {{ progress < 100 
                    ? 'Please do not close or refresh this page. We are stitching your lesson illustrations and audio together.' 
                    : 'The video has been successfully generated and is being downloaded.' }}
                </p>
              </div>
            </div>
          </div>

          <!-- Progress Bar Section -->
          <div class="mt-5 sm:mt-6">
            <div class="flex justify-between items-center mb-2">
               <span class="text-xs font-medium text-gray-500 uppercase tracking-wider">Progress</span>
               <span class="text-xs font-bold text-green-600">{{ progress }}%</span>
            </div>
            <div class="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
               <div 
                 class="h-full bg-green-500 transition-all duration-300 ease-out shadow-[0_0_10px_rgba(34,197,94,0.3)]"
                 :style="{ width: progress + '%' }"
               ></div>
            </div>
          </div>

          <!-- Hint Footer (Optional) -->
          <div v-if="!isExporting && progress === 100" class="mt-5 sm:mt-6">
            <button 
              type="button" 
              @click="close"
              class="inline-flex w-full justify-center rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-green-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-600"
            >
              Go back
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>
