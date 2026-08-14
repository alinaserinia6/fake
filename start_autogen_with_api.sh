#!/bin/bash

# AutoGen Studio environment variable setup and startup script
# Extracts API keys from the .env file and starts AutoGen Studio

echo "🚀 Starting AutoGen Studio with API key configuration"
echo "=================================================="

# Set working directory
cd /home/coder-gw/Interruptr

# Read API keys from the .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
    echo "✅ Loaded API keys from .env file"
else
    echo "⚠️  .env file not found. Please copy from .env.example and configure"
    echo "   cp .env.example .env"
    echo "   Then edit the .env file and fill in your real API keys"
    exit 1
fi

# Set local Ollama configuration
export OLLAMA_BASE_URL="http://localhost:11434"

# Verify that API keys were set successfully
echo "✅ Environment variables configured:"
echo "   OpenAI API Key: ${OPENAI_API_KEY:0:10}..."
echo "   Anthropic API Key: ${ANTHROPIC_API_KEY:0:10}..."
echo "   Gemini API Key: ${GEMINI_API_KEY:0:10}..."
echo "   Ollama URL: $OLLAMA_BASE_URL"

# Stop any existing AutoGen Studio process
echo ""
echo "🛑 Stopping any existing AutoGen Studio processes..."
pkill -f "autogenstudio" 2>/dev/null || echo "   No running AutoGen Studio process found"

# Wait for the process to fully stop
sleep 2

# Start AutoGen Studio (run in background, loading environment variables)
echo ""
echo "🚀 Starting AutoGen Studio (with API keys)..."
nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &

# Wait for startup
sleep 5

# Check startup status
if pgrep -f "autogenstudio" > /dev/null; then
    echo "✅ AutoGen Studio started successfully!"
    echo "🌐 Access URL: http://localhost:8081"
    echo "📋 Log file: autogen_studio.log"
    
    # Check if the service is responding
    echo ""
    echo "🔍 Checking service status..."
    if curl -s http://localhost:8081 >/dev/null 2>&1; then
        echo "✅ Web service is responding"
        echo ""
        echo "🎯 You can now create teams in AutoGen Studio!"
        echo "   API keys are configured correctly; validation issues should be resolved."
    else
        echo "⚠️  Web service may still be starting up; please wait a moment"
    fi
else
    echo "❌ AutoGen Studio failed to start"
    echo "📋 Please check the log: tail -f autogen_studio.log"
fi

echo ""
echo "📚 Next steps:"
echo "1. Visit http://localhost:8081"
echo "2. Go to Team Builder"
echo "3. Create a new team (API validation issues should be resolved)"
echo "4. Use the prepared configuration files to set up agents"
