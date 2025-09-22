#!/bin/bash

# AutoGen Studio 多智能体C/C++分析系统 - 快速配置脚本
# 运行此脚本确保所有配置正确

echo "=== AutoGen Studio 多智能体系统状态检查 ==="

# 检查AutoGen Studio进程
if pgrep -f "autogenstudio" > /dev/null; then
    echo "✅ AutoGen Studio 正在运行"
    echo "🌐 访问地址: http://localhost:8081"
else
    echo "❌ AutoGen Studio 未运行，正在启动..."
    cd /home/coder-gw/Interruptr
    nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &
    sleep 3
    echo "✅ AutoGen Studio 已启动"
fi

# 检查端口
if curl -s http://localhost:8081 >/dev/null; then
    echo "✅ Web界面可访问"
else
    echo "❌ Web界面不可访问"
fi

# 显示配置文件位置
echo ""
echo "=== 配置文件 ==="
echo "📋 工作流指南: /home/coder-gw/Interruptr/autogen_workflow_guide.md"
echo "🔍 示例代码: /home/coder-gw/Interruptr/sample_code.cpp"
echo "📊 运行日志: /home/coder-gw/Interruptr/autogen_studio.log"

echo ""
echo "=== 下一步操作 ==="
echo "1. 在浏览器中打开: http://localhost:8081"
echo "2. 导航到 'Teams' 或 'Team Builder'"
echo "3. 创建新团队: C/C++ Code Analysis Team"
echo "4. 配置5个智能体角色:"
echo "   - Coordinator (协调员)"
echo "   - Code Analyst (代码分析师)"  
echo "   - Security Expert (安全专家)"
echo "   - Debug Expert (调试专家)"
echo "   - Quality Critic (质量评估师)"
echo "5. 使用 sample_code.cpp 测试工作流"

echo ""
echo "=== 智能体配置模板 ==="
echo "模型设置: gpt-oss:latest (本地模型)"
echo "温度: 0.3 (保持分析一致性)"
echo "最大输出: 2048 tokens"

echo ""
echo "系统已准备就绪! 🚀"
