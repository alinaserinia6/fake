# AutoGen Studio 多智能体C/C++代码分析工作流配置指南

## ⚠️ 重要：API密钥配置

### 🔑 为什么需要API密钥？
AutoGen Studio需要API密钥才能创建团队和智能体。没有配置API密钥会出现验证错误，无法使用团队功能。

### ✅ API密钥已自动配置
我们已经为您配置了完整的API密钥环境：
- **OpenAI API** - 用于GPT模型
- **Anthropic API** - 用于Claude模型  
- **Google Gemini API** - 用于Gemini模型
- **本地Ollama** - 用于gpt-oss:latest模型

### 🚀 重新启动AutoGen Studio (已完成)
```bash
# 已为您执行以下操作：
./start_autogen_with_api.sh
```
✅ AutoGen Studio现在已经带着正确的API密钥运行在 http://localhost:8081

## 🎯 关于文件上传 vs 手动配置

### 文件上传方式 ✅
AutoGen Studio 支持多种配置方式：

1. **JSON配置文件导入** - 我们已经为您准备了完整的配置文件
2. **智能体提示词文件** - 每个角色的详细提示词已单独保存
3. **批量配置脚本** - 自动化配置工具

### 手动拖拽配置 ✅
在AutoGen Studio的Team Builder中：
- 可以拖拽调整智能体之间的连接关系
- 可视化编辑工作流程图
- 实时预览消息传递路径

## 🚀 快速配置方法

### 方法一：使用配置文件 (推荐)

1. **运行配置工具**：
```bash
cd /home/coder-gw/Interruptr
python configure_agents.py
```

2. **文件已自动生成**：
   - `agent_configs.json` - 完整团队配置
   - `agent_prompts/` - 每个智能体的提示词文件
   - 详细的配置指南

3. **在AutoGen Studio中使用**：
   - 访问 http://localhost:8081
   - 创建新团队时，可以参考JSON配置
   - 复制粘贴对应的提示词文件内容

### 方法二：可视化拖拽配置

1. **访问Team Builder**：
   - 打开 http://localhost:8081
   - 点击 "Teams" 或 "Team Builder"

2. **创建智能体**：
   - 拖拽创建5个Agent节点
   - 设置角色名称和描述
   - 粘贴对应的系统提示词

3. **配置工作流**：
   - 拖拽连接线设置消息传递路径
   - 设置并行/串行执行模式
   - 配置终止条件

## 📁 已准备的配置文件

```
/home/coder-gw/Interruptr/
├── agent_configs.json           # 完整团队配置文件
├── agent_prompts/              # 智能体提示词目录
│   ├── coordinator_prompt.txt     # 协调员提示词
│   ├── code_analyst_prompt.txt    # 代码分析师提示词
│   ├── security_expert_prompt.txt # 安全专家提示词
│   ├── debug_expert_prompt.txt    # 调试专家提示词
│   └── quality_critic_prompt.txt  # 质量评估师提示词
└── configure_agents.py         # 自动配置工具
```

## 🤖 智能体配置详情

### 1. Coordinator (协调员)
- **模型**: gpt-oss:latest
- **温度**: 0.3 (保持一致性)
- **令牌数**: 2048
- **文件**: `agent_prompts/coordinator_prompt.txt`

### 2. Code_Analyst (代码分析师)
- **模型**: gpt-oss:latest  
- **温度**: 0.2 (更严格的分析)
- **令牌数**: 3072
- **文件**: `agent_prompts/code_analyst_prompt.txt`

### 3. Security_Expert (安全专家)
- **模型**: gpt-oss:latest
- **温度**: 0.1 (最严格的分析)
- **令牌数**: 3072
- **文件**: `agent_prompts/security_expert_prompt.txt`

### 4. Debug_Expert (调试专家)
- **模型**: gpt-oss:latest
- **温度**: 0.2 (精确的诊断)
- **令牌数**: 3072
- **文件**: `agent_prompts/debug_expert_prompt.txt`

### 5. Quality_Critic (质量评估师)
- **模型**: gpt-oss:latest
- **温度**: 0.3 (综合评估)
- **令牌数**: 4096 (最长的输出)
- **文件**: `agent_prompts/quality_critic_prompt.txt`

## 🔄 工作流程配置

### 消息传递架构
```
用户输入
    ↓
Coordinator (接收任务)
    ↓
┌─────────────────────────────────┐
│     并行分析阶段 (Parallel)      │
├─ Code_Analyst    (代码分析)     │
├─ Security_Expert (安全检查)     │  
└─ Debug_Expert    (调试分析)     │
└─────────────────────────────────┘
    ↓
Coordinator (收集结果)
    ↓
Quality_Critic (最终评估)
    ↓
输出综合报告
```

### AutoGen Studio中的配置步骤

1. **创建团队**:
   - 团队名称: `C/C++ Code Analysis Team`
   - 描述: `专业的C/C++代码分析和安全审查团队`

2. **添加智能体** (按以下顺序):
   ```
   Coordinator → Code_Analyst → Security_Expert → Debug_Expert → Quality_Critic
   ```

3. **设置连接关系**:
   - User → Coordinator
   - Coordinator → [Code_Analyst, Security_Expert, Debug_Expert] (并行)
   - [Code_Analyst, Security_Expert, Debug_Expert] → Coordinator
   - Coordinator → Quality_Critic
   - Quality_Critic → User

4. **配置参数**:
   - 最大轮次: 10
   - 人工输入模式: NEVER
   - 终止条件: Quality_Critic 完成最终报告

## 📊 测试场景

### 使用示例代码
```bash
# 查看测试代码
cat /home/coder-gw/Interruptr/sample_code.cpp
```

### 测试流程
1. 在AutoGen Studio Playground中选择配置好的团队
2. 输入测试代码或上传文件
3. 观察智能体之间的消息传递
4. 查看每个专家的分析结果
5. 获得最终的综合评估报告

## 🛠️ 配置工具使用

### 自动配置脚本
```bash
# 运行配置工具
python configure_agents.py

# 检查系统状态
./setup_check.sh
```

### 文件管理
- 所有提示词文件可直接复制粘贴使用
- JSON配置文件包含完整的团队设置
- 可以根据需要修改温度、令牌数等参数

## 🎯 最佳实践

### 智能体配置
1. **保持温度一致性**: Security_Expert使用最低温度(0.1)确保严格分析
2. **合理分配令牌**: Quality_Critic需要最多令牌(4096)用于综合报告
3. **角色明确分工**: 每个智能体专注于特定领域

### 工作流优化
1. **并行处理**: Code/Security/Debug分析可以并行执行
2. **结果汇总**: Coordinator负责收集和整理所有分析结果
3. **质量把关**: Quality_Critic进行最终的综合评估

### 测试建议
1. **从简单开始**: 使用提供的sample_code.cpp测试基本功能
2. **观察对话**: 重点关注agent之间的消息传递过程
3. **调整参数**: 根据实际效果调整温度和令牌数设置

## 🚀 立即开始

现在您有两种配置方式：

### 快速配置 (文件上传方式)
1. 使用准备好的配置文件和提示词
2. 在AutoGen Studio中创建团队时参考JSON配置
3. 复制粘贴对应的提示词文件内容

### 可视化配置 (拖拽方式)  
1. 在Team Builder中手动创建和连接智能体
2. 拖拽设置工作流程图
3. 实时调整消息传递路径

**现在就访问 http://localhost:8081 开始配置您的多智能体团队！** 🎯
