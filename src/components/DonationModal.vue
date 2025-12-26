<script setup lang="ts">
import { ref } from 'vue';
import donationsData from '../data/donations.json';

const showDonationModal = ref(false);
const donations = ref(donationsData);

const openDonation = () => {
  showDonationModal.value = true;
};

const closeDonation = () => {
  showDonationModal.value = false;
};

defineExpose({ openDonation });
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="showDonationModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeDonation">
        <div class="bg-white w-full max-w-2xl rounded-3xl shadow-2xl p-8 md:p-10 relative overflow-hidden animate-scale-up">
          
          <!-- Close Button -->
          <button @click="closeDonation" class="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Content -->
          <div class="space-y-8">
            <div class="text-center">
              <h2 class="text-2xl font-black text-slate-800 mb-2">支持 Visual NCE</h2>
              <p class="text-slate-500 font-medium text-sm">Support This Project</p>
            </div>

            <!-- Support Section -->
            <div class="text-center space-y-4 pt-4">              
              <div class="bg-amber-50/50 rounded-2xl p-6 inline-block shadow-sm border border-amber-100/50">
                <img src="/images/sponsor.jpg" alt="WeChat Pay Sponsor Code" class="w-64 h-64 rounded-xl mx-auto mb-3 shadow-md mix-blend-multiply" />
                
                <div class="bg-white/60 rounded-lg px-4 py-2 border border-amber-200/50 text-center max-w-[240px] mx-auto">
                  <p class="text-[10px] text-amber-900 font-medium leading-tight">
                    您在打赏时的备注将作为昵称<br>展示在下方的捐助名单中
                  </p>
                </div>
              </div>

              <!-- Donation List -->
              <div class="max-w-md mx-auto mt-8">
                <h4 class="text-sm font-bold text-slate-800 mb-4 flex items-center justify-center gap-2">
                  <span class="w-8 h-[1px] bg-slate-200"></span>
                  捐助名单 / Hall of Fame
                  <span class="w-8 h-[1px] bg-slate-200"></span>
                </h4>

                <div class="bg-white border border-slate-100 rounded-xl overflow-hidden shadow-sm">
                  <!-- Header -->
                  <div class="grid grid-cols-3 bg-slate-50 px-4 py-2 text-xs font-bold text-slate-500 border-b border-slate-100">
                    <div class="text-left">昵称 (Name)</div>
                    <div class="text-center">金额 (Amount)</div>
                    <div class="text-right">日期 (Date)</div>
                  </div>
                  
                  <!-- List -->
                  <div class="max-h-48 overflow-y-auto custom-scrollbar">
                    <div v-for="(item, idx) in donations" :key="idx" 
                         class="grid grid-cols-3 px-4 py-3 text-xs border-b border-slate-50 last:border-none hover:bg-slate-50/50 transition-colors items-center">
                      <div class="text-left font-medium text-slate-700 truncate pr-2" :title="item.message || item.name">
                        {{ item.name }}
                      </div>
                      <div class="text-center font-bold text-amber-600">
                        ¥{{ item.amount }}
                      </div>
                      <div class="text-right text-slate-400 font-mono text-[10px]">
                        {{ item.date }}
                      </div>
                    </div>
                  </div>
                </div>
                
                <p class="text-[10px] text-slate-400 mt-2">
                  * 名单将不定期更新，感谢所有的支持与陪伴
                </p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.animate-scale-up {
  animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
</style>
