#!/bin/bash

# Visual NCE 一键启动脚本

echo "🚀 正在启动 Visual NCE 开发环境..."

# 检查 node_modules 是否存在，不存在则安装
if [ ! -d "node_modules" ]; then
    echo "📦 发现缺失依赖，正在进行 npm install..."
    npm install
fi

# 启动开发服务器
echo "🌐 应用即将运行在 http://localhost:5173"
echo "💡 按 CTRL+C 可停止运行"
echo "----------------------------------------"

npm run dev
