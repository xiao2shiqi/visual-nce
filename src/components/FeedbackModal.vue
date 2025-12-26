<script setup lang="ts">
import { ref } from 'vue';

const showFeedbackModal = ref(false);
const isSubmitting = ref(false);
const isSuccess = ref(false);
const form = ref({
  name: '',
  email: '',
  type: 'suggestion',
  message: ''
});

const openFeedback = () => {
  showFeedbackModal.value = true;
  isSuccess.value = false;
  form.value = { name: '', email: '', type: 'suggestion', message: '' };
};

const closeFeedback = () => {
  showFeedbackModal.value = false;
};

const handleSubmit = async () => {
  if (!form.value.message || !form.value.email) return;

  isSubmitting.value = true;
  
  try {
    const response = await fetch("https://formspree.io/f/xzdbbgoz", {
      method: "POST",
      body: JSON.stringify(form.value),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      isSuccess.value = true;
      setTimeout(() => {
        closeFeedback();
      }, 3000);
    } else {
      alert("提交失败，请稍后重试");
    }
  } catch (error) {
    alert("网络错误，提交失败");
  } finally {
    isSubmitting.value = false;
  }
};

defineExpose({ openFeedback });
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="showFeedbackModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeFeedback">
        <div class="bg-white w-full max-w-lg rounded-3xl shadow-2xl p-8 relative overflow-hidden animate-scale-up">
          
          <!-- Close Button -->
          <button @click="closeFeedback" class="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Content -->
          <div v-if="!isSuccess">
            <h2 class="text-2xl font-black text-slate-800 mb-1">反馈与建议</h2>
            <p class="text-slate-500 text-sm mb-6">Feedback / Suggestions</p>

            <form @submit.prevent="handleSubmit" class="space-y-4">
              <!-- Name & Contact -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold text-slate-500 uppercase mb-1">您的称呼 (Name)</label>
                  <input v-model="form.name" type="text" class="w-full px-4 py-2 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm font-medium text-slate-700" placeholder="怎么称呼您" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-slate-500 uppercase mb-1">联系邮箱 (Email) <span class="text-red-500">*</span></label>
                  <input v-model="form.email" type="email" required class="w-full px-4 py-2 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm font-medium text-slate-700" placeholder="用于接收回复" />
                </div>
              </div>

              <!-- Type -->
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">反馈类型 (Type)</label>
                <div class="flex flex-wrap gap-2">
                  <label v-for="type in [
                    {val: 'suggestion', label: '✨ 功能建议'},
                    {val: 'bug', label: '🐛 Bug 反馈'},
                    {val: 'content', label: '📚 本纠错'},
                    {val: 'other', label: '💬 其他'}
                  ]" :key="type.val" class="cursor-pointer">
                    <input type="radio" v-model="form.type" :value="type.val" class="hidden peer" />
                    <span class="inline-block px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-xs font-bold text-slate-500 peer-checked:bg-blue-50 peer-checked:text-blue-600 peer-checked:border-blue-200 transition-all hover:bg-slate-100">
                      {{ type.label }}
                    </span>
                  </label>
                </div>
              </div>

              <!-- Message -->
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-1">详细内容 (Details) <span class="text-red-500">*</span></label>
                <textarea v-model="form.message" required rows="4" class="w-full px-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all text-sm font-medium text-slate-700 resize-none" placeholder="请详细描述您的建议或遇到的问题..."></textarea>
              </div>

              <!-- Submit Button -->
              <button 
                type="submit" 
                :disabled="isSubmitting"
                class="w-full py-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-sm shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:translate-y-[-1px] active:translate-y-[1px] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2"
              >
                <svg v-if="isSubmitting" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span v-else>提交反馈 (Submit)</span>
              </button>
            </form>
          </div>

          <!-- Success State -->
          <div v-else class="py-12 text-center animate-fade-in">
            <div class="w-16 h-16 bg-green-100 text-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-8 h-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            </div>
            <h3 class="text-xl font-black text-slate-800 mb-2">提交成功！</h3>
            <p class="text-slate-500 text-sm">感谢您的宝贵建议，我们会认真阅读。</p>
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

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
