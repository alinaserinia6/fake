"""
增强的多智能体系统
包含质疑者(Critic)和检查者(Reviewer)角色，实现更全面的代码分析
"""

import asyncio
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from dataclasses import dataclass
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.env_config import config

@dataclass
class AgentConfig:
    """智能体配置"""
    name: str
    role: str
    llm_provider: str
    system_message: str
    temperature: float = 0.1
    max_tokens: int = 4000

class LLMInterface:
    """LLM接口抽象层"""
    
    @staticmethod
    async def call_openai(prompt: str, system_message: str) -> str:
        """调用OpenAI API"""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(
                api_key=config.openai_api_key,
                base_url=config.openai_base_url
            )
            
            response = await client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=config.openai_temperature,
                max_tokens=config.openai_max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"OpenAI调用失败: {str(e)}"
    
    @staticmethod
    async def call_anthropic(prompt: str, system_message: str) -> str:
        """调用Anthropic Claude API"""
        try:
            from anthropic import AsyncAnthropic
            
            client = AsyncAnthropic(
                api_key=config.anthropic_api_key
            )
            
            response = await client.messages.create(
                model=config.anthropic_model,
                max_tokens=config.anthropic_max_tokens,
                temperature=config.anthropic_temperature,
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"Anthropic调用失败: {str(e)}"
    
    @staticmethod
    async def call_gemini(prompt: str, system_message: str) -> str:
        """调用Google Gemini API"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=config.gemini_api_key)
            model = genai.GenerativeModel(config.gemini_model)
            
            full_prompt = f"{system_message}\n\n{prompt}"
            response = await model.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.gemini_temperature,
                    max_output_tokens=config.gemini_max_tokens
                )
            )
            
            return response.text
            
        except Exception as e:
            return f"Gemini调用失败: {str(e)}"
    
    @staticmethod
    async def call_ollama(prompt: str, system_message: str) -> str:
        """调用Ollama本地推理"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": config.ollama_model,
                    "prompt": f"{system_message}\n\n{prompt}",
                    "stream": False,
                    "options": {
                        "temperature": config.ollama_temperature,
                        "num_predict": config.ollama_max_tokens
                    }
                }
                
                async with session.post(
                    f"{config.ollama_base_url}/api/generate",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "Ollama响应为空")
                    else:
                        return f"Ollama调用失败: HTTP {response.status}"
                        
        except Exception as e:
            return f"Ollama调用失败: {str(e)}"

class EnhancedAgent:
    """增强的智能体类"""
    
    def __init__(self, agent_config: AgentConfig):
        self.config = agent_config
        self.conversation_history: List[Dict[str, str]] = []
        
    async def process(self, prompt: str, context: Optional[Dict] = None) -> str:
        """处理输入并返回响应"""
        
        # 添加上下文信息
        if context:
            enhanced_prompt = f"""
上下文信息:
{json.dumps(context, ensure_ascii=False, indent=2)}

任务:
{prompt}
"""
        else:
            enhanced_prompt = prompt
        
        # 根据LLM提供商选择调用方法
        if self.config.llm_provider == "openai":
            response = await LLMInterface.call_openai(enhanced_prompt, self.config.system_message)
        elif self.config.llm_provider == "claude":
            response = await LLMInterface.call_anthropic(enhanced_prompt, self.config.system_message)
        elif self.config.llm_provider == "gemini":
            response = await LLMInterface.call_gemini(enhanced_prompt, self.config.system_message)
        elif self.config.llm_provider == "ollama":
            response = await LLMInterface.call_ollama(enhanced_prompt, self.config.system_message)
        else:
            response = f"不支持的LLM提供商: {self.config.llm_provider}"
        
        # 记录对话历史
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": enhanced_prompt,
            "response": response
        })
        
        return response

class EnhancedMultiAgentSystem:
    """增强的多智能体系统"""
    
    def __init__(self):
        self.agents: Dict[str, EnhancedAgent] = {}
        self.analysis_results: Dict[str, Any] = {}
        self.conversation_log: List[Dict[str, Any]] = []
        
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有智能体"""
        
        # 协调者 - GPT-4 (综合协调能力强)
        coordinator_config = AgentConfig(
            name="coordinator",
            role="协调者",
            llm_provider=config.coordinator_llm,
            system_message="""你是Interruptr系统的协调者，负责管理整个代码分析流程。
你的职责：
1. 分解复杂的分析任务
2. 协调各专家智能体的工作
3. 整合分析结果
4. 确保分析的完整性和准确性
5. 生成最终的综合报告

请始终保持客观、专业的态度，确保分析过程有序进行。"""
        )
        
        # 代码分析师 - Claude (深度分析能力)
        code_analyst_config = AgentConfig(
            name="code_analyst",
            role="代码分析师", 
            llm_provider=config.code_analyst_llm,
            system_message="""你是专业的C/C++代码分析师，具有深厚的编程经验。
你的专长：
1. 静态代码分析和结构解析
2. 代码复杂度计算和质量评估
3. 编程规范和最佳实践检查
4. 性能瓶颈识别
5. 代码可维护性评估

请提供详细、准确的分析报告，包含具体的改进建议。"""
        )
        
        # 安全专家 - Claude (专业安全分析)
        security_expert_config = AgentConfig(
            name="security_expert",
            role="安全专家",
            llm_provider=config.security_expert_llm,
            system_message="""你是C/C++安全领域的专家，专注于识别和分析安全漏洞。
你的专长：
1. 缓冲区溢出检测
2. 内存泄漏和野指针分析
3. 整数溢出和下溢检查
4. 格式字符串漏洞识别
5. 竞态条件分析
6. 加密和认证问题

请提供详细的安全风险评估和具体的修复方案。"""
        )
        
        # 调试专家 - GPT-4 (调试经验丰富)
        debug_expert_config = AgentConfig(
            name="debug_expert",
            role="调试专家",
            llm_provider=config.debug_expert_llm,
            system_message="""你是经验丰富的调试专家，擅长分析程序执行流程和定位问题。
你的专长：
1. 智能断点位置推荐
2. 程序执行路径分析
3. 变量状态跟踪策略
4. 异常和错误处理分析
5. 测试用例设计
6. 调试工具使用建议

请提供实用的调试策略和具体的断点建议。"""
        )
        
        # 架构师 - Claude (架构设计能力)
        architect_config = AgentConfig(
            name="architect",
            role="架构师",
            llm_provider=config.architect_llm,
            system_message="""你是软件架构师，专注于代码的整体设计和架构质量。
你的专长：
1. 软件架构模式识别和评估
2. 代码组织结构分析
3. 模块耦合度和内聚性评估
4. 设计原则遵循情况检查
5. 可扩展性和可维护性分析
6. 重构建议和架构改进

请从架构角度提供专业的设计建议。"""
        )
        
        # 质疑者 - Gemini (多角度质疑)
        critic_config = AgentConfig(
            name="critic",
            role="质疑者",
            llm_provider=config.critic_llm,
            system_message="""你是独立的质疑者，负责对其他智能体的分析结果进行批判性审查。
你的职责：
1. 质疑分析结论的合理性
2. 寻找被遗漏的问题和风险
3. 验证建议的可行性
4. 提出反对意见和替代方案
5. 确保分析的全面性和客观性

请保持批判性思维，提出有建设性的质疑和不同观点。"""
        )
        
        # 检查者 - Ollama本地 (独立验证)
        reviewer_config = AgentConfig(
            name="reviewer",
            role="检查者",
            llm_provider=config.reviewer_llm,
            system_message="""你是独立的检查者，负责最终审核和验证所有分析结果。
你的职责：
1. 验证分析结果的准确性
2. 检查结论的逻辑一致性
3. 确认建议的实用性
4. 识别矛盾和不一致之处
5. 提供最终的质量保证

请进行严格的审核，确保输出结果的质量和可靠性。"""
        )
        
        # 创建智能体实例
        configs = [
            coordinator_config, code_analyst_config, security_expert_config,
            debug_expert_config, architect_config, critic_config, reviewer_config
        ]
        
        for agent_config in configs:
            self.agents[agent_config.name] = EnhancedAgent(agent_config)
    
    def _log_conversation(self, sender: str, receiver: str, message: str, message_type: str = "analysis"):
        """记录对话"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "type": message_type
        }
        self.conversation_log.append(entry)
    
    async def analyze_code_file(self, file_path: str, code_content: str) -> Dict[str, Any]:
        """执行完整的代码分析流程"""
        
        print(f"🚀 开始分析文件: {file_path}")
        
        # 第一轮：基础分析
        print("\n📊 第一轮：基础专家分析...")
        
        # 1. 代码分析师分析
        code_analysis_prompt = f"""
请分析以下C/C++代码文件：

文件路径: {file_path}
代码内容:
```c
{code_content}
```

请提供详细的代码质量分析报告。
"""
        
        code_analysis = await self.agents["code_analyst"].process(code_analysis_prompt)
        self.analysis_results["code_quality"] = code_analysis
        self._log_conversation("system", "code_analyst", code_analysis_prompt)
        self._log_conversation("code_analyst", "system", code_analysis)
        print("✅ 代码质量分析完成")
        
        # 2. 安全专家分析
        security_analysis_prompt = f"""
基于代码质量分析结果，请进行安全漏洞检测：

代码分析结果：
{code_analysis}

原始代码：
```c
{code_content}
```

请重点检测安全风险和漏洞。
"""
        
        security_analysis = await self.agents["security_expert"].process(
            security_analysis_prompt,
            {"code_analysis": code_analysis}
        )
        self.analysis_results["security"] = security_analysis
        self._log_conversation("system", "security_expert", security_analysis_prompt)
        self._log_conversation("security_expert", "system", security_analysis)
        print("✅ 安全分析完成")
        
        # 3. 调试专家分析
        debug_analysis_prompt = f"""
基于前面的分析结果，请提供调试建议：

代码质量分析：
{code_analysis}

安全分析：
{security_analysis}

请推荐断点位置和调试策略。
"""
        
        debug_analysis = await self.agents["debug_expert"].process(
            debug_analysis_prompt,
            {"code_analysis": code_analysis, "security_analysis": security_analysis}
        )
        self.analysis_results["debug"] = debug_analysis
        self._log_conversation("system", "debug_expert", debug_analysis_prompt)
        self._log_conversation("debug_expert", "system", debug_analysis)
        print("✅ 调试分析完成")
        
        # 4. 架构师分析
        architecture_analysis_prompt = f"""
基于所有分析结果，请进行架构评估：

代码质量：{code_analysis}
安全分析：{security_analysis}
调试分析：{debug_analysis}

请从架构角度提供设计建议。
"""
        
        architecture_analysis = await self.agents["architect"].process(
            architecture_analysis_prompt,
            {
                "code_analysis": code_analysis,
                "security_analysis": security_analysis,
                "debug_analysis": debug_analysis
            }
        )
        self.analysis_results["architecture"] = architecture_analysis
        self._log_conversation("system", "architect", architecture_analysis_prompt)
        self._log_conversation("architect", "system", architecture_analysis)
        print("✅ 架构分析完成")
        
        # 第二轮：质疑和检查
        print("\n🤔 第二轮：质疑者审查...")
        
        # 5. 质疑者审查
        critic_prompt = f"""
请对以下分析结果进行批判性审查：

代码质量分析：{code_analysis}
安全分析：{security_analysis}
调试分析：{debug_analysis}
架构分析：{architecture_analysis}

请质疑这些结论，寻找遗漏的问题，提出不同观点。
"""
        
        critic_review = await self.agents["critic"].process(
            critic_prompt,
            self.analysis_results
        )
        self.analysis_results["critic_review"] = critic_review
        self._log_conversation("system", "critic", critic_prompt)
        self._log_conversation("critic", "system", critic_review)
        print("✅ 质疑审查完成")
        
        # 第三轮：最终检查
        print("\n🔍 第三轮：检查者验证...")
        
        # 6. 检查者验证
        reviewer_prompt = f"""
请对整个分析过程进行最终验证：

所有分析结果：
{json.dumps(self.analysis_results, ensure_ascii=False, indent=2)}

质疑者意见：{critic_review}

请验证分析的准确性、一致性和完整性，提供最终评估。
"""
        
        final_review = await self.agents["reviewer"].process(
            reviewer_prompt,
            self.analysis_results
        )
        self.analysis_results["final_review"] = final_review
        self._log_conversation("system", "reviewer", reviewer_prompt)
        self._log_conversation("reviewer", "system", final_review)
        print("✅ 最终检查完成")
        
        # 第四轮：协调者总结
        print("\n📋 第四轮：协调者总结...")
        
        # 7. 协调者生成最终报告
        coordinator_prompt = f"""
基于所有智能体的分析结果，请生成最终的综合报告：

完整分析结果：
{json.dumps(self.analysis_results, ensure_ascii=False, indent=2)}

请整合所有观点，生成结构化的最终报告。
"""
        
        final_report = await self.agents["coordinator"].process(
            coordinator_prompt,
            self.analysis_results
        )
        self.analysis_results["final_report"] = final_report
        self._log_conversation("system", "coordinator", coordinator_prompt)
        self._log_conversation("coordinator", "system", final_report)
        print("✅ 综合报告生成完成")
        
        return {
            "status": "completed",
            "file_path": file_path,
            "analysis_results": self.analysis_results,
            "conversation_log": self.conversation_log,
            "agent_summary": self._generate_agent_summary()
        }
    
    def _generate_agent_summary(self) -> Dict[str, Any]:
        """生成智能体工作摘要"""
        summary = {}
        
        for agent_name, agent in self.agents.items():
            summary[agent_name] = {
                "role": agent.config.role,
                "llm_provider": agent.config.llm_provider,
                "interactions": len(agent.conversation_history),
                "status": "completed"
            }
        
        return summary

# 使用示例
async def main():
    """主函数示例"""
    
    # 创建增强的多智能体系统
    system = EnhancedMultiAgentSystem()
    
    # 分析示例文件
    file_path = "examples/unsafe_code.c"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 执行分析
        result = await system.analyze_code_file(file_path, code_content)
        
        # 保存结果
        output_file = f"analysis_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 分析完成！结果已保存到: {output_file}")
        print(f"📊 智能体参与数量: {len(result['agent_summary'])}")
        print(f"💬 对话记录数量: {len(result['conversation_log'])}")
        
    except FileNotFoundError:
        print(f"❌ 文件不存在: {file_path}")
    except Exception as e:
        print(f"❌ 分析失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
