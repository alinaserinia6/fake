#!/bin/bash

# Interruptr 项目启动脚本

echo "🚀 启动 Interruptr - 高级多智能体C/C++代码调试分析工具"
echo "========================================"

# 检查conda环境
if [[ "$CONDA_DEFAULT_ENV" != "interruptr" ]]; then
    echo "⚠️  请先激活conda环境: conda activate interruptr"
    exit 1
fi

# 检查必要工具
echo "🔍 检查系统工具..."

tools=("gcc" "gdb" "valgrind" "cppcheck")
missing_tools=()

for tool in "${tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        missing_tools+=($tool)
    else
        echo "✅ $tool: $(which $tool)"
    fi
done

if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "❌ 缺少以下工具: ${missing_tools[*]}"
    echo "请运行: sudo apt install -y ${missing_tools[*]}"
    exit 1
fi

# 检查Python包
echo ""
echo "🔍 检查Python依赖..."

python -c "
import sys
required_packages = [
    'fastapi', 'uvicorn', 'streamlit', 'pyautogen', 'langgraph', 
    'langchain', 'openai', 'anthropic', 'pandas', 'numpy'
]

missing = []
for pkg in required_packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        missing.append(pkg)
        print(f'❌ {pkg}')

if missing:
    print(f'\\n缺少包: {missing}')
    print('请运行: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('\\n🎉 所有依赖已安装')
"

if [ $? -ne 0 ]; then
    exit 1
fi

echo ""
echo "🎯 选择启动模式:"
echo "1) 启动API服务"
echo "2) 启动前端界面" 
echo "3) 同时启动API和前端"
echo "4) 运行示例分析"

read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo "🚀 启动API服务..."
        cd api && python main.py
        ;;
    2)
        echo "🚀 启动前端界面..."
        cd frontend && streamlit run app.py
        ;;
    3)
        echo "🚀 同时启动API和前端..."
        echo "启动API服务..."
        cd api && python main.py &
        API_PID=$!
        sleep 3
        
        echo "启动前端界面..."
        cd ../frontend && streamlit run app.py &
        FRONTEND_PID=$!
        
        echo "API PID: $API_PID"
        echo "Frontend PID: $FRONTEND_PID"
        echo "按 Ctrl+C 停止所有服务"
        
        # 等待信号
        trap "kill $API_PID $FRONTEND_PID; exit" INT
        wait
        ;;
    4)
        echo "🔍 运行示例分析..."
        cd examples
        echo "编译示例代码..."
        gcc -g -o unsafe_code unsafe_code.c
        
        echo "运行静态分析..."
        cppcheck --enable=all unsafe_code.c
        
        echo "运行内存检查..."
        valgrind --tool=memcheck --leak-check=full ./unsafe_code 2>&1 | head -20
        
        echo "分析完成! 你可以在前端界面中上传此文件进行智能体分析。"
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
