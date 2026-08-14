#!/bin/bash

# Interruptr Project Startup Script

echo "🚀 Starting Interruptr - Advanced Multi-Agent C/C++ Code Debugging and Analysis Tool"
echo "========================================"

# Check conda environment
if [[ "$CONDA_DEFAULT_ENV" != "interruptr" ]]; then
    echo "⚠️  Please activate the conda environment first: conda activate interruptr"
    exit 1
fi

# Check required tools
echo "🔍 Checking system tools..."

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
    echo "❌ Missing tools: ${missing_tools[*]}"
    echo "Please run: sudo apt install -y ${missing_tools[*]}"
    exit 1
fi

# Check Python packages
echo ""
echo "🔍 Checking Python dependencies..."

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
    print(f'\\nMissing packages: {missing}')
    print('Please run: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('\\n🎉 All dependencies installed')
"

if [ $? -ne 0 ]; then
    exit 1
fi

echo ""
echo "🎯 Select startup mode:"
echo "1) Start API service"
echo "2) Start frontend interface"
echo "3) Start both API and frontend"
echo "4) Run example analysis"

read -p "Please select (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting API service..."
        cd api && python main.py
        ;;
    2)
        echo "🚀 Starting frontend interface..."
        cd frontend && streamlit run app.py
        ;;
    3)
        echo "🚀 Starting both API and frontend..."
        echo "Starting API service..."
        cd api && python main.py &
        API_PID=$!
        sleep 3
        
        echo "Starting frontend interface..."
        cd ../frontend && streamlit run app.py &
        FRONTEND_PID=$!
        
        echo "API PID: $API_PID"
        echo "Frontend PID: $FRONTEND_PID"
        echo "Press Ctrl+C to stop all services"
        
        # Wait for signal
        trap "kill $API_PID $FRONTEND_PID; exit" INT
        wait
        ;;
    4)
        echo "🔍 Running example analysis..."
        cd examples
        echo "Compiling example code..."
        gcc -g -o unsafe_code unsafe_code.c
        
        echo "Running static analysis..."
        cppcheck --enable=all unsafe_code.c
        
        echo "Running memory check..."
        valgrind --tool=memcheck --leak-check=full ./unsafe_code 2>&1 | head -20
        
        echo "Analysis complete! You can upload this file in the frontend interface for agent-based analysis."
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
