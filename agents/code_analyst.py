"""
代码分析师智能体 - 专注于静态代码分析和代码质量评估
"""

import os
from typing import Dict, List, Any
from pathlib import Path
import tree_sitter
from tree_sitter import Language, Parser
import tree_sitter_cpp as tscpp

class CodeAnalystAgent:
    """代码分析师智能体，负责静态代码分析"""
    
    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.name = "代码分析师"
        self.role = "静态代码分析和代码质量评估"
        
        # 初始化Tree-sitter解析器
        self.language = Language(tscpp.language(), "cpp")
        self.parser = Parser()
        self.parser.set_language(self.language)
        
    def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """分析单个代码文件"""
        
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
                
            # 使用Tree-sitter解析代码
            tree = self.parser.parse(bytes(code_content, 'utf-8'))
            
            analysis_result = {
                "file_path": file_path,
                "file_size": len(code_content),
                "line_count": code_content.count('\n') + 1,
                "functions": self._extract_functions(tree.root_node, code_content),
                "classes": self._extract_classes(tree.root_node, code_content),
                "includes": self._extract_includes(tree.root_node, code_content),
                "complexity_metrics": self._calculate_complexity(tree.root_node, code_content),
                "potential_issues": self._identify_issues(tree.root_node, code_content)
            }
            
            return analysis_result
            
        except Exception as e:
            return {"error": f"分析文件时出错: {str(e)}"}
    
    def _extract_functions(self, node, code_content: str) -> List[Dict[str, Any]]:
        """提取函数信息"""
        functions = []
        
        def traverse(node):
            if node.type == 'function_definition':
                # 获取函数名
                name_node = None
                for child in node.children:
                    if child.type == 'function_declarator':
                        for subchild in child.children:
                            if subchild.type == 'identifier':
                                name_node = subchild
                                break
                        break
                
                if name_node:
                    func_info = {
                        "name": code_content[name_node.start_byte:name_node.end_byte],
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "line_count": node.end_point[0] - node.start_point[0] + 1,
                        "parameters": self._extract_parameters(node, code_content),
                        "return_type": self._extract_return_type(node, code_content)
                    }
                    functions.append(func_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return functions
    
    def _extract_classes(self, node, code_content: str) -> List[Dict[str, Any]]:
        """提取类信息"""
        classes = []
        
        def traverse(node):
            if node.type == 'class_specifier':
                name_node = None
                for child in node.children:
                    if child.type == 'type_identifier':
                        name_node = child
                        break
                
                if name_node:
                    class_info = {
                        "name": code_content[name_node.start_byte:name_node.end_byte],
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                        "line_count": node.end_point[0] - node.start_point[0] + 1,
                        "methods": self._extract_class_methods(node, code_content),
                        "members": self._extract_class_members(node, code_content)
                    }
                    classes.append(class_info)
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return classes
    
    def _extract_includes(self, node, code_content: str) -> List[str]:
        """提取包含的头文件"""
        includes = []
        
        def traverse(node):
            if node.type == 'preproc_include':
                include_text = code_content[node.start_byte:node.end_byte]
                includes.append(include_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return includes
    
    def _calculate_complexity(self, node, code_content: str) -> Dict[str, Any]:
        """计算代码复杂度指标"""
        
        complexity_metrics = {
            "cyclomatic_complexity": 0,
            "nesting_depth": 0,
            "function_count": 0,
            "class_count": 0,
            "max_function_length": 0
        }
        
        # 简化的圈复杂度计算
        decision_points = 0
        max_depth = 0
        current_depth = 0
        
        def traverse(node):
            nonlocal decision_points, max_depth, current_depth
            
            # 决策点节点
            if node.type in ['if_statement', 'while_statement', 'for_statement', 
                           'switch_statement', 'case_statement', 'conditional_expression']:
                decision_points += 1
            
            # 嵌套深度
            if node.type in ['compound_statement', 'if_statement', 'while_statement', 'for_statement']:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            
            for child in node.children:
                traverse(child)
            
            if node.type in ['compound_statement', 'if_statement', 'while_statement', 'for_statement']:
                current_depth -= 1
        
        traverse(node)
        
        complexity_metrics["cyclomatic_complexity"] = decision_points + 1
        complexity_metrics["nesting_depth"] = max_depth
        
        return complexity_metrics
    
    def _identify_issues(self, node, code_content: str) -> List[Dict[str, Any]]:
        """识别潜在的代码问题"""
        issues = []
        
        def traverse(node):
            # 检查过长的函数
            if node.type == 'function_definition':
                line_count = node.end_point[0] - node.start_point[0] + 1
                if line_count > 50:
                    issues.append({
                        "type": "long_function",
                        "severity": "warning",
                        "line": node.start_point[0] + 1,
                        "message": f"函数过长 ({line_count} 行)，建议拆分"
                    })
            
            # 检查深度嵌套
            if self._calculate_nesting_depth(node) > 4:
                issues.append({
                    "type": "deep_nesting",
                    "severity": "warning", 
                    "line": node.start_point[0] + 1,
                    "message": "嵌套层次过深，影响代码可读性"
                })
            
            for child in node.children:
                traverse(child)
        
        traverse(node)
        return issues
    
    def _calculate_nesting_depth(self, node) -> int:
        """计算节点的嵌套深度"""
        if not node.children:
            return 0
        
        max_child_depth = 0
        for child in node.children:
            if child.type in ['compound_statement', 'if_statement', 'while_statement', 'for_statement']:
                child_depth = self._calculate_nesting_depth(child)
                max_child_depth = max(max_child_depth, child_depth)
        
        if node.type in ['compound_statement', 'if_statement', 'while_statement', 'for_statement']:
            return max_child_depth + 1
        else:
            return max_child_depth
    
    def _extract_parameters(self, node, code_content: str) -> List[str]:
        """提取函数参数"""
        # 简化实现，实际需要更复杂的解析
        return []
    
    def _extract_return_type(self, node, code_content: str) -> str:
        """提取函数返回类型"""
        # 简化实现，实际需要更复杂的解析
        return "unknown"
    
    def _extract_class_methods(self, node, code_content: str) -> List[str]:
        """提取类方法"""
        # 简化实现，实际需要更复杂的解析
        return []
    
    def _extract_class_members(self, node, code_content: str) -> List[str]:
        """提取类成员变量"""
        # 简化实现，实际需要更复杂的解析
        return []
    
    def generate_analysis_report(self, analysis_result: Dict[str, Any]) -> str:
        """生成分析报告"""
        
        if "error" in analysis_result:
            return f"分析失败: {analysis_result['error']}"
        
        report = f"""
## 代码分析报告 - {analysis_result['file_path']}

### 基本信息
- 文件大小: {analysis_result['file_size']} 字节
- 代码行数: {analysis_result['line_count']} 行
- 函数数量: {len(analysis_result['functions'])}
- 类数量: {len(analysis_result['classes'])}

### 复杂度指标
- 圈复杂度: {analysis_result['complexity_metrics']['cyclomatic_complexity']}
- 最大嵌套深度: {analysis_result['complexity_metrics']['nesting_depth']}

### 包含的头文件
{chr(10).join(f"- {inc}" for inc in analysis_result['includes'])}

### 函数列表
{chr(10).join(f"- {func['name']} (第{func['start_line']}-{func['end_line']}行)" for func in analysis_result['functions'])}

### 潜在问题
{chr(10).join(f"- 第{issue['line']}行: {issue['message']} ({issue['severity']})" for issue in analysis_result['potential_issues'])}

### 建议
1. 保持函数长度适中（建议不超过50行）
2. 减少嵌套层次（建议不超过4层）
3. 添加适当的注释和文档
4. 考虑重构复杂的函数
        """
        
        return report
