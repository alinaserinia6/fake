#!/usr/bin/env python3
"""
真实的多智能体代码分析演示脚本
使用 AutoGen 进行多智能体协作
"""

import os
import asyncio
from pathlib import Path
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# 配置模型
def get_model_client():
    """获取模型客户端 - 优先使用本地 Ollama"""
    try:
        # 尝试使用本地 Ollama gpt-oss 模型
        client = OpenAIChatCompletionClient(
            model="gpt-oss:latest",
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )
        return client
    except Exception as e:
        print(f"Ollama 连接失败，尝试使用 OpenAI: {e}")
        # 备用 OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAIChatCompletionClient(
                model="gpt-4o-mini",
                api_key=api_key
            )
        else:
            raise Exception("未找到可用的模型配置")

def create_agents():
    """创建多智能体团队"""
    model_client = get_model_client()
    
    # 协调器
    coordinator = AssistantAgent(
        name="coordinator",
        model_client=model_client,
        system_message="""你是一个多智能体代码分析系统的协调器。

你的职责：
1. 接收并理解代码分析任务
2. 将任务分解为具体的分析维度
3. 协调各专家智能体的工作
4. 整合分析结果并给出综合性建议
5. 确保分析的完整性和准确性

请始终保持专业和条理性。"""
    )
    
    # 代码分析专家
    code_analyst = AssistantAgent(
        name="code_analyst", 
        model_client=model_client,
        system_message="""你是一个专业的代码分析专家。

你的专长：
1. 静态代码分析和结构评估
2. 代码逻辑流程分析
3. 代码质量和可维护性评估
4. 性能问题识别
5. 编程最佳实践检查

分析时请提供具体的行号、问题描述和改进建议。"""
    )
    
    # 安全专家
    security_expert = AssistantAgent(
        name="security_expert",
        model_client=model_client, 
        system_message="""你是一个网络安全专家，专注于代码安全分析。

你的专长：
1. 缓冲区溢出检测
2. 注入攻击漏洞识别
3. 内存安全问题分析
4. 输入验证检查
5. 安全编码实践评估

请提供详细的安全风险评估和修复建议。"""
    )
    
    # 调试专家
    debug_expert = AssistantAgent(
        name="debug_expert",
        model_client=model_client,
        system_message="""你是一个调试和错误分析专家。

你的专长：
1. 运行时错误分析
2. 内存泄漏检测
3. 逻辑错误识别
4. 异常处理分析
5. 错误修复方案设计

请提供精确的错误定位和可执行的修复步骤。"""
    )
    
    # 评审专家
    critic = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message="""你是一个代码评审专家，负责质量控制。

你的职责：
1. 评审其他专家的分析结果
2. 验证分析的准确性和完整性
3. 识别可能遗漏的问题
4. 评估修复方案的可行性
5. 提供最终的质量保证

请提供客观、全面的评审意见。"""
    )
    
    # 用户代理 - 简化版本
    user_proxy = None  # 在新版本中不需要 UserProxy
    
    return [coordinator, code_analyst, security_expert, debug_expert, critic], user_proxy

async def analyze_code_with_agents(code_content, file_path):
    """使用多智能体分析代码"""
    print(f"\\n{'='*60}")
    print(f"开始多智能体分析: {file_path}")
    print(f"{'='*60}")
    
    agents, user_proxy = create_agents()
    
    # 创建分析任务
    task_message = f"""
请分析以下 C++ 代码文件：{file_path}

代码内容：
```cpp
{code_content}
```

要求：
1. 代码分析专家进行静态分析和结构评估
2. 安全专家检查安全漏洞
3. 调试专家识别潜在的运行时错误
4. 评审专家对所有分析结果进行综合评审
5. 协调器整合所有意见并提供最终修复建议

请各位专家详细分析并提供具体的修复方案。
"""
    
    # 创建群聊团队
    group_chat = RoundRobinGroupChat(
        participants=agents,
        termination_condition=MaxMessageTermination(max_messages=20)
    )
    
    console = Console(stream=True)
    
    # 开始多智能体对话
    result = await console.a_run(
        task=task_message,
        team=group_chat
    )
    
    return result

async def main():
    """主函数"""
    print("🤖 启动多智能体代码分析系统...")
    print("📝 使用 AutoGen 进行真实的智能体协作\\n")
    
    # 获取示例代码文件
    examples_dir = Path("/home/coder-gw/Interruptr/examples")
    cpp_files = list(examples_dir.glob("*.cpp"))
    
    if not cpp_files:
        print("❌ 未找到示例代码文件")
        return
    
    # 分析每个代码文件
    for cpp_file in cpp_files[:2]:  # 分析前两个文件作为演示
        try:
            with open(cpp_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # 启动多智能体分析
            await analyze_code_with_agents(code_content, cpp_file.name)
            
            print(f"\\n✅ 完成分析: {cpp_file.name}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ 分析失败 {cpp_file.name}: {e}")
    
    print("\\n🎉 多智能体分析完成！")
    print("🌐 AutoGen Studio 正在运行在: http://localhost:8081")

if __name__ == "__main__":
    asyncio.run(main())
