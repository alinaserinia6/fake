"""
多智能体可视化使用示例

这个示例展示如何在Interruptr中实现AutoGen和LangGraph的混合架构
"""

import asyncio
from typing import Dict, List, Any
import json
from datetime import datetime

# AutoGen导入 (用于对话)
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import MessageContext

# LangGraph导入 (用于工作流)
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing_extensions import TypedDict

class AnalysisState(TypedDict):
    """分析状态定义"""
    file_path: str
    code_content: str
    analysis_results: Dict[str, Any]
    current_step: str
    messages: List[Dict[str, str]]
    errors: List[str]

class HybridAgentSystem:
    """混合智能体系统 - 结合AutoGen和LangGraph"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.autogen_agents = {}
        self.langgraph_workflow = None
        self.visualization_data = {
            "conversations": [],
            "workflow_states": [],
            "interaction_graph": {}
        }
        
        self._setup_autogen_agents()
        self._setup_langgraph_workflow()
    
    def _setup_autogen_agents(self):
        """设置AutoGen智能体"""
        
        # 代码分析师
        self.autogen_agents['code_analyst'] = AssistantAgent(
            name="code_analyst",
            system_message="""你是一个专业的C/C++代码分析师。
            你的任务是分析代码结构、计算复杂度指标、识别代码质量问题。
            请提供详细的分析报告和改进建议。""",
            llm_config=self.llm_config
        )
        
        # 安全专家
        self.autogen_agents['security_expert'] = AssistantAgent(
            name="security_expert", 
            system_message="""你是一个C/C++安全专家。
            专注于识别安全漏洞：缓冲区溢出、内存泄漏、空指针解引用等。
            提供具体的安全风险评估和修复建议。""",
            llm_config=self.llm_config
        )
        
        # 调试专家
        self.autogen_agents['debug_expert'] = AssistantAgent(
            name="debug_expert",
            system_message="""你是一个调试专家。
            分析代码执行流程，推荐最佳断点位置，提供调试策略。
            帮助开发者更有效地调试和测试代码。""",
            llm_config=self.llm_config
        )
        
        # 架构师
        self.autogen_agents['architect'] = AssistantAgent(
            name="architect",
            system_message="""你是一个软件架构师。
            评估代码的整体架构、设计模式、可维护性。
            提供重构建议和最佳实践指导。""",
            llm_config=self.llm_config
        )
    
    def _setup_langgraph_workflow(self):
        """设置LangGraph工作流"""
        
        # 创建状态图
        workflow = StateGraph(AnalysisState)
        
        # 添加节点
        workflow.add_node("parse_code", self._parse_code_node)
        workflow.add_node("code_analysis", self._code_analysis_node)
        workflow.add_node("security_scan", self._security_scan_node)
        workflow.add_node("debug_analysis", self._debug_analysis_node)
        workflow.add_node("architecture_review", self._architecture_review_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # 添加边（工作流）
        workflow.set_entry_point("parse_code")
        workflow.add_edge("parse_code", "code_analysis")
        workflow.add_edge("code_analysis", "security_scan")
        workflow.add_edge("security_scan", "debug_analysis")
        workflow.add_edge("debug_analysis", "architecture_review")
        workflow.add_edge("architecture_review", "generate_report")
        workflow.add_edge("generate_report", END)
        
        # 编译工作流
        self.langgraph_workflow = workflow.compile()
    
    async def _parse_code_node(self, state: AnalysisState) -> AnalysisState:
        """代码解析节点"""
        
        self._log_workflow_state("parse_code", "开始解析代码结构")
        
        # 这里调用Tree-sitter或其他解析器
        # 模拟解析结果
        parse_result = {
            "functions": ["unsafe_copy", "memory_leak_example", "null_pointer_risk", "complex_function"],
            "lines": 67,
            "complexity": 8
        }
        
        state["analysis_results"]["parse"] = parse_result
        state["current_step"] = "code_analysis"
        
        return state
    
    async def _code_analysis_node(self, state: AnalysisState) -> AnalysisState:
        """代码分析节点 - 调用AutoGen智能体"""
        
        self._log_workflow_state("code_analysis", "启动代码分析智能体")
        
        # 创建分析任务
        analysis_prompt = f"""
        请分析以下代码文件: {state['file_path']}
        
        解析结果: {state['analysis_results']['parse']}
        
        请提供详细的代码质量分析，包括：
        1. 函数复杂度评估
        2. 代码结构分析
        3. 可维护性评价
        4. 改进建议
        """
        
        # 使用AutoGen进行分析
        agent = self.autogen_agents['code_analyst']
        response = await self._call_autogen_agent(agent, analysis_prompt)
        
        self._log_conversation("system", "code_analyst", analysis_prompt)
        self._log_conversation("code_analyst", "system", response)
        
        state["analysis_results"]["code_quality"] = response
        state["current_step"] = "security_scan"
        
        return state
    
    async def _security_scan_node(self, state: AnalysisState) -> AnalysisState:
        """安全扫描节点"""
        
        self._log_workflow_state("security_scan", "启动安全分析智能体")
        
        security_prompt = f"""
        基于代码分析结果，请进行安全漏洞检测：
        
        代码质量分析: {state['analysis_results']['code_quality']}
        
        重点检测：
        1. 缓冲区溢出风险
        2. 内存泄漏问题
        3. 空指针解引用
        4. 整数溢出
        """
        
        agent = self.autogen_agents['security_expert']
        response = await self._call_autogen_agent(agent, security_prompt)
        
        self._log_conversation("system", "security_expert", security_prompt)
        self._log_conversation("security_expert", "system", response)
        
        state["analysis_results"]["security"] = response
        state["current_step"] = "debug_analysis"
        
        return state
    
    async def _debug_analysis_node(self, state: AnalysisState) -> AnalysisState:
        """调试分析节点"""
        
        self._log_workflow_state("debug_analysis", "启动调试分析智能体")
        
        debug_prompt = f"""
        基于前面的分析结果，请提供调试建议：
        
        安全分析: {state['analysis_results']['security']}
        
        请提供：
        1. 推荐断点位置
        2. 调试策略
        3. 测试建议
        """
        
        agent = self.autogen_agents['debug_expert']
        response = await self._call_autogen_agent(agent, debug_prompt)
        
        self._log_conversation("system", "debug_expert", debug_prompt)
        self._log_conversation("debug_expert", "system", response)
        
        state["analysis_results"]["debug"] = response
        state["current_step"] = "architecture_review"
        
        return state
    
    async def _architecture_review_node(self, state: AnalysisState) -> AnalysisState:
        """架构评审节点"""
        
        self._log_workflow_state("architecture_review", "启动架构评审智能体")
        
        arch_prompt = f"""
        进行整体架构评估：
        
        综合分析结果: {json.dumps(state['analysis_results'], ensure_ascii=False, indent=2)}
        
        请评估：
        1. 整体架构质量
        2. 设计模式使用
        3. 重构建议
        """
        
        agent = self.autogen_agents['architect']
        response = await self._call_autogen_agent(agent, arch_prompt)
        
        self._log_conversation("system", "architect", arch_prompt)
        self._log_conversation("architect", "system", response)
        
        state["analysis_results"]["architecture"] = response
        state["current_step"] = "generate_report"
        
        return state
    
    async def _generate_report_node(self, state: AnalysisState) -> AnalysisState:
        """生成报告节点"""
        
        self._log_workflow_state("generate_report", "生成综合分析报告")
        
        # 生成综合报告
        report = {
            "file_path": state["file_path"],
            "timestamp": datetime.now().isoformat(),
            "analysis_results": state["analysis_results"],
            "visualization_data": self.visualization_data
        }
        
        state["analysis_results"]["final_report"] = report
        state["current_step"] = "completed"
        
        return state
    
    async def _call_autogen_agent(self, agent: AssistantAgent, prompt: str) -> str:
        """调用AutoGen智能体"""
        
        # 这里需要根据实际的AutoGen API调用
        # 简化的模拟响应
        agent_responses = {
            "code_analyst": "代码结构分析完成，发现复杂度较高的函数需要重构",
            "security_expert": "检测到缓冲区溢出风险，建议使用安全的字符串函数",
            "debug_expert": "推荐在第12行和第27行设置断点进行调试",
            "architect": "建议重构复杂函数，提高代码可维护性"
        }
        
        return agent_responses.get(agent.name, "分析完成")
    
    def _log_conversation(self, sender: str, receiver: str, message: str):
        """记录对话"""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "type": "chat"
        }
        
        self.visualization_data["conversations"].append(conversation_entry)
        
        # 更新交互图
        if sender not in self.visualization_data["interaction_graph"]:
            self.visualization_data["interaction_graph"][sender] = []
        if receiver not in self.visualization_data["interaction_graph"][sender]:
            self.visualization_data["interaction_graph"][sender].append(receiver)
    
    def _log_workflow_state(self, node: str, description: str):
        """记录工作流状态"""
        state_entry = {
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "description": description,
            "step": len(self.visualization_data["workflow_states"]) + 1
        }
        
        self.visualization_data["workflow_states"].append(state_entry)
    
    async def analyze_code(self, file_path: str, code_content: str) -> Dict[str, Any]:
        """执行完整的代码分析"""
        
        # 初始化状态
        initial_state = AnalysisState(
            file_path=file_path,
            code_content=code_content,
            analysis_results={},
            current_step="parse_code",
            messages=[],
            errors=[]
        )
        
        # 执行LangGraph工作流
        result = await self.langgraph_workflow.ainvoke(initial_state)
        
        return {
            "analysis_results": result["analysis_results"],
            "visualization_data": self.visualization_data
        }

# 使用示例
async def main():
    """主函数示例"""
    
    # LLM配置
    llm_config = {
        "model": "gpt-4",
        "api_key": "your-api-key",
        "temperature": 0.1
    }
    
    # 创建混合智能体系统
    hybrid_system = HybridAgentSystem(llm_config)
    
    # 分析代码
    file_path = "examples/unsafe_code.c"
    with open(file_path, 'r') as f:
        code_content = f.read()
    
    result = await hybrid_system.analyze_code(file_path, code_content)
    
    # 输出结果
    print("分析完成!")
    print(f"对话记录数量: {len(result['visualization_data']['conversations'])}")
    print(f"工作流步骤: {len(result['visualization_data']['workflow_states'])}")
    
    # 保存可视化数据
    with open("visualization_data.json", "w") as f:
        json.dump(result["visualization_data"], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
