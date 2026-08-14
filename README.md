# C/C++ Multi-Agent Code Analysis System - Deployment Complete

## 🎉 System Status

- ✅ **AutoGen Studio**: Started and running in the background (`http://localhost:8081`)
- ✅ **Multi-Agent Framework**: Uses the official AutoGen Studio instead of a custom web UI
- ✅ **Local LLM**: Supports `gpt-oss:latest` (optimized for your dual RTX 3090 hardware)
- ✅ **Process Management**: Runs in the background without blocking the terminal
- ✅ **Example Code**: Includes test files covering various typical C++ issues

## 📁 Created Files

1. `autogen_workflow_guide.md` - Detailed workflow configuration guide
2. `sample_code.cpp` - Test C++ code containing security, performance, and memory-management issues
3. `setup_check.sh` - System status checking script
4. `autogen_studio.log` - AutoGen Studio runtime log

## 🤖 Multi-Agent Team Design

### Agent Roles

1. **Coordinator** - Task assignment and progress management
2. **Code Analyst** - Structural and algorithm analysis
3. **Security Expert** - Vulnerability and security issue detection
4. **Debugging Expert** - Error diagnosis and performance analysis
5. **Quality Evaluator** - Overall assessment and improvement recommendations

### Message-Passing Workflow

```text
User Code Input
      ↓
Coordinator Receives Task
      ↓
Parallel Analysis (3 Experts)
      ↓
Coordinator Aggregates Results
      ↓
Quality Evaluator Generates Final Report
      ↓
Output Results
```

## 🌐 Web Interface Usage

### Immediate Access

- **URL**: `http://localhost:8081`
- **Status**: ✅ Already opened in VS Code Simple Browser
- **Background Execution**: Does not block the terminal

### Configuration Steps

1. Open the AutoGen Studio Web interface
2. Click **"Teams"** or **"Team Builder"**
3. Create a new team named **"C/C++ Code Analysis Team"**
4. Create an agent for each role using the system prompts provided in the guide
5. Configure the model as `gpt-oss:latest`
6. Configure the workflow and message-passing logic
7. Use `sample_code.cpp` to test the analysis workflow

## 📊 Test Scenarios

### Example Code Issues Covered

- **Security Vulnerabilities**: Buffer overflows, hardcoded passwords, access-control issues
- **Memory Management**: Memory leaks, unreleased resources, null-pointer risks
- **Algorithm Efficiency**: Inefficient sorting, linear searches, string operations
- **Programming Practices**: Missing boundary checks, incomplete error handling, RAII violations

### Expected Analysis Output

- A professional analysis report from each expert
- The collaboration and conversation process between agents
- A final comprehensive quality assessment and improvement recommendations
- Complete code-analysis documentation

## 🔄 Agent-to-Agent Message Flow Demonstration

In the AutoGen Studio Playground, you will see:

1. The **Coordinator** assigns tasks to each expert
2. The **Code Analyst** analyzes architecture and algorithms
3. The **Security Expert** identifies security risks
4. The **Debugging Expert** identifies performance issues
5. The **Quality Evaluator** consolidates all opinions and provides the final assessment

## 🚀 Ready to Use!

All custom web UI components have been removed. The project now uses the official AutoGen Studio tools to implement genuine multi-agent collaboration.

You can:

1. **Start immediately**: Open `http://localhost:8081`
2. **View conversations**: Observe real-time message passing between agents
3. **Analyze code**: Use the provided example code to test analysis capabilities
4. **Customize workflows**: Adjust agent configurations according to your requirements

### Key Improvements

- ❌ Removed all custom demos and web UI code
- ✅ Uses the official AutoGen multi-agent framework
- ✅ Real agent-to-agent message passing
- ✅ Observable conversation and source-code processing workflow
- ✅ Runs in the background without blocking the terminal

**The system is fully ready. Start your multi-agent C/C++ code-analysis journey!** 🎯

---

## 📂 Project Structure

```text
├── execution_tracer.py   # Execution tracing
├── gdb_controller.py     # GDB controller
├── api/                  # API service
│   └── main.py           # FastAPI main application
├── frontend/             # Frontend interface
│   └── app.py            # Streamlit application
├── config/               # Configuration files
│   └── settings.py       # Project configuration
├── examples/             # Example code
│   └── unsafe_code.c     # Test case
├── tests/                # Test cases
└── requirements.txt      # Dependencies
```

## 🛠️ Environment Setup

### 1. Create a Conda Environment

```bash
conda create -n interruptr python=3.11 -y
conda activate interruptr
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install System Tools

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y gcc gdb valgrind cppcheck clang-tools

# CentOS/RHEL
sudo yum install -y gcc gdb valgrind cppcheck clang-tools-extra

# macOS
brew install gcc gdb valgrind cppcheck llvm
```

## 🚀 Quick Start

### 1. Initialize the Environment

```bash
# Run the configuration check script
python3 setup.py

# Edit the environment configuration file
nano .env
```

### 2. Configure API Keys

Add your API keys to the `.env` file:

```bash
# OpenAI API (recommended for conversation visualization)
OPENAI_API_KEY=your-openai-api-key-here

# Or Anthropic Claude API (recommended for code analysis)
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. Start the Services

```bash
./start.sh
```

Select a startup mode:

* 1. API service only (port 8000)
* 2. Frontend interface only (port 8501)
* 3. Start both
* 4. Run example analysis

## 📊 Usage Example

### Analyze the Example Code

The project provides an example file, `examples/unsafe_code.c`, containing common security issues:

```c
void unsafe_copy(char* source) {
    char buffer[100];
    strcpy(buffer, source);  // Potential buffer overflow
    printf("Copied: %s\\n", buffer);
}
```

Interruptr will identify and report:

- 🚨 **High Risk**: Buffer overflow vulnerability
- 💡 **Recommendation**: Use `strncpy` or `snprintf` instead
- 🎯 **Breakpoint**: Set a breakpoint before the `strcpy` call for inspection

## 🎯 Multi-Agent Framework Selection

### AutoGen vs. LangGraph Comparison

| Feature                        | AutoGen             | LangGraph                  | Recommended Use Case           |
| ------------------------------ | ------------------- | -------------------------- | ------------------------------ |
| **Conversation Visualization** | ✅ Built-in support  | ⚠️ Requires customization  | Real-time conversation display |
| **Workflow Visualization**     | ⚠️ Simple workflows | ✅ Complex graph structures | Workflow orchestration         |
| **State Management**           | ⚠️ Basic            | ✅ Powerful                 | Complex state tracking         |
| **Development Difficulty**     | 🟢 Easy             | 🟡 Moderate                | Rapid prototyping              |
| **Extensibility**              | 🟡 Moderate         | 🟢 Excellent               | Large-scale projects           |

### Hybrid Architecture of This Project

**Reason for Selection: Combining the Advantages of Both**

1. **AutoGen** is used for:

   - Real-time communication between agents
   - User interaction interface
   - Rapid prototyping and demonstrations

2. **LangGraph** is used for:

   - Complex analysis workflow orchestration
   - State management and persistence
   - Conditional branching and loop logic

```python
# Example: Hybrid usage
from autogen_agentchat.teams import RoundRobinGroupChat
from langgraph.graph import StateGraph

# AutoGen handles conversations
agents = [code_analyst, security_expert, debug_expert]
chat_team = RoundRobinGroupChat(agents)

# LangGraph handles workflows
workflow = StateGraph(AnalysisState)
workflow.add_node("parse_code", parse_code_node)
workflow.add_node("security_scan", security_scan_node)
workflow.add_edge("parse_code", "security_scan")
```

## 🔧 Configuration

### Environment Variables

The project uses a `.env` file to manage configuration:

```bash
# Required configuration
OPENAI_API_KEY=your-openai-key          # OpenAI API key
ANTHROPIC_API_KEY=your-anthropic-key    # Anthropic API key

# Optional configuration
DEFAULT_LLM_PROVIDER=openai             # Default LLM provider
API_HOST=localhost                      # API service host
API_PORT=8000                            # API service port
SECURITY_LEVEL=high                     # Security detection level
MAX_FILE_SIZE=10                         # Maximum file size (MB)
```

### Configuration File

The following settings can be customized in `config/settings.py`:

- Agent behavior parameters
- Security detection rules
- Analysis tool paths
- Database connection

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/

# Check code quality
flake8 src/
mypy src/
```

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📈 Roadmap

### v0.2.0 (Planned)

- [ ] Improve the AutoGen + LangGraph hybrid architecture
- [ ] Implement a real-time conversation visualization interface
- [ ] Support more programming languages (Java, Python)
- [ ] Integrate more static-analysis tools
- [ ] Add CI/CD integration

### v0.3.0 (Planned)

- [ ] Distributed multi-agent collaboration
- [ ] Real-time code monitoring and hot reload
- [ ] Custom rule engine and plugin system
- [ ] Team collaboration and permission management
- [ ] Performance optimization and caching mechanisms

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Development Team**: Interruptr Development Team
- **Contact**: [Project Issues](https://github.com/your-org/interruptr/issues)

## 🙏 Acknowledgments

Thanks to the following open-source projects for their support:

- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Workflow orchestration
- [Tree-sitter](https://tree-sitter.github.io/) - Syntax parsing
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Streamlit](https://streamlit.io/) - Frontend framework

---

🚀 **Make code analysis smarter and debugging more efficient!**
