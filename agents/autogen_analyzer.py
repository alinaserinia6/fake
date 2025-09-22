"""
基于 AutoGen 的多智能体 C++ 代码分析系统
"""

import os
import sys
import asyncio
from typing import Dict, List, Any, Optional
import tempfile
import json

# AutoGen imports
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken
    AUTOGEN_AVAILABLE = True
except ImportError as e:
    print(f"AutoGen 导入失败: {e}")
    AUTOGEN_AVAILABLE = False

# LangChain imports for LLM integration
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_config import config

class AutoGenCodeAnalyzer:
    """基于 AutoGen 的多智能体代码分析器"""
    
    def __init__(self):
        self.agents = {}
        self.conversation_history = []
        self.analysis_results = {}
        
    def setup_llm_clients(self):
        """设置 LLM 客户端"""
        llm_configs = {}
        
        # OpenAI 配置
        if config.openai_api_key:
            llm_configs["openai"] = {
                "config_list": [{
                    "model": config.openai_model,
                    "api_key": config.openai_api_key,
                    "base_url": config.openai_base_url,
                    "temperature": config.openai_temperature
                }]
            }
        
        # Anthropic Claude 配置
        if config.anthropic_api_key:
            llm_configs["anthropic"] = {
                "config_list": [{
                    "model": config.anthropic_model,
                    "api_key": config.anthropic_api_key,
                    "base_url": config.anthropic_base_url,
                    "temperature": config.anthropic_temperature
                }]
            }
        
        return llm_configs
    
    def create_agents(self):
        """创建专业的智能体团队"""
        
        llm_configs = self.setup_llm_clients()
        
        # 如果没有可用的 LLM 配置，使用模拟模式
        if not llm_configs:
            print("⚠️ 未找到可用的 LLM 配置，将使用模拟模式")
            return self.create_mock_agents()
        
        # 使用第一个可用的 LLM 配置
        primary_llm = list(llm_configs.values())[0]
        
        # 协调者智能体
        self.agents["coordinator"] = AssistantAgent(
            name="协调者",
            model_client=primary_llm,
            system_message="""你是一个智能的代码分析协调者。你的职责是：
            1. 接收用户提交的 C/C++ 代码
            2. 协调其他专家智能体进行分析
            3. 整理和总结所有分析结果
            4. 制定修复优先级和建议
            
            请保持专业、准确，并确保分析的全面性。
            """,
            description="负责协调整个分析流程"
        )
        
        # 代码分析师
        self.agents["code_analyst"] = AssistantAgent(
            name="代码分析师",
            model_client=primary_llm,
            system_message="""你是一个专业的 C/C++ 代码分析师。你的专长包括：
            1. 静态代码分析和度量
            2. 计算圈复杂度和代码质量指标
            3. 检查代码结构和组织
            4. 识别性能问题和优化建议
            
            请提供详细的代码质量分析报告。
            """,
            description="专注于代码质量和结构分析"
        )
        
        # 安全专家
        self.agents["security_expert"] = AssistantAgent(
            name="安全专家",
            model_client=primary_llm,
            system_message="""你是一个 C/C++ 安全漏洞专家。你的专长包括：
            1. 缓冲区溢出检测
            2. 内存泄漏和野指针分析
            3. 危险函数使用检查
            4. 输入验证和边界检查
            5. 常见安全漏洞模式识别
            
            请重点关注安全问题，提供具体的漏洞位置和修复建议。
            """,
            description="专注于安全漏洞检测和分析"
        )
        
        # 调试专家
        self.agents["debug_expert"] = AssistantAgent(
            name="调试专家",
            model_client=primary_llm,
            system_message="""你是一个 C/C++ 调试专家。你的专长包括：
            1. 分析代码的可调试性
            2. 建议断点设置位置
            3. 推荐调试工具和技术
            4. 错误处理和异常分析
            5. 日志记录和监控建议
            
            请提供实用的调试策略和工具建议。
            """,
            description="专注于调试策略和工具建议"
        )
        
        # 架构师
        self.agents["architect"] = AssistantAgent(
            name="架构师",
            model_client=primary_llm,
            system_message="""你是一个软件架构专家。你的专长包括：
            1. 设计模式识别和建议
            2. SOLID 原则检查
            3. 代码组织和模块化分析
            4. 接口设计和依赖管理
            5. 可维护性和扩展性评估
            
            请从架构角度分析代码设计质量。
            """,
            description="专注于软件架构和设计模式分析"
        )
        
        # 评判者（使用不同的 LLM 如果可用）
        critic_llm = llm_configs.get("anthropic", primary_llm)
        self.agents["critic"] = AssistantAgent(
            name="评判者",
            model_client=critic_llm,
            system_message="""你是一个严格的代码评判者。你的职责是：
            1. 综合所有专家的分析结果
            2. 进行客观的质量评分
            3. 指出分析中可能的遗漏
            4. 提供改进优先级排序
            5. 给出最终的评估结论
            
            请保持批判性思维，确保分析的准确性和完整性。
            """,
            description="负责最终质量评估和批判性分析"
        )
        
        return True
    
    def create_mock_agents(self):
        """创建模拟智能体（当没有 LLM 配置时）"""
        
        class MockAgent:
            def __init__(self, name, role):
                self.name = name
                self.role = role
            
            async def generate_response(self, message):
                # 返回模拟响应
                responses = {
                    "协调者": f"我是协调者，收到分析请求：{message[:50]}...",
                    "代码分析师": "进行静态代码分析中...",
                    "安全专家": "检测安全漏洞中...",
                    "调试专家": "分析调试需求中...", 
                    "架构师": "评估架构设计中...",
                    "评判者": "进行综合评估中..."
                }
                return responses.get(self.name, "处理中...")
        
        agent_configs = [
            ("协调者", "协调分析流程"),
            ("代码分析师", "代码质量分析"),
            ("安全专家", "安全漏洞检测"),
            ("调试专家", "调试策略建议"),
            ("架构师", "架构设计分析"),
            ("评判者", "综合质量评估")
        ]
        
        for name, role in agent_configs:
            self.agents[name] = MockAgent(name, role)
        
        return False  # 表示使用模拟模式
    
    async def analyze_code(self, code_content: str, filename: str) -> Dict[str, Any]:
        """使用多智能体分析代码"""
        
        print(f"🔍 开始分析文件: {filename}")
        print(f"📝 代码长度: {len(code_content)} 字符")
        
        # 创建智能体
        has_real_llm = self.create_agents()
        
        if has_real_llm:
            return await self.run_autogen_analysis(code_content, filename)
        else:
            return await self.run_mock_analysis(code_content, filename)
    
    async def run_autogen_analysis(self, code_content: str, filename: str) -> Dict[str, Any]:
        """运行真实的 AutoGen 多智能体分析"""
        
        if not AUTOGEN_AVAILABLE:
            print("⚠️ AutoGen 不可用，使用模拟模式")
            return await self.run_mock_analysis(code_content, filename)
        
        try:
            # 创建团队聊天
            team = RoundRobinGroupChat([
                self.agents["coordinator"],
                self.agents["code_analyst"], 
                self.agents["security_expert"],
                self.agents["debug_expert"],
                self.agents["architect"],
                self.agents["critic"]
            ])
            
            # 准备分析提示
            analysis_prompt = f"""
请分析以下 C/C++ 代码文件：{filename}

代码内容：
```cpp
{code_content}
```

请每个专家按照自己的专长进行分析：
1. 协调者：总体协调和流程管理
2. 代码分析师：代码质量、复杂度、性能分析
3. 安全专家：安全漏洞、内存安全、危险函数检测
4. 调试专家：调试建议、断点推荐、工具建议
5. 架构师：设计模式、SOLID原则、架构质量
6. 评判者：综合评估、评分、改进建议

请提供详细且具体的分析结果。
"""
            
            # 运行分析
            import sys
            result = await team.run(
                task=analysis_prompt,
                cancellation_token=CancellationToken()
            )
            
            # 整理对话历史
            conversation_history = []
            if hasattr(result, 'messages'):
                for message in result.messages:
                    conversation_history.append({
                        "agent": getattr(message, 'source', 'unknown'),
                        "agent_name": f"🤖 {getattr(message, 'source', 'unknown')}",
                        "message": getattr(message, 'content', str(message)),
                        "timestamp": "2025-08-30 16:40:00",  # 简化时间戳
                        "reasoning": f"基于 {getattr(message, 'source', 'unknown')} 的专业分析"
                    })
            
            return {
                "analysis_type": "autogen_real",
                "filename": filename,
                "agent_conversations": conversation_history,
                "summary": {
                    "total_agents": len(self.agents),
                    "total_messages": len(conversation_history),
                    "analysis_complete": True
                },
                "file_info": {
                    "filename": filename,
                    "total_lines": len(code_content.split('\n')),
                    "code_size": len(code_content)
                }
            }
            
        except Exception as e:
            print(f"❌ AutoGen 分析失败: {e}")
            return await self.run_mock_analysis(code_content, filename)
    
    async def run_mock_analysis(self, code_content: str, filename: str) -> Dict[str, Any]:
        """运行模拟的多智能体分析"""
        
        print("🎭 运行模拟多智能体分析模式")
        
        # 简单的代码分析
        lines = code_content.split('\n')
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
        
        # 检测问题
        security_issues = []
        if 'strcpy' in code_content:
            security_issues.append("发现 strcpy 函数，可能导致缓冲区溢出")
        if 'gets' in code_content:
            security_issues.append("发现 gets 函数，极易导致缓冲区溢出")
        if 'malloc' in code_content and 'free' not in code_content:
            security_issues.append("发现 malloc 但未找到对应的 free，可能存在内存泄漏")
        
        # 模拟智能体对话
        conversations = [
            {
                "agent": "coordinator",
                "agent_name": "🎯 协调者",
                "message": f"开始分析文件 {filename}，共 {len(lines)} 行代码。分配任务给各专家智能体。",
                "timestamp": "2025-08-30 16:40:01",
                "reasoning": "初始化多智能体协作分析流程"
            },
            {
                "agent": "code_analyst", 
                "agent_name": "📊 代码分析师",
                "message": f"代码结构分析完成：\n- 总行数：{len(lines)}\n- 有效代码行：{len(code_lines)}\n- 函数数量：{code_content.count('(')}\n- 复杂度：中等",
                "timestamp": "2025-08-30 16:40:05",
                "reasoning": "基于静态分析进行代码度量统计"
            },
            {
                "agent": "security_expert",
                "agent_name": "🔒 安全专家", 
                "message": f"安全分析结果：\n{''.join(['- ' + issue + chr(10) for issue in security_issues]) if security_issues else '✅ 未发现明显安全问题'}",
                "timestamp": "2025-08-30 16:40:08",
                "reasoning": "扫描常见的C/C++安全漏洞模式"
            },
            {
                "agent": "debug_expert",
                "agent_name": "🐛 调试专家",
                "message": "调试建议：\n- 建议使用 gdb 进行调试\n- 关键位置设置断点\n- 开启编译器警告选项\n- 使用 Valgrind 检测内存问题",
                "timestamp": "2025-08-30 16:40:12",
                "reasoning": "基于代码特征提供调试策略"
            },
            {
                "agent": "architect",
                "agent_name": "🏗️ 架构师",
                "message": f"架构评估：\n- 代码组织：{'简单' if len(code_lines) < 50 else '复杂'}\n- 函数设计：需要进一步模块化\n- 建议遵循 SOLID 原则",
                "timestamp": "2025-08-30 16:40:16",
                "reasoning": "从软件工程角度评估代码设计"
            },
            {
                "agent": "critic",
                "agent_name": "🧐 评判者",
                "message": f"综合评估：\n- 代码质量：{'良好' if not security_issues else '需要改进'}\n- 安全评分：{8 if not security_issues else 4}/10\n- 建议：{'继续保持' if not security_issues else '优先修复安全问题'}",
                "timestamp": "2025-08-30 16:40:20",
                "reasoning": "综合所有专家意见进行最终评估"
            },
            {
                "agent": "coordinator",
                "agent_name": "🎯 协调者",
                "message": f"分析完成！共发现 {len(security_issues)} 个潜在问题。建议按优先级修复。",
                "timestamp": "2025-08-30 16:40:24",
                "reasoning": "汇总分析结果并制定行动计划"
            }
        ]
        
        return {
            "analysis_type": "autogen_mock",
            "filename": filename,
            "agent_conversations": conversations,
            "security_issues": security_issues,
            "code_metrics": {
                "total_lines": len(lines),
                "code_lines": len(code_lines),
                "complexity": "medium",
                "function_count": code_content.count('(')
            },
            "summary": {
                "total_agents": len(self.agents),
                "issues_found": len(security_issues),
                "overall_score": 8 if not security_issues else 4
            },
            "file_info": {
                "filename": filename,
                "total_lines": len(lines),
                "code_size": len(code_content)
            }
        }

# 全局分析器实例
autogen_analyzer = AutoGenCodeAnalyzer()
