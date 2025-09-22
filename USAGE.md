# 🚀 Interruptr 使用指南

## 快速开始

### 1. 启动系统
```bash
# 完整启动
python start.py

# 或者分别启动
python start.py demo
```

### 2. 访问界面
- **前端界面**: http://localhost:8501
- **API文档**: http://localhost:8000/docs

### 3. 基本使用流程
1. 打开前端界面
2. 选择"智能体可视化"标签页
3. 上传C/C++文件或使用示例文件
4. 配置分析选项（启用质疑者、检查者等）
5. 点击"开始多智能体分析"
6. 观看实时分析过程和智能体对话
7. 查看分析结果和下载报告

## 系统架构

### 智能体角色配置
| 角色 | LLM提供商 | 主要职责 |
|------|-----------|----------|
| 🎯 协调者 | OpenAI GPT-4 | 流程管理和任务分配 |
| 📊 代码分析师 | Claude-3.5 | 代码质量和复杂度分析 |
| 🔒 安全专家 | Claude-3.5 | 安全漏洞检测 |
| 🐛 调试专家 | OpenAI GPT-4 | 断点推荐和调试策略 |
| 🏛️ 架构师 | Claude-3.5 | 软件架构评估 |
| 🤔 质疑者 | Google Gemini | 批判性审查 |
| ✅ 检查者 | Ollama本地 | 最终质量验证 |

### 分析流程
1. **第一轮**: 基础专家分析
   - 代码分析师 → 质量评估
   - 安全专家 → 漏洞检测
   - 调试专家 → 断点建议
   - 架构师 → 设计评估

2. **第二轮**: 质疑和审查
   - 质疑者 → 批判性审查
   - 检查者 → 最终验证

3. **第三轮**: 综合报告
   - 协调者 → 整合所有分析结果

## 配置说明

### 环境变量 (.env)
```bash
# LLM API配置
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GEMINI_API_KEY=your-gemini-api-key

# Ollama本地配置
OLLAMA_BASE_URL=http://localhost:11434

# 角色分配
COORDINATOR_LLM=openai
CODE_ANALYST_LLM=claude
SECURITY_EXPERT_LLM=claude
DEBUG_EXPERT_LLM=openai
ARCHITECT_LLM=claude
CRITIC_LLM=gemini
REVIEWER_LLM=ollama
```

### 模型配置
- **OpenAI**: gpt-4 (推理能力强，适合协调和调试)
- **Claude**: claude-3-sonnet (分析能力强，适合代码和安全)
- **Gemini**: gemini-pro (多角度思考，适合批判性审查)
- **Ollama**: llama2:7b (本地推理，独立验证)

## 常用命令

### 系统管理
```bash
# 启动完整系统
python start.py

# 运行系统测试
python start.py test

# 查看配置信息
python start.py config

# 演示模式
python start.py demo

# 显示帮助
python start.py help
```

### 测试命令
```bash
# 完整系统测试
python test_system.py

# 单独测试多智能体系统
python -c "from agents.enhanced_multi_agent_system import EnhancedMultiAgentSystem; print('✅ 多智能体系统导入成功')"
```

## 功能特性

### 🎭 多智能体可视化
- 实时显示智能体状态和交互
- 彩色编码的对话时间线
- 分析进度可视化
- 智能体网络图谱

### 📊 分析功能
- **代码质量**: 复杂度、可维护性、可读性评估
- **安全分析**: 缓冲区溢出、内存泄漏、安全漏洞检测
- **调试建议**: 智能断点推荐、调试策略
- **架构评估**: 设计模式、代码组织、重构建议

### 🔍 高级特性
- **批判性审查**: 质疑者角色质疑分析结果
- **独立验证**: 检查者角色进行最终审核
- **多轮对话**: 智能体之间的协作推理
- **可视化监控**: 实时观察分析过程

## 故障排除

### 常见问题

1. **API密钥未配置**
   ```
   解决方案: 检查.env文件中的API密钥配置
   ```

2. **Ollama连接失败**
   ```
   解决方案: 确保Ollama服务正在运行
   curl http://localhost:11434/api/tags
   ```

3. **端口被占用**
   ```
   解决方案: 
   - 前端: 修改streamlit端口 --server.port 8502
   - API: 修改uvicorn端口 --port 8001
   ```

4. **依赖包缺失**
   ```
   解决方案: 安装requirements.txt中的依赖
   pip install -r requirements.txt
   ```

### 调试技巧

1. **查看详细日志**
   ```bash
   # API日志
   uvicorn api.main:app --log-level debug

   # Streamlit日志
   streamlit run frontend/app.py --logger.level debug
   ```

2. **测试单个组件**
   ```bash
   # 测试配置
   python -c "from config.env_config import config; print(config.openai_model)"

   # 测试LLM接口
   python -c "import asyncio; from agents.enhanced_multi_agent_system import LLMInterface; asyncio.run(LLMInterface.call_openai('test', 'test'))"
   ```

## 性能优化

### 建议配置
- **并发限制**: 设置合适的LLM调用并发数
- **缓存机制**: 启用分析结果缓存
- **超时设置**: 配置合理的API调用超时
- **本地推理**: 使用Ollama减少API调用成本

### 资源监控
- CPU使用率 (多智能体并行处理)
- 内存占用 (代码分析和缓存)
- 网络带宽 (LLM API调用)
- API配额 (避免超出限制)

## 扩展开发

### 添加新智能体
1. 在`EnhancedMultiAgentSystem`中定义新角色
2. 配置LLM提供商和系统消息
3. 在分析流程中集成新智能体
4. 更新前端可视化界面

### 支持新语言
1. 添加语言解析器 (tree-sitter)
2. 扩展安全规则库
3. 更新代码质量度量
4. 调整分析模板

### 自定义分析器
1. 继承`EnhancedAgent`类
2. 实现特定分析逻辑
3. 注册到多智能体系统
4. 配置前端界面选项

---

## 📞 技术支持

如有问题，请查看：
1. 系统测试报告: `test_report_*.json`
2. API文档: http://localhost:8000/docs
3. 配置验证: `python start.py config`
4. 完整测试: `python start.py test`
