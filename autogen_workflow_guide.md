# AutoGen Studio Multi-Agent C/C++ Code Analysis Workflow Configuration Guide

## ⚠️ Important: API Key Configuration

### 🔑 Why Are API Keys Needed?

AutoGen Studio requires API keys to create teams and agents. Without configured API keys, validation errors will occur and team features cannot be used.

### ✅ API Keys Have Been Automatically Configured

We have already configured the complete API key environment for you:

- **OpenAI API** - For GPT models
- **Anthropic API** - For Claude models
- **Google Gemini API** - For Gemini models
- **Local Ollama** - For gpt-oss:latest model

### 🚀 Restart AutoGen Studio (Completed)

```bash
# The following has been executed for you:
./start_autogen_with_api.sh
```

✅ AutoGen Studio is now running with the correct API keys at <http://localhost:8081>

## 🎯 About File Upload vs. Manual Configuration

### File Upload Method ✅

AutoGen Studio supports multiple configuration methods:

1. **JSON Configuration Import** - We have already prepared a complete configuration file for you
2. **Agent Prompt Files** - Detailed prompts for each role have been saved separately
3. **Batch Configuration Script** - Automated configuration tool

### Manual Drag-and-Drop Configuration ✅

In AutoGen Studio's Team Builder:

- Drag to adjust connection relationships between agents
- Visually edit workflow diagrams
- Real-time preview of message routing paths

## 🚀 Quick Configuration Methods

### Method 1: Using Configuration Files (Recommended)

1. **Run the configuration tool**:

   ```bash
   cd /home/coder-gw/Interruptr
   python configure_agents.py
   ```

2. **Files have been automatically generated**:

   - `agent_configs.json` - Complete team configuration
   - `agent_prompts/` - Prompt files for each agent
   - Detailed configuration guide

3. **Use in AutoGen Studio**:
   - Visit <http://localhost:8081>
   - When creating a new team, refer to the JSON configuration
   - Copy and paste the corresponding prompt file contents

### Method 2: Visual Drag-and-Drop Configuration

1. **Access Team Builder**:
   - Open <http://localhost:8081>
   - Click "Teams" or "Team Builder"

2. **Create Agents**:
   - Drag to create 5 Agent nodes
   - Set role names and descriptions
   - Paste the corresponding system prompts

3. **Configure Workflow**:
   - Drag connection lines to set message routing paths
   - Set parallel/serial execution modes
   - Configure termination conditions

## 📁 Prepared Configuration Files

```txt
/home/coder-gw/Interruptr/
├── agent_configs.json           # Complete team configuration file
├── agent_prompts/              # Agent prompts directory
│   ├── coordinator_prompt.txt     # Coordinator prompt
│   ├── code_analyst_prompt.txt    # Code Analyst prompt
│   ├── security_expert_prompt.txt # Security Expert prompt
│   ├── debug_expert_prompt.txt    # Debug Expert prompt
│   └── quality_critic_prompt.txt  # Quality Critic prompt
└── configure_agents.py         # Automatic configuration tool
```

## 🤖 Agent Configuration Details

### 1. Coordinator

- **Model**: gpt-oss:latest
- **Temperature**: 0.3 (maintain consistency)
- **Tokens**: 2048
- **File**: `agent_prompts/coordinator_prompt.txt`

### 2. Code_Analyst (Code Analyst)

- **Model**: gpt-oss:latest
- **Temperature**: 0.2 (stricter analysis)
- **Tokens**: 3072
- **File**: `agent_prompts/code_analyst_prompt.txt`

### 3. Security_Expert (Security Expert)

- **Model**: gpt-oss:latest
- **Temperature**: 0.1 (strictest analysis)
- **Tokens**: 3072
- **File**: `agent_prompts/security_expert_prompt.txt`

### 4. Debug_Expert (Debug Expert)

- **Model**: gpt-oss:latest
- **Temperature**: 0.2 (precise diagnostics)
- **Tokens**: 3072
- **File**: `agent_prompts/debug_expert_prompt.txt`

### 5. Quality_Critic (Quality Critic)

- **Model**: gpt-oss:latest
- **Temperature**: 0.3 (comprehensive assessment)
- **Tokens**: 4096 (longest output)
- **File**: `agent_prompts/quality_critic_prompt.txt`

## 🔄 Workflow Configuration

### Message Routing Architecture

```txt
User Input
    ↓
Coordinator (Receive task)
    ↓
┌─────────────────────────────────┐
│     Parallel Analysis Phase     │
├─ Code_Analyst    (Code analysis)│
├─ Security_Expert (Security scan)│  
└─ Debug_Expert    (Debug analysis)│
└─────────────────────────────────┘
    ↓
Coordinator (Collect results)
    ↓
Quality_Critic (Final assessment)
    ↓
Comprehensive Report Output
```

### Configuration Steps in AutoGen Studio

1. **Create Team**:
   - Team Name: `C/C++ Code Analysis Team`
   - Description: `Professional C/C++ code analysis and security review team`

2. **Add Agents** (in the following order):

   ```txt
   Coordinator → Code_Analyst → Security_Expert → Debug_Expert → Quality_Critic
   ```

3. **Set Connection Relationships**:
   - User → Coordinator
   - Coordinator → [Code_Analyst, Security_Expert, Debug_Expert] (parallel)
   - [Code_Analyst, Security_Expert, Debug_Expert] → Coordinator
   - Coordinator → Quality_Critic
   - Quality_Critic → User

4. **Configure Parameters**:
   - Maximum rounds: 10
   - Human input mode: NEVER
   - Termination condition: Quality_Critic completes final report

## 📊 Test Scenarios

### Using Example Code

```bash
# View test code
cat /home/coder-gw/Interruptr/sample_code.cpp
```

### Test Workflow

1. In the AutoGen Studio Playground, select the configured team
2. Input test code or upload a file
3. Observe message passing between agents
4. View analysis results from each expert
5. Obtain the final comprehensive assessment report

## 🛠️ Using the Configuration Tool

### Automatic Configuration Script

```bash
# Run the configuration tool
python configure_agents.py

# Check system status
./setup_check.sh
```

### File Management

- All prompt files can be copied and pasted directly
- The JSON configuration file contains the complete team setup
- Parameters such as temperature and token limits can be modified as needed

## 🎯 Best Practices

### Agent Configuration

1. **Maintain Temperature Consistency**: Security_Expert uses the lowest temperature (0.1) to ensure strict analysis
2. **Allocate Tokens Appropriately**: Quality_Critic needs the most tokens (4096) for comprehensive reports
3. **Clear Role Division**: Each agent focuses on a specific domain

### Workflow Optimisation

1. **Parallel Processing**: Code/Security/Debug analysis can be executed in parallel
2. **Result Aggregation**: Coordinator is responsible for collecting and organising all analysis results
3. **Quality Gatekeeping**: Quality_Critic performs the final comprehensive assessment

### Testing Recommendations

1. **Start Simple**: Use the provided sample_code.cpp to test basic functionality
2. **Observe Conversations**: Pay attention to the message passing process between agents
3. **Adjust Parameters**: Modify temperature and token settings based on actual results

## 🚀 Get Started Now

You now have two configuration methods:

### Quick Configuration (File Upload Method)

1. Use the prepared configuration files and prompts
2. Refer to the JSON configuration when creating a team in AutoGen Studio
3. Copy and paste the corresponding prompt file contents

### Visual Configuration (Drag-and-Drop Method)

1. Manually create and connect agents in Team Builder
2. Drag to set up the workflow diagram
3. Adjust message routing paths in real-time

**Visit <http://localhost:8081> now to start configuring your multi-agent team!** 🎯
