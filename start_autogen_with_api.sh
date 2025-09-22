#!/bin/bash

# AutoGen Studio 环境变量设置和启动脚本
# 从.env文件中提取API密钥并启动AutoGen Studio

echo "🚀 启动AutoGen Studio与API密钥配置"
echo "=" * 50

# 设置工作目录
cd /home/coder-gw/Interruptr

# 从.env文件读取API密钥
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
    echo "✅ 已从.env文件加载API密钥"
else
    echo "⚠️  未找到.env文件，请从.env.example复制并配置"
    echo "   cp .env.example .env"
    echo "   然后编辑.env文件，填入您的真实API密钥"
    exit 1
fi

# 设置本地Ollama配置
export OLLAMA_BASE_URL="http://localhost:11434"

# 验证API密钥是否设置成功
echo "✅ 环境变量设置完成:"
echo "   OpenAI API Key: ${OPENAI_API_KEY:0:10}..."
echo "   Anthropic API Key: ${ANTHROPIC_API_KEY:0:10}..."
echo "   Gemini API Key: ${GEMINI_API_KEY:0:10}..."
echo "   Ollama URL: $OLLAMA_BASE_URL"

# 停止现有的AutoGen Studio进程
echo ""
echo "🛑 停止现有AutoGen Studio进程..."
pkill -f "autogenstudio" 2>/dev/null || echo "   没有发现运行中的AutoGen Studio进程"

# 等待进程完全停止
sleep 2

# 启动AutoGen Studio (后台运行，加载环境变量)
echo ""
echo "🚀 启动AutoGen Studio (带API密钥)..."
nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &

# 等待启动
sleep 5

# 检查启动状态
if pgrep -f "autogenstudio" > /dev/null; then
    echo "✅ AutoGen Studio 启动成功!"
    echo "🌐 访问地址: http://localhost:8081"
    echo "📋 日志文件: autogen_studio.log"
    
    # 检查服务是否响应
    echo ""
    echo "🔍 检查服务状态..."
    if curl -s http://localhost:8081 >/dev/null 2>&1; then
        echo "✅ Web服务正常响应"
        echo ""
        echo "🎯 现在可以在AutoGen Studio中创建团队了!"
        echo "   API密钥已正确配置，验证问题应该解决。"
    else
        echo "⚠️  Web服务可能还在启动中，请稍等片刻"
    fi
else
    echo "❌ AutoGen Studio 启动失败"
    echo "📋 请检查日志: tail -f autogen_studio.log"
fi

echo ""
echo "📚 接下来的步骤:"
echo "1. 访问 http://localhost:8081"
echo "2. 进入Team Builder"
echo "3. 创建新团队 (API验证问题应该已解决)"
echo "4. 使用准备好的配置文件配置智能体"
