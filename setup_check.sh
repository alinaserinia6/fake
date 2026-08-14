#!/bin/bash

# AutoGen Studio Multi-Agent C/C++ Analysis System - Quick Configuration Script
# Run this script to ensure all configurations are correct

echo "=== AutoGen Studio Multi-Agent System Status Check ==="

# Check AutoGen Studio process
if pgrep -f "autogenstudio" > /dev/null; then
    echo "✅ AutoGen Studio is running"
    echo "🌐 Access URL: http://localhost:8081"
else
    echo "❌ AutoGen Studio is not running, starting..."
    cd /home/coder-gw/Interruptr
    nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &
    sleep 3
    echo "✅ AutoGen Studio has been started"
fi

# Check port
if curl -s http://localhost:8081 >/dev/null; then
    echo "✅ Web interface is accessible"
else
    echo "❌ Web interface is not accessible"
fi

# Display configuration file locations
echo ""
echo "=== Configuration Files ==="
echo "📋 Workflow guide: /home/coder-gw/Interruptr/autogen_workflow_guide.md"
echo "🔍 Example code: /home/coder-gw/Interruptr/sample_code.cpp"
echo "📊 Log file: /home/coder-gw/Interruptr/autogen_studio.log"

echo ""
echo "=== Next Steps ==="
echo "1. Open in your browser: http://localhost:8081"
echo "2. Navigate to 'Teams' or 'Team Builder'"
echo "3. Create a new team: C/C++ Code Analysis Team"
echo "4. Configure 5 agent roles:"
echo "   - Coordinator"
echo "   - Code Analyst"
echo "   - Security Expert"
echo "   - Debug Expert"
echo "   - Quality Critic"
echo "5. Test the workflow using sample_code.cpp"

echo ""
echo "=== Agent Configuration Template ==="
echo "Model: gpt-oss:latest (local model)"
echo "Temperature: 0.3 (maintain analysis consistency)"
echo "Max output: 2048 tokens"

echo ""
echo "System is ready! 🚀"
