# 🚀 Interruptr User Guide

## Quick Start

### 1. Start the System

```bash
# Full startup
python start.py

# Or start separately
python start.py demo
```

### 2. Access the Interface

- **Frontend Interface**: <http://localhost:8501>
- **API Docs**: <http://localhost:8000/docs>

### 3. Basic Workflow

1. Open the frontend interface
2. Select the "Agent Visualization" tab
3. Upload a C/C++ file or use a sample file
4. Configure analysis options (enable Critic, Reviewer, etc.)
5. Click "Start Multi-Agent Analysis"
6. Watch the real-time analysis process and agent conversations
7. View analysis results and download reports

## System Architecture

### Agent Role Configuration

| Role | LLM Provider | Primary Responsibility |
| ------ | ----------- | ---------- |
| 🎯 Coordinator | OpenAI GPT-4 | Process management and task allocation |
| 📊 Code Analyst | Claude-3.5 | Code quality and complexity analysis |
| 🔒 Security Expert | Claude-3.5 | Security vulnerability detection |
| 🐛 Debug Expert | OpenAI GPT-4 | Breakpoint recommendations and debugging strategies |
| 🏛️ Architect | Claude-3.5 | Software architecture evaluation |
| 🤔 Critic | Google Gemini | Critical review |
| ✅ Reviewer | Ollama (Local) | Final quality verification |

### Analysis Flow

1. **Round 1**: Basic Expert Analysis
   - Code Analyst → Quality assessment
   - Security Expert → Vulnerability detection
   - Debug Expert → Breakpoint suggestions
   - Architect → Design assessment

2. **Round 2**: Critique and Review
   - Critic → Critical review
   - Reviewer → Final verification

3. **Round 3**: Comprehensive Report
   - Coordinator → Consolidate all analysis results

## Configuration Instructions

### Environment Variables (.env)

```bash
# LLM API Configuration
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GEMINI_API_KEY=your-gemini-api-key

# Ollama Local Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Role Assignment
COORDINATOR_LLM=openai
CODE_ANALYST_LLM=claude
SECURITY_EXPERT_LLM=claude
DEBUG_EXPERT_LLM=openai
ARCHITECT_LLM=claude
CRITIC_LLM=gemini
REVIEWER_LLM=ollama
```

### Model Configuration

- **OpenAI**: gpt-4 (strong reasoning, suitable for coordination and debugging)
- **Claude**: claude-3-sonnet (strong analytical capabilities, suitable for code and security)
- **Gemini**: gemini-pro (multi-perspective thinking, suitable for critical review)
- **Ollama**: llama2:7b (local inference, independent verification)

## Common Commands

### System Management

```bash
# Start the full system
python start.py

# Run system tests
python start.py test

# View configuration info
python start.py config

# Demo mode
python start.py demo

# Show help
python start.py help
```

### Test Commands

```bash
# Full system test
python test_system.py

# Test the multi-agent system separately
python -c "from agents.enhanced_multi_agent_system import EnhancedMultiAgentSystem; print('✅ Multi-agent system imported successfully')"
```

## Features

### 🎭 Multi-Agent Visualization

- Real-time display of agent status and interactions
- Color-coded conversation timeline
- Analysis progress visualization
- Agent network graph

### 📊 Analysis Features

- **Code Quality**: Complexity, maintainability, readability assessment
- **Security Analysis**: Buffer overflow, memory leak, security vulnerability detection
- **Debugging Suggestions**: Intelligent breakpoint recommendations, debugging strategies
- **Architecture Assessment**: Design patterns, code organization, refactoring suggestions

### 🔍 Advanced Features

- **Critical Review**: Critic role challenges analysis results
- **Independent Verification**: Reviewer role performs final review
- **Multi-round Dialogue**: Collaborative reasoning between agents
- **Visual Monitoring**: Real-time observation of the analysis process

## Troubleshooting

### Common Issues

1. **API key not configured**

   ```txt
   Solution: Check the API key configuration in the .env file
   ```

2. **Ollama connection failed**

   ```txt
   Solution: Ensure the Ollama service is running
   curl http://localhost:11434/api/tags
   ```

3. **Port is occupied**

   ```txt
   Solution:
   - Frontend: Modify the streamlit port --server.port 8502
   - API: Modify the uvicorn port --port 8001
   ```

4. **Missing dependency packages**

   ```txt
   Solution: Install dependencies from requirements.txt
   pip install -r requirements.txt
   ```

### Debugging Tips

1. **View detailed logs**

   ```bash
   # API logs
   uvicorn api.main:app --log-level debug

   # Streamlit logs
   streamlit run frontend/app.py --logger.level debug
   ```

2. **Test individual components**

   ```bash
   # Test configuration
   python -c "from config.env_config import config; print(config.openai_model)"

   # Test LLM interface
   python -c "import asyncio; from agents.enhanced_multi_agent_system import LLMInterface; asyncio.run(LLMInterface.call_openai('test', 'test'))"
   ```

## Performance Optimization

### Recommended Configuration

- **Concurrency limits**: Set appropriate concurrency for LLM calls
- **Caching**: Enable analysis result caching
- **Timeout settings**: Configure reasonable API call timeouts
- **Local inference**: Use Ollama to reduce API call costs

### Resource Monitoring

- CPU usage (multi-agent parallel processing)
- Memory usage (code analysis and caching)
- Network bandwidth (LLM API calls)
- API quota (avoid exceeding limits)

## Extension Development

### Add a New Agent

1. Define a new role in `EnhancedMultiAgentSystem`
2. Configure the LLM provider and system messages
3. Integrate the new agent into the analysis flow
4. Update the frontend visualization interface

### Support New Languages

1. Add a language parser (tree-sitter)
2. Extend the security rule base
3. Update code quality metrics
4. Adjust analysis templates

### Custom Analyzer

1. Inherit the `EnhancedAgent` class
2. Implement specific analysis logic
3. Register with the multi-agent system
4. Configure frontend interface options

---

## 📞 Technical Support

If you have any questions, please check:

1. System test report: `test_report_*.json`
2. API Docs: <http://localhost:8000/docs>
3. Configuration verification: `python start.py config`
4. Full test: `python start.py test`
