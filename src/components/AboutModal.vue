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
      <div v-if="showAboutModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 overlay backdrop-blur-sm" @click.self="closeAbout">
        <div class="bg-raised w-full max-w-2xl rounded-xl shadow-2xl p-8 p-10 relative overflow-hidden animate-scale-up">
          
          <!-- Close Button -->
          <button @click="closeAbout" class="absolute top-4 right-4 p-2 rounded-full hover:bg-hovered transition-colors text-ink-mute hover:text-ink-soft">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Content -->
          <div class="space-y-8">
            <div class="text-center">
              <h2 class="text-2xl font-black text-ink mb-2">关于 Visual NCE</h2>
              <p class="text-ink-soft font-medium text-sm">About This Project</p>
            </div>

            <!-- Disclaimer Section -->
            <div class="bg-hovered rounded-xl p-6 border border-line">
              <h3 class="text-sm font-black text-red-500 uppercase tracking-widest mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
                  <path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                </svg>
                免责声明 / Disclaimer
              </h3>
              <div class="space-y-4 text-sm text-ink-soft leading-relaxed text-justify">
                <p>
                  <strong class="text-ink">非盈利性质与版权归属：</strong><br>
                  本站（Visual NCE）是一个<strong class="text-ink">非盈利性的个人开源学习项目</strong>，仅用于现代 Web 技术展示与个人编程学习研究。
                  网站内使用的《新概念英语》(New Concept English) 相关文本、音频及课程结构，其版权均归原作者 <strong>L.G. Alexander</strong> 及出版商 <strong>Pearson Education (培生教育集团)</strong> 所有。
                </p>
                <p>
                  <strong class="text-ink">合理使用说明：</strong><br>
                  本项目旨在通过可视化技术辅助语言学习，所有重制内容（如AI生成的图片）仅为教学辅助。本站不进行任何形式的商业变现（无广告、无会员、无销售），也不提供任何官方教材的电子书下载。
                </p>
                <p>
                  <strong class="text-ink">侵权处理：</strong><br>
                  本站与 Pearson Education 无任何关联。如果您是版权所有者并认为本站内容侵犯了您的权益，请通过邮件联系，我将在确认后立即删除相关内容。
                </p>
              </div>
            </div>

            <!-- Contact Section -->
            <div class="text-center space-y-4">
              <p class="text-xs font-bold text-ink-mute uppercase tracking-widest">联系开发者 / Contact</p>

              <!-- WeChat QR -->
              <div class="flex flex-col items-center gap-2">
                <img
                  src="/images/wechat_qr.png"
                  alt="作者微信二维码"
                  loading="lazy"
                  class="w-44 h-44 object-contain rounded-xl border border-line shadow-sm bg-raised"
                />
                <p class="text-xs text-ink-mute">微信扫码加好友，进入学习交流群</p>
              </div>

              <div class="space-y-2">
                <div>
                  <a href="https://blog.xiao27.com" target="_blank" class="text-ink font-bold hover:underline transition-all">
                    https://blog.xiao27.com
                  </a>
                </div>

                <div class="text-sm font-medium text-ink-soft">
                  <span class="font-bold text-ink">WeChat:</span> 18198971094
                </div>

                <div>
                  <a href="mailto:xiaobin.phoenix@gmail.com" class="text-sm text-ink-soft hover:text-ink transition-colors">
                    xiaobin.phoenix@gmail.com
                  </a>
                </div>
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
</style>
