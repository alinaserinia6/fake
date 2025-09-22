"""
智能体模块
包含不同角色的智能体定义和协作逻辑
"""

# 导入增强的多智能体系统
from .enhanced_multi_agent_system import EnhancedMultiAgentSystem, EnhancedAgent, LLMInterface

__all__ = [
    'EnhancedMultiAgentSystem',
    'EnhancedAgent', 
    'LLMInterface'
]
