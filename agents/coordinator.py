"""
协调者智能体 - 管理和协调其他智能体的工作流程
"""

import asyncio
from typing import List, Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult

class CoordinatorAgent:
    """协调者智能体，负责管理多智能体协作流程"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.agents: List[AssistantAgent] = []
        self.current_task = None
        
    def add_agent(self, agent: AssistantAgent):
        """添加智能体到协作团队"""
        self.agents.append(agent)
        
    async def coordinate_analysis(self, code_path: str, task_description: str) -> Dict[str, Any]:
        """协调多智能体进行代码分析"""
        
        # 创建智能体团队
        team = RoundRobinGroupChat(self.agents)
        
        # 构建分析任务
        analysis_prompt = f"""
        请对以下C/C++代码文件进行全面分析：{code_path}
        
        任务描述：{task_description}
        
        请按照以下步骤进行协作分析：
        1. 代码分析师：进行静态代码分析，识别代码结构和潜在问题
        2. 安全专家：检测安全漏洞和风险点
        3. 调试专家：分析断点设置和执行流程
        4. 架构师：评估整体架构和设计质量
        
        每个专家请提供详细的分析报告和建议。
        """
        
        try:
            # 执行协作分析
            result = await team.run(
                task=analysis_prompt,
                max_turns=20
            )
            
            return {
                "status": "success",
                "analysis_result": result,
                "agents_participated": [agent.name for agent in self.agents],
                "task_completed": True
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error_message": str(e),
                "task_completed": False
            }
    
    def create_analysis_workflow(self, code_files: List[str]) -> Dict[str, Any]:
        """创建代码分析工作流"""
        
        workflow = {
            "steps": [
                {
                    "step": 1,
                    "agent": "code_analyst",
                    "task": "静态代码分析",
                    "input": code_files,
                    "expected_output": "代码结构分析、复杂度评估、代码质量报告"
                },
                {
                    "step": 2, 
                    "agent": "security_expert",
                    "task": "安全漏洞检测",
                    "input": "代码分析结果",
                    "expected_output": "安全漏洞报告、风险评估、修复建议"
                },
                {
                    "step": 3,
                    "agent": "debug_expert", 
                    "task": "调试分析",
                    "input": "代码和安全分析结果",
                    "expected_output": "断点建议、执行路径分析、调试策略"
                },
                {
                    "step": 4,
                    "agent": "architect",
                    "task": "架构评估",
                    "input": "所有分析结果",
                    "expected_output": "架构质量评估、设计模式分析、重构建议"
                }
            ],
            "final_output": "综合分析报告和改进建议"
        }
        
        return workflow
    
    def generate_summary_report(self, analysis_results: Dict[str, Any]) -> str:
        """生成综合分析报告"""
        
        report = f"""
# Interruptr 代码分析报告

## 分析概览
- 分析状态: {analysis_results.get('status', 'unknown')}
- 参与智能体: {', '.join(analysis_results.get('agents_participated', []))}
- 任务完成: {analysis_results.get('task_completed', False)}

## 分析结果
{analysis_results.get('analysis_result', '无分析结果')}

## 建议改进
基于多智能体协作分析，建议从以下方面改进代码：

1. **代码质量**: 提高代码可读性和维护性
2. **安全性**: 修复识别的安全漏洞
3. **调试性**: 优化调试和测试策略  
4. **架构**: 改进整体设计和架构

## 下一步行动
1. 优先修复高危安全漏洞
2. 重构复杂度过高的代码段
3. 添加必要的错误处理和边界检查
4. 完善测试用例和文档

---
由 Interruptr 多智能体系统生成
        """
        
        return report
