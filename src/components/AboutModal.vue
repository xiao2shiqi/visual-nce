<script setup lang="ts">
import { ref } from 'vue';

const showAboutModal = ref(false);

const openAbout = () => {
  showAboutModal.value = true;
};

const closeAbout = () => {
  showAboutModal.value = false;
};

defineExpose({ openAbout });
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="showAboutModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeAbout">
        <div class="bg-white w-full max-w-2xl rounded-3xl shadow-2xl p-8 md:p-10 relative overflow-hidden animate-scale-up">
          
          <!-- Close Button -->
          <button @click="closeAbout" class="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Content -->
          <div class="space-y-8">
            <div class="text-center">
              <h2 class="text-2xl font-black text-slate-800 mb-2">关于 Visual NCE</h2>
              <p class="text-slate-500 font-medium text-sm">About This Project</p>
            </div>

            <!-- Disclaimer Section -->
            <div class="bg-slate-50 rounded-2xl p-6 border border-slate-100">
              <h3 class="text-sm font-black text-red-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                  <path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                </svg>
                免责声明 / Disclaimer
              </h3>
              <div class="space-y-4 text-sm text-slate-600 leading-relaxed text-justify">
                <p>
                  <strong class="text-slate-800">非盈利性质与版权归属：</strong><br>
                  本站（Visual NCE）是一个<strong class="text-slate-800">非盈利性的个人开源学习项目</strong>，仅用于现代 Web 技术展示与个人编程学习研究。
                  网站内使用的《新概念英语》(New Concept English) 相关文本、音频及课程结构，其版权均归原作者 <strong>L.G. Alexander</strong> 及出版商 <strong>Pearson Education (培生教育集团)</strong> 所有。
                </p>
                <p>
                  <strong class="text-slate-800">合理使用说明：</strong><br>
                  本项目旨在通过可视化技术辅助语言学习，所有重制内容（如AI生成的图片）仅为教学辅助。本站不进行任何形式的商业变现（无广告、无会员、无销售），也不提供任何官方教材的电子书下载。
                </p>
                <p>
                  <strong class="text-slate-800">侵权处理：</strong><br>
                  本站与 Pearson Education 无任何关联。如果您是版权所有者并认为本站内容侵犯了您的权益，请通过邮件联系，我将在确认后立即删除相关内容。
                </p>
              </div>
            </div>

            <!-- Support Section -->
            <div class="text-center space-y-4 pt-4 border-t border-slate-100">
              <h3 class="text-xs font-black text-amber-500 uppercase tracking-widest flex items-center justify-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                  <path d="M12.75 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM7.5 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM8.25 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM9.75 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM10.5 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM12.75 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM14.25 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM15 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM16.5 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM15 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM16.5 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" />
                  <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 0 1 7.5 3v1.5h9V3A.75.75 0 0 1 18 3v1.5h.75a3 3 0 0 1 3 3v11.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V7.5a3 3 0 0 1 3-3H6V3a.75.75 0 0 1 .75-.75Zm13.5 9a1.5 1.5 0 0 0-1.5-1.5H5.25a1.5 1.5 0 0 0-1.5 1.5v7.5a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5v-7.5Z" clip-rule="evenodd" />
                </svg>
                支持项目 / Support
              </h3>
              
              <div class="bg-amber-50/50 rounded-2xl p-6 inline-block shadow-sm border border-amber-100/50">
                <img src="/images/sponsor.jpg" alt="WeChat Pay Sponsor Code" class="w-48 h-48 rounded-xl mx-auto mb-3 shadow-md mix-blend-multiply" />
                <p class="text-[10px] text-amber-800/60 font-medium">长按识别或扫码</p>
              </div>
            </div>

            <!-- Contact Section -->
            <div class="text-center space-y-2">
              <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">联系开发者 / Contact</p>
              <a href="mailto:xiaobin.phoenix@gmail.com" class="text-blue-600 font-bold hover:underline transition-all">
                xiaobin.phoenix@gmail.com
              </a>
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
</style>
