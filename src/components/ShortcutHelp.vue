<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';

const props = withDefaults(defineProps<{
  visible?: boolean;
}>(), {
  visible: false
});

const emit = defineEmits<{
  (e: 'update:visible', val: boolean): void;
  (e: 'close'): void;
}>();

const close = () => {
  emit('update:visible', false);
  emit('close');
};

const handleWindowKeyDown = (e: KeyboardEvent) => {
  if (!props.visible) return;
  if (e.key === 'Escape' || e.code === 'Escape') {
    e.preventDefault();
    close();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleWindowKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleWindowKeyDown);
});

defineExpose({ close });

interface ShortcutItem {
  keys: string[];
  desc: string;
}

interface ShortcutSection {
  title: string;
  items: ShortcutItem[];
}

const shortcutSections: ShortcutSection[] = [
  {
    title: '音频播放与句子导航',
    items: [
      { keys: ['Space'], desc: '播放 / 暂停音频' },
      { keys: ['←'], desc: '跳转至上一句' },
      { keys: ['→'], desc: '跳转至下一句' },
      { keys: ['R'], desc: '重听当前句（从句首重播）' }
    ]
  },
  {
    title: '播放模式与界面视图',
    items: [
      { keys: ['L'], desc: '循环切换播放模式（连读 → 点读 → 循环 → 跟读）' },
      { keys: ['T'], desc: '切换中文译文显示' },
      { keys: ['B'], desc: '切换盲听模式（隐藏台词，专注听力）' }
    ]
  },
  {
    title: '播放速度与系统帮助',
    items: [
      { keys: ['-'], desc: '播放减速一档（0.75x ~ 2.0x）' },
      { keys: ['='], desc: '播放加速一档（0.75x ~ 2.0x）' },
      { keys: ['?'], desc: '打开 / 关闭快捷键帮助' },
      { keys: ['Esc'], desc: '关闭帮助浮层' }
    ]
  }
];
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 overlay backdrop-blur-sm"
        @click.self="close"
      >
        <div class="bg-raised w-full max-w-lg rounded-xl shadow-2xl p-6 sm:p-7 relative border border-line overflow-hidden animate-scale-up">
          <!-- Close Button -->
          <button
            @click="close"
            class="absolute top-4 right-4 p-2 rounded-full hover:bg-hovered transition-colors text-ink-mute hover:text-ink-soft cursor-pointer"
            title="关闭 (Esc)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- Header -->
          <div class="flex items-center gap-3 mb-6">
            <div class="w-9 h-9 rounded-md bg-hovered border border-line flex items-center justify-center text-ink">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h12A2.25 2.25 0 0 1 20.25 6v12A2.25 2.25 0 0 1 18 20.25H6A2.25 2.25 0 0 1 3.75 18V6Z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3.75h9m-9 3.75h4.5" />
              </svg>
            </div>
            <div>
              <h2 class="text-base font-bold text-ink">键盘快捷键指南</h2>
              <p class="text-xs text-ink-soft">精听与跟读快捷键，告别鼠标挪动</p>
            </div>
          </div>

          <!-- Shortcuts Sections -->
          <div class="space-y-5">
            <div v-for="section in shortcutSections" :key="section.title">
              <h3 class="text-[11px] font-bold text-ink-mute uppercase tracking-wider mb-2 px-1">
                {{ section.title }}
              </h3>
              <div class="space-y-1 bg-base rounded-xl p-2 border border-line">
                <div
                  v-for="item in section.items"
                  :key="item.desc"
                  class="flex items-center justify-between py-1.5 px-2 rounded-md hover:bg-hovered transition-colors"
                >
                  <span class="text-xs text-ink font-medium">{{ item.desc }}</span>
                  <div class="flex items-center gap-1">
                    <kbd
                      v-for="k in item.keys"
                      :key="k"
                      class="px-2 py-0.5 text-xs font-mono font-bold text-ink bg-raised border border-line rounded-md shadow-xs min-w-[24px] text-center"
                    >
                      {{ k }}
                    </kbd>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer Note -->
          <div class="mt-5 pt-3 border-t border-line flex items-center justify-between text-[11px] text-ink-mute">
            <span>输入框聚焦时快捷键自动禁用</span>
            <span>按 <kbd class="px-1.5 py-0.5 text-[10px] font-mono font-bold bg-base border border-line rounded-md">Esc</kbd> 关闭</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.animate-scale-up {
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
