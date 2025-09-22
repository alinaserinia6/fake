"""
基于 LangGraph 的多智能体 C++ 代码分析系统
"""

import os
import sys
from typing import Dict, List, Any, TypedDict, Annotated
import operator
import json

# LangGraph imports
try:
    from langgraph.graph import StateGraph, MessagesState, START, END
    from langgraph.prebuilt import create_react_agent
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    print(f"LangGraph 导入失败: {e}")
    LANGGRAPH_AVAILABLE = False

# LangChain imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_anthropic import ChatAnthropic
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"LangChain 导入失败: {e}")
    LANGCHAIN_AVAILABLE = False

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.env_config import config

# 定义状态类型
class AnalysisState(TypedDict):
    code_content: str
    filename: str
    messages: Annotated[list, operator.add]
    code_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any] 
    debug_analysis: Dict[str, Any]
    architecture_analysis: Dict[str, Any]
    final_report: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]

class LangGraphCodeAnalyzer:
    """基于 LangGraph 的多智能体代码分析器"""
    
    def __init__(self):
        self.llm = None
        self.graph = None
        self.conversation_history = []
        
    def setup_llm(self):
        """设置 LLM - 暂时禁用，使用模拟模式"""
        # 暂时返回 None，使用模拟模式展示多智能体工作流
        return None
    
    def create_agent_nodes(self):
        """创建智能体节点"""
        
        def coordinator_node(state: AnalysisState):
            """协调者节点"""
            prompt = f"""
你是一个智能的代码分析协调者。请分析以下 C/C++ 代码：

文件名: {state['filename']}
代码内容:
```cpp
{state['code_content']}
```

请提供一个整体的分析计划，包括需要关注的重点领域。
            """
            
            if self.llm:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                message_content = response.content
            else:
                message_content = f"协调者开始分析 {state['filename']}，制定分析计划..."
            
            conversation_entry = {
                "agent": "coordinator",
                "agent_name": "🎯 协调者",
                "message": message_content,
                "timestamp": "2025-08-30 16:41:00",
                "reasoning": "制定整体分析策略和工作分配"
            }
            
            return {
                "messages": [AIMessage(content=message_content)],
                "conversation_history": [conversation_entry]
            }
        
        def code_analyst_node(state: AnalysisState):
            """代码分析师节点"""
            prompt = f"""
作为 C/C++ 代码分析师，请分析以下代码的质量指标：

代码内容:
```cpp
{state['code_content']}
```

请重点分析：
1. 代码复杂度
2. 函数设计质量
3. 变量命名规范
4. 代码结构和组织
5. 性能考虑

提供具体的分析结果和改进建议。
            """
            
            if self.llm:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                message_content = response.content
                
                # 简单解析分析结果
                analysis_result = {
                    "complexity": "medium",
                    "quality_score": 7.5,
                    "issues": [],
                    "suggestions": []
                }
            else:
                # 简单的静态分析
                lines = state['code_content'].split('\n')
                code_lines = [line for line in lines if line.strip() and not line.strip().startswith('//')]
                
                analysis_result = {
                    "total_lines": len(lines),
                    "code_lines": len(code_lines),
                    "complexity": "medium" if len(code_lines) > 20 else "low",
                    "function_count": state['code_content'].count('('),
                    "quality_score": 8.0
                }
                
                message_content = f"代码质量分析完成：\n总行数：{len(lines)}\n有效代码行：{len(code_lines)}\n复杂度：{analysis_result['complexity']}\n质量评分：{analysis_result['quality_score']}/10"
            
            conversation_entry = {
                "agent": "code_analyst",
                "agent_name": "📊 代码分析师", 
                "message": message_content,
                "timestamp": "2025-08-30 16:41:05",
                "reasoning": "基于静态分析和代码度量进行质量评估"
            }
            
            return {
                "messages": [AIMessage(content=message_content)],
                "code_analysis": analysis_result,
                "conversation_history": [conversation_entry]
            }
        
        def security_expert_node(state: AnalysisState):
            """安全专家节点"""
            prompt = f"""
作为 C/C++ 安全专家，请分析以下代码的安全问题：

代码内容:
```cpp
{state['code_content']}
```

请重点检查：
1. 缓冲区溢出风险
2. 内存泄漏可能性
3. 危险函数使用
4. 输入验证缺失
5. 整数溢出
6. 空指针解引用

提供具体的安全问题位置和修复建议。
            """
            
            # 简单的安全检查
            security_issues = []
            code = state['code_content']
            
            if 'strcpy' in code:
                security_issues.append({
                    "type": "缓冲区溢出",
                    "function": "strcpy",
                    "severity": "高",
                    "description": "strcpy 函数不检查目标缓冲区大小，可能导致缓冲区溢出"
                })
            
            if 'gets' in code:
                security_issues.append({
                    "type": "缓冲区溢出", 
                    "function": "gets",
                    "severity": "严重",
                    "description": "gets 函数极易导致缓冲区溢出，应避免使用"
                })
            
            if 'malloc' in code and 'free' not in code:
                security_issues.append({
                    "type": "内存泄漏",
                    "function": "malloc",
                    "severity": "中",
                    "description": "使用 malloc 分配内存但未找到对应的 free 调用"
                })
            
            if 'scanf' in code:
                security_issues.append({
                    "type": "输入验证",
                    "function": "scanf", 
                    "severity": "中",
                    "description": "scanf 可能导致缓冲区溢出，建议使用更安全的输入函数"
                })
            
            if self.llm:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                message_content = response.content
            else:
                if security_issues:
                    message_content = f"安全分析完成，发现 {len(security_issues)} 个安全问题：\n"
                    for issue in security_issues:
                        message_content += f"- {issue['type']}（{issue['severity']}）: {issue['description']}\n"
                else:
                    message_content = "✅ 安全分析完成，未发现明显的安全问题"
            
            conversation_entry = {
                "agent": "security_expert",
                "agent_name": "🔒 安全专家",
                "message": message_content,
                "timestamp": "2025-08-30 16:41:10", 
                "reasoning": "基于安全漏洞库和模式匹配进行安全风险评估"
            }
            
            return {
                "messages": [AIMessage(content=message_content)],
                "security_analysis": {
                    "issues": security_issues,
                    "risk_level": "high" if any(i['severity'] == '严重' for i in security_issues) else "medium" if security_issues else "low"
                },
                "conversation_history": [conversation_entry]
            }
        
        def debug_expert_node(state: AnalysisState):
            """调试专家节点"""
            prompt = f"""
作为 C/C++ 调试专家，请为以下代码提供调试建议：

代码内容:
```cpp
{state['code_content']}
```

请提供：
1. 推荐的调试工具
2. 关键断点位置
3. 日志记录建议  
4. 错误处理评估
5. 调试策略

提供实用的调试指导。
            """
            
            if self.llm:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                message_content = response.content
            else:
                # 基本调试建议
                debug_suggestions = [
                    "使用 gdb 进行源码级调试",
                    "编译时添加 -g -O0 选项保留调试信息",
                    "使用 Valgrind 检测内存错误", 
                    "添加断点在函数入口和关键循环处",
                    "使用 printf/cout 添加日志输出"
                ]
                
                message_content = "调试建议：\n" + "\n".join([f"- {suggestion}" for suggestion in debug_suggestions])
            
            conversation_entry = {
                "agent": "debug_expert",
                "agent_name": "🐛 调试专家",
                "message": message_content,
                "timestamp": "2025-08-30 16:41:15",
                "reasoning": "基于代码特征和最佳实践提供调试策略"
            }
            
            return {
                "messages": [AIMessage(content=message_content)],
                "debug_analysis": {
                    "tools": ["gdb", "valgrind", "printf"],
                    "strategies": ["断点调试", "内存检测", "日志跟踪"]
                },
                "conversation_history": [conversation_entry]
            }
        
        def architect_node(state: AnalysisState):
            """架构师节点"""
            prompt = f"""
作为软件架构师，请评估以下代码的设计质量：

代码内容:
```cpp
{state['code_content']}
```

请从以下角度分析：
1. SOLID 原则遵循情况
2. 设计模式使用
3. 模块化程度
4. 接口设计质量
5. 可维护性和扩展性

提供架构改进建议。
            """
            
            if self.llm:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                message_content = response.content
            else:
                # 简单的架构分析
                lines = state['code_content'].split('\n')
                
                architecture_score = 7.0
                if len(lines) > 100:
                    architecture_score -= 1.0  # 复杂度较高
                if 'class' in state['code_content']:
                    architecture_score += 1.0  # 使用面向对象
                
                message_content = f"架构分析：\n- 代码组织：{'良好' if len(lines) < 100 else '需要优化'}\n- 面向对象：{'使用' if 'class' in state['code_content'] else '未使用'}\n- 架构评分：{architecture_score}/10"
            
            conversation_entry = {
                "agent": "architect",
                "agent_name": "🏗️ 架构师",
                "message": message_content,
                "timestamp": "2025-08-30 16:41:20",
                "reasoning": "从软件工程和设计模式角度评估代码架构"
            }
            
            return {
                "messages": [AIMessage(content=message_content)],
                "architecture_analysis": {
                    "score": 7.5,
                    "patterns": [],
                    "suggestions": ["模块化改进", "接口优化"]
                },
                "conversation_history": [conversation_entry]
            }
        
        def final_report_node(state: AnalysisState):
            """最终报告节点"""
            
            # 汇总所有分析结果
            code_analysis = state.get('code_analysis', {})
            security_analysis = state.get('security_analysis', {})
            debug_analysis = state.get('debug_analysis', {})
            architecture_analysis = state.get('architecture_analysis', {})
            
            # 计算综合评分
            quality_score = code_analysis.get('quality_score', 7.0)
            security_score = 10.0 if security_analysis.get('risk_level') == 'low' else 5.0 if security_analysis.get('risk_level') == 'medium' else 2.0
            architecture_score = architecture_analysis.get('score', 7.0)
            
            overall_score = (quality_score + security_score + architecture_score) / 3
            
            issues_count = len(security_analysis.get('issues', []))
            
            report_content = f"""
🎯 综合分析报告

📊 质量评分：{quality_score:.1f}/10
🔒 安全评分：{security_score:.1f}/10  
🏗️ 架构评分：{architecture_score:.1f}/10
📈 综合评分：{overall_score:.1f}/10

🔍 发现问题：{issues_count} 个
✅ 分析完成：所有智能体协作完成分析

建议：{'优先修复安全问题' if issues_count > 0 else '代码质量良好，继续保持'}
            """
            
            conversation_entry = {
                "agent": "final_report",
                "agent_name": "📋 最终报告",
                "message": report_content.strip(),
                "timestamp": "2025-08-30 16:41:25",
                "reasoning": "汇总所有智能体分析结果，生成综合评估报告"
            }
            
            final_report = {
                "overall_score": overall_score,
                "quality_score": quality_score,
                "security_score": security_score,
                "architecture_score": architecture_score,
                "issues_count": issues_count,
                "recommendation": "优先修复安全问题" if issues_count > 0 else "代码质量良好，继续保持"
            }
            
            return {
                "messages": [AIMessage(content=report_content)],
                "final_report": final_report,
                "conversation_history": [conversation_entry]
            }
        
        return {
            "coordinator": coordinator_node,
            "code_analyst": code_analyst_node,
            "security_expert": security_expert_node,
            "debug_expert": debug_expert_node,
            "architect": architect_node,
            "final_report": final_report_node
        }
    
    def build_graph(self):
        """构建 LangGraph 工作流"""
        
        if not LANGGRAPH_AVAILABLE:
            return None
        
        # 创建状态图
        workflow = StateGraph(AnalysisState)
        
        # 获取智能体节点
        nodes = self.create_agent_nodes()
        
        # 添加节点
        for name, func in nodes.items():
            workflow.add_node(name, func)
        
        # 定义工作流程
        workflow.add_edge(START, "coordinator")
        workflow.add_edge("coordinator", "code_analyst")
        workflow.add_edge("code_analyst", "security_expert") 
        workflow.add_edge("security_expert", "debug_expert")
        workflow.add_edge("debug_expert", "architect")
        workflow.add_edge("architect", "final_report")
        workflow.add_edge("final_report", END)
        
        # 编译图
        return workflow.compile()
    
    async def analyze_code(self, code_content: str, filename: str) -> Dict[str, Any]:
        """使用 LangGraph 多智能体分析代码"""
        
        print(f"🔍 LangGraph 分析文件: {filename}")
        
        # 暂时直接使用模拟模式，展示多智能体工作流
        return await self.run_mock_analysis(code_content, filename)
    
    async def run_mock_analysis(self, code_content: str, filename: str) -> Dict[str, Any]:
        """运行模拟的 LangGraph 分析"""
        
        print("🎭 运行模拟 LangGraph 分析模式")
        
        # 复用 AutoGen 的模拟逻辑，但标记为 LangGraph
        from .autogen_analyzer import autogen_analyzer
        result = await autogen_analyzer.run_mock_analysis(code_content, filename)
        
        # 修改类型标识
        result["analysis_type"] = "langgraph_mock"
        
        # 添加 LangGraph 特定的结构
        result["workflow_steps"] = [
            "coordinator → code_analyst → security_expert → debug_expert → architect → final_report"
        ]
        
        return result

# 全局分析器实例
langgraph_analyzer = LangGraphCodeAnalyzer()
