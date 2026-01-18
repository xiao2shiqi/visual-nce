#!/bin/bash
# 监控 NCE4 翻译进度

echo "================================"
echo "NCE4 翻译进度监控"
echo "================================"
echo ""

# 检查后台任务是否还在运行
if pgrep -f "addTranslationsImproved.ts" > /dev/null; then
    echo "✓ 翻译任务正在运行中..."
    echo ""
else
    echo "✗ 翻译任务已停止或完成"
    echo ""
fi

# 显示最新的输出
echo "最新进度："
echo "--------------------------------"
tail -30 nce4_translation.log | grep -E "(\[.*\]|处理文件|✓|✗|→)" || echo "暂无输出"
echo ""

# 统计已完成的翻译
total_files=48
completed=$(grep -c "✓ 所有翻译已完整" nce4_translation.log 2>/dev/null || echo 0)
updated=$(grep -c "✓ 更新了.*个翻译" nce4_translation.log 2>/dev/null || echo 0)

echo "统计："
echo "--------------------------------"
echo "总课程数: $total_files"
echo "已完成: $((completed + updated))"
echo "进度: $(( (completed + updated) * 100 / total_files ))%"
echo ""
echo "最近更新: $(tail -1 nce4_translation.log)"
