"""
Multi-Agent Visualisation Usage Example

This example shows how to implement a hybrid architecture of AutoGen and LangGraph in Interruptr
"""

import asyncio
from typing import Dict, List, Any
import json
from datetime import datetime

# AutoGen imports (for conversation)
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import MessageContext

# LangGraph imports (for workflow)
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing_extensions import TypedDict

class AnalysisState(TypedDict):
    """Analysis state definition"""
    file_path: str
    code_content: str
    analysis_results: Dict[str, Any]
    current_step: str
    messages: List[Dict[str, str]]
    errors: List[str]

class HybridAgentSystem:
    """Hybrid agent system - combining AutoGen and LangGraph"""
    
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
        """Set up AutoGen agents"""
        
        # Code Analyst
        self.autogen_agents['code_analyst'] = AssistantAgent(
            name="code_analyst",
            system_message="""You are a professional C/C++ code analyst.
            Your task is to analyse code structure, calculate complexity metrics, and identify code quality issues.
            Please provide a detailed analysis report and improvement suggestions.""",
            llm_config=self.llm_config
        )
        
        # Security Expert
        self.autogen_agents['security_expert'] = AssistantAgent(
            name="security_expert", 
            system_message="""You are a C/C++ security expert.
            Focused on identifying security vulnerabilities: buffer overflows, memory leaks, null pointer dereferences, etc.
            Provide specific security risk assessments and remediation recommendations.""",
            llm_config=self.llm_config
        )
        
        # Debug Expert
        self.autogen_agents['debug_expert'] = AssistantAgent(
            name="debug_expert",
            system_message="""You are a debugging expert.
            Analyse code execution flow, recommend optimal breakpoint locations, and provide debugging strategies.
            Help developers debug and test code more effectively.""",
            llm_config=self.llm_config
        )
        
        # Architect
        self.autogen_agents['architect'] = AssistantAgent(
            name="architect",
            system_message="""You are a software architect.
            Evaluate the overall code architecture, design patterns, and maintainability.
            Provide refactoring recommendations and best practice guidance.""",
            llm_config=self.llm_config
        )
    
    def _setup_langgraph_workflow(self):
        """Set up LangGraph workflow"""
        
        # Create state graph
        workflow = StateGraph(AnalysisState)
        
        # Add nodes
        workflow.add_node("parse_code", self._parse_code_node)
        workflow.add_node("code_analysis", self._code_analysis_node)
        workflow.add_node("security_scan", self._security_scan_node)
        workflow.add_node("debug_analysis", self._debug_analysis_node)
        workflow.add_node("architecture_review", self._architecture_review_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # Add edges (workflow)
        workflow.set_entry_point("parse_code")
        workflow.add_edge("parse_code", "code_analysis")
        workflow.add_edge("code_analysis", "security_scan")
        workflow.add_edge("security_scan", "debug_analysis")
        workflow.add_edge("debug_analysis", "architecture_review")
        workflow.add_edge("architecture_review", "generate_report")
        workflow.add_edge("generate_report", END)
        
        # Compile workflow
        self.langgraph_workflow = workflow.compile()
    
    async def _parse_code_node(self, state: AnalysisState) -> AnalysisState:
        """Code parsing node"""
        
        self._log_workflow_state("parse_code", "Starting code structure parsing")
        
        # Call Tree-sitter or other parser here
        # Simulate parsing results
        parse_result = {
            "functions": ["unsafe_copy", "memory_leak_example", "null_pointer_risk", "complex_function"],
            "lines": 67,
            "complexity": 8
        }
        
        state["analysis_results"]["parse"] = parse_result
        state["current_step"] = "code_analysis"
        
        return state
    
    async def _code_analysis_node(self, state: AnalysisState) -> AnalysisState:
        """Code analysis node - calls AutoGen agent"""
        
        self._log_workflow_state("code_analysis", "Starting code analysis agent")
        
        # Create analysis task
        analysis_prompt = f"""
        Please analyse the following code file: {state['file_path']}

        Parse results: {state['analysis_results']['parse']}

        Please provide a detailed code quality analysis, including:
        1. Function complexity assessment
        2. Code structure analysis
        3. Maintainability evaluation
        4. Improvement suggestions
        """
        
        # Use AutoGen for analysis
        agent = self.autogen_agents['code_analyst']
        response = await self._call_autogen_agent(agent, analysis_prompt)
        
        self._log_conversation("system", "code_analyst", analysis_prompt)
        self._log_conversation("code_analyst", "system", response)
        
        state["analysis_results"]["code_quality"] = response
        state["current_step"] = "security_scan"
        
        return state
    
    async def _security_scan_node(self, state: AnalysisState) -> AnalysisState:
        """Security scan node"""
        
        self._log_workflow_state("security_scan", "Starting security analysis agent")
        
        security_prompt = f"""
        Based on the code analysis results, please perform security vulnerability detection:

        Code quality analysis: {state['analysis_results']['code_quality']}

        Focus on detecting:
        1. Buffer overflow risks
        2. Memory leak issues
        3. Null pointer dereferences
        4. Integer overflows
        """
        
        agent = self.autogen_agents['security_expert']
        response = await self._call_autogen_agent(agent, security_prompt)
        
        self._log_conversation("system", "security_expert", security_prompt)
        self._log_conversation("security_expert", "system", response)
        
        state["analysis_results"]["security"] = response
        state["current_step"] = "debug_analysis"
        
        return state
    
    async def _debug_analysis_node(self, state: AnalysisState) -> AnalysisState:
        """Debug analysis node"""
        
        self._log_workflow_state("debug_analysis", "Starting debug analysis agent")
        
        debug_prompt = f"""
        Based on the previous analysis results, please provide debugging suggestions:

        Security analysis: {state['analysis_results']['security']}

        Please provide:
        1. Recommended breakpoint locations
        2. Debugging strategies
        3. Testing suggestions
        """
        
        agent = self.autogen_agents['debug_expert']
        response = await self._call_autogen_agent(agent, debug_prompt)
        
        self._log_conversation("system", "debug_expert", debug_prompt)
        self._log_conversation("debug_expert", "system", response)
        
        state["analysis_results"]["debug"] = response
        state["current_step"] = "architecture_review"
        
        return state
    
    async def _architecture_review_node(self, state: AnalysisState) -> AnalysisState:
        """Architecture review node"""
        
        self._log_workflow_state("architecture_review", "Starting architecture review agent")
        
        arch_prompt = f"""
        Perform overall architecture assessment:

        Comprehensive analysis results: {json.dumps(state['analysis_results'], ensure_ascii=False, indent=2)}

        Please evaluate:
        1. Overall architecture quality
        2. Design pattern usage
        3. Refactoring suggestions
        """
        
        agent = self.autogen_agents['architect']
        response = await self._call_autogen_agent(agent, arch_prompt)
        
        self._log_conversation("system", "architect", arch_prompt)
        self._log_conversation("architect", "system", response)
        
        state["analysis_results"]["architecture"] = response
        state["current_step"] = "generate_report"
        
        return state
    
    async def _generate_report_node(self, state: AnalysisState) -> AnalysisState:
        """Generate report node"""
        
        self._log_workflow_state("generate_report", "Generating comprehensive analysis report")
        
        # Generate final report
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
        """Call AutoGen agent"""
        
        # Actual AutoGen API call would go here
        # Simplified mock responses
        agent_responses = {
            "code_analyst": "Code structure analysis complete; functions with high complexity need refactoring",
            "security_expert": "Buffer overflow risk detected; it is recommended to use safe string functions",
            "debug_expert": "Recommended to set breakpoints at lines 12 and 27 for debugging",
            "architect": "Suggest refactoring complex functions to improve code maintainability"
        }
        
        return agent_responses.get(agent.name, "Analysis complete")
    
    def _log_conversation(self, sender: str, receiver: str, message: str):
        """Log a conversation"""
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "type": "chat"
        }
        
        self.visualization_data["conversations"].append(conversation_entry)
        
        # Update interaction graph
        if sender not in self.visualization_data["interaction_graph"]:
            self.visualization_data["interaction_graph"][sender] = []
        if receiver not in self.visualization_data["interaction_graph"][sender]:
            self.visualization_data["interaction_graph"][sender].append(receiver)
    
    def _log_workflow_state(self, node: str, description: str):
        """Log workflow state"""
        state_entry = {
            "timestamp": datetime.now().isoformat(),
            "node": node,
            "description": description,
            "step": len(self.visualization_data["workflow_states"]) + 1
        }
        
        self.visualization_data["workflow_states"].append(state_entry)
    
    async def analyze_code(self, file_path: str, code_content: str) -> Dict[str, Any]:
        """Execute the complete code analysis"""
        
        # Initialise state
        initial_state = AnalysisState(
            file_path=file_path,
            code_content=code_content,
            analysis_results={},
            current_step="parse_code",
            messages=[],
            errors=[]
        )
        
        # Execute LangGraph workflow
        result = await self.langgraph_workflow.ainvoke(initial_state)
        
        return {
            "analysis_results": result["analysis_results"],
            "visualization_data": self.visualization_data
        }

# Usage example
async def main():
    """Main function example"""
    
    # LLM configuration
    llm_config = {
        "model": "gpt-4",
        "api_key": "your-api-key",
        "temperature": 0.1
    }
    
    # Create hybrid agent system
    hybrid_system = HybridAgentSystem(llm_config)
    
    # Analyse code
    file_path = "examples/unsafe_code.c"
    with open(file_path, 'r') as f:
        code_content = f.read()
    
    result = await hybrid_system.analyze_code(file_path, code_content)
    
    # Output results
    print("Analysis complete!")
    print(f"Number of conversation entries: {len(result['visualization_data']['conversations'])}")
    print(f"Workflow steps: {len(result['visualization_data']['workflow_states'])}")
    
    # Save visualisation data
    with open("visualization_data.json", "w") as f:
        json.dump(result["visualization_data"], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
