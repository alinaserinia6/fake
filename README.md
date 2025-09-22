# C/C++ 多智能体代码分析系统 - 部署完成

## 🎉 系统状态
- ✅ **AutoGen Studio**: 已启动并运行在后台 (http://localhost:8081)
- ✅ **多智能体框架**: 使用官方AutoGen Studio替代自定义web UI
- ✅ **本地LLM**: 支持 gpt-oss:latest (适配您的双3090硬件)
- ✅ **进程管理**: 后台运行，不阻塞终端
- ✅ **示例代码**: 包含多种典型C++问题的测试文件

## � 已创建的文件
1. `autogen_workflow_guide.md` - 详细的工作流配置指南
2. `sample_code.cpp` - 测试用C++代码(包含安全、性能、内存管理问题)
3. `setup_check.sh` - 系统状态检查脚本
4. `autogen_studio.log` - AutoGen Studio运行日志

## 🤖 多智能体团队设计

### 智能体角色分工
1. **协调员** - 任务分配和进度管理
2. **代码分析师** - 结构和算法分析
3. **安全专家** - 漏洞和安全问题检测
4. **调试专家** - 错误诊断和性能分析
5. **质量评估师** - 综合评估和改进建议

### 消息传递流程
```
用户代码输入 → 协调员接收 → 并行分析(3个专家) → 协调员汇总 → 质量评估师最终报告 → 输出结果
```

## 🌐 Web界面使用

### 即时访问
- **URL**: http://localhost:8081
- **状态**: ✅ 已在VS Code Simple Browser中打开
- **后台运行**: 不会阻塞终端

### 配置步骤
1. 访问AutoGen Studio Web界面
2. 点击 "Teams" 或 "Team Builder"
3. 创建新团队 "C/C++ Code Analysis Team"
4. 为每个角色创建智能体 (使用指南中的系统提示词)
5. 配置模型为 `gpt-oss:latest`
6. 设置工作流程和消息传递逻辑
7. 使用 `sample_code.cpp` 测试分析流程

## 📊 测试场景

### 示例代码问题覆盖
- **安全漏洞**: 缓冲区溢出、硬编码密码、权限控制
- **内存管理**: 内存泄漏、资源未释放、空指针风险
- **算法效率**: 低效排序、线性查找、字符串操作
- **编程实践**: 边界检查缺失、错误处理不完整、RAII违反

### 预期分析输出
- 每个专家的专业分析报告
- 智能体之间的协作对话过程
- 最终的综合质量评估和改进建议
- 完整的代码分析文档

## � agent-to-agent 消息流演示

在AutoGen Studio的Playground中，您将看到：
1. **协调员**分配任务给各专家
2. **代码分析师**分析架构和算法
3. **安全专家**识别安全风险
4. **调试专家**发现性能问题
5. **质量评估师**综合所有意见并给出最终评估

## 🚀 现在可以开始使用！

所有自定义web UI已删除，现在使用AutoGen Studio的官方工具实现真正的多智能体协作。您可以：

1. **立即体验**: 打开 http://localhost:8081 
2. **查看对话**: 观察agent之间的实时消息传递
3. **分析代码**: 使用提供的示例代码测试分析能力
4. **自定义工作流**: 根据需要调整智能体配置

### 关键改进
- ❌ 移除了所有自定义demo和web UI代码
- ✅ 使用AutoGen官方多智能体框架
- ✅ 真实的agent-to-agent消息传递
- ✅ 可观察的对话过程和源代码处理流程
- ✅ 后台运行，不阻塞终端

**系统已完全准备就绪，请开始您的多智能体C/C++代码分析之旅！** 🎯
│   ├── execution_tracer.py   # 执行跟踪
│   └── gdb_controller.py     # GDB控制器
├── api/                   # API服务
│   └── main.py           # FastAPI主应用
├── frontend/              # 前端界面
│   └── app.py            # Streamlit应用
├── config/                # 配置文件
│   └── settings.py       # 项目配置
├── examples/              # 示例代码
│   └── unsafe_code.c     # 测试用例
├── tests/                 # 测试用例
└── requirements.txt       # 依赖包
```

## 🛠️ 环境安装

### 1. 创建Conda环境

```bash
conda create -n interruptr python=3.11 -y
conda activate interruptr
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 3. 安装系统工具

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y gcc gdb valgrind cppcheck clang-tools

# CentOS/RHEL
sudo yum install -y gcc gdb valgrind cppcheck clang-tools-extra

# macOS
brew install gcc gdb valgrind cppcheck llvm
```

## 🚀 快速开始

### 1. 环境初始化

```bash
# 运行配置检查脚本
python3 setup.py

# 编辑环境配置文件
nano .env
```

### 2. 配置API密钥

在 `.env` 文件中添加您的API密钥：

```bash
# OpenAI API (推荐用于对话可视化)
OPENAI_API_KEY=your-openai-api-key-here

# 或 Anthropic Claude API (推荐用于代码分析)  
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. 启动服务

```bash
./start.sh
```

选择启动模式：
- 1) 仅API服务 (端口8000)
- 2) 仅前端界面 (端口8501)  
- 3) 同时启动两者
- 4) 运行示例分析

## 📊 使用示例

### 分析示例代码

项目提供了一个包含常见安全问题的示例文件 `examples/unsafe_code.c`：

```c
void unsafe_copy(char* source) {
    char buffer[100];
    strcpy(buffer, source);  // 潜在缓冲区溢出
    printf("Copied: %s\\n", buffer);
}
```

Interruptr会识别并报告：
- 🚨 **高危**: 缓冲区溢出风险
- 💡 **建议**: 使用strncpy或snprintf替代
- 🎯 **断点**: 在strcpy调用前设置检查点

## 🎯 多智能体框架选择建议

### AutoGen vs LangGraph 对比

| 特性 | AutoGen | LangGraph | 推荐场景 |
|------|---------|-----------|----------|
| **对话可视化** | ✅ 内置支持 | ⚠️ 需自定义 | 实时对话展示 |
| **工作流可视化** | ⚠️ 简单流程 | ✅ 复杂图结构 | 流程编排 |
| **状态管理** | ⚠️ 基础 | ✅ 强大 | 复杂状态跟踪 |
| **开发难度** | 🟢 简单 | 🟡 中等 | 快速原型 |
| **扩展性** | 🟡 中等 | 🟢 优秀 | 大型项目 |

### 本项目的混合架构

**选择原因：结合两者优势**

1. **AutoGen** 用于：
   - 智能体间的实时对话
   - 用户交互界面
   - 快速原型和演示

2. **LangGraph** 用于：
   - 复杂分析工作流编排
   - 状态管理和持久化
   - 条件分支和循环逻辑

```python
# 示例：混合使用
from autogen_agentchat.teams import RoundRobinGroupChat
from langgraph.graph import StateGraph

# AutoGen负责对话
agents = [code_analyst, security_expert, debug_expert]
chat_team = RoundRobinGroupChat(agents)

# LangGraph负责工作流
workflow = StateGraph(AnalysisState)
workflow.add_node("parse_code", parse_code_node)
workflow.add_node("security_scan", security_scan_node)
workflow.add_edge("parse_code", "security_scan")
```

## 🔧 配置说明

### 环境变量

项目使用 `.env` 文件管理配置：

```bash
# 必需配置
OPENAI_API_KEY=your-openai-key          # OpenAI API密钥
ANTHROPIC_API_KEY=your-anthropic-key    # Anthropic API密钥

# 可选配置  
DEFAULT_LLM_PROVIDER=openai             # 默认LLM提供商
API_HOST=localhost                      # API服务地址
API_PORT=8000                          # API服务端口
SECURITY_LEVEL=high                     # 安全检测级别
MAX_FILE_SIZE=10                       # 最大文件大小(MB)
```

### 配置文件

在 `config/settings.py` 中可以自定义：
- 智能体行为参数
- 安全检测规则
- 分析工具路径
- 数据库连接

## 🧪 测试

```bash
# 运行单元测试
python -m pytest tests/

# 运行集成测试  
python -m pytest tests/integration/

# 检查代码质量
flake8 src/
mypy src/
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📈 路线图

### v0.2.0 (计划中)
- [ ] 完善AutoGen+LangGraph混合架构
- [ ] 实现实时对话可视化界面
- [ ] 支持更多编程语言 (Java, Python)
- [ ] 集成更多静态分析工具
- [ ] 添加CI/CD集成

### v0.3.0 (计划中)
- [ ] 分布式多智能体协作
- [ ] 实时代码监控和热重载
- [ ] 自定义规则引擎和插件系统
- [ ] 团队协作和权限管理
- [ ] 性能优化和缓存机制

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 团队

- **开发团队**: Interruptr Development Team
- **联系方式**: [项目Issues](https://github.com/your-org/interruptr/issues)

## 🙏 致谢

感谢以下开源项目的支持：
- [AutoGen](https://github.com/microsoft/autogen) - 多智能体框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排
- [Tree-sitter](https://tree-sitter.github.io/) - 语法解析
- [FastAPI](https://fastapi.tiangolo.com/) - API框架
- [Streamlit](https://streamlit.io/) - 前端框架

---

🚀 **让代码分析更智能，让调试更高效！**
