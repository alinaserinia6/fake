#!/usr/bin/env python3
"""
Interruptr 多智能体演示脚本
用实际的C++缺陷代码测试智能体分析能力
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from agents.enhanced_multi_agent_system import EnhancedMultiAgentSystem
from config.env_config import config

class DemoRunner:
    """演示运行器"""
    
    def __init__(self):
        self.test_files = [
            {
                "name": "buffer_overflow.cpp",
                "description": "缓冲区溢出漏洞示例",
                "focus": "安全漏洞检测"
            },
            {
                "name": "memory_leaks.cpp", 
                "description": "内存管理问题示例",
                "focus": "内存安全分析"
            },
            {
                "name": "race_conditions.cpp",
                "description": "并发竞态条件示例",
                "focus": "线程安全分析"
            },
            {
                "name": "architecture_issues.cpp",
                "description": "架构设计问题示例",
                "focus": "架构质量评估"
            }
        ]
        
        self.results = {}
    
    def display_banner(self):
        """显示演示横幅"""
        print("🎭" + "="*70 + "🎭")
        print("🚀 Interruptr 多智能体C++代码分析演示")
        print("💡 7个专业智能体协作分析C++代码缺陷")
        print("🤖 使用OpenAI + Claude + Gemini + Ollama")
        print("="*72)
        
    def display_test_files(self):
        """显示测试文件信息"""
        print("\n📁 测试文件概览:")
        print("-" * 50)
        
        for i, file_info in enumerate(self.test_files, 1):
            file_path = project_root / "examples" / file_info["name"]
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                lines = len(content.splitlines())
                chars = len(content)
                
                print(f"{i}. {file_info['name']}")
                print(f"   📄 {file_info['description']}")
                print(f"   🎯 分析重点: {file_info['focus']}")
                print(f"   📊 代码统计: {lines}行, {chars}字符")
                print()
            else:
                print(f"❌ {file_info['name']} 文件不存在")
    
    def check_llm_availability(self):
        """检查LLM可用性"""
        print("🔍 检查LLM提供商配置:")
        print("-" * 40)
        
        providers = [
            ("OpenAI", config.openai_api_key, "协调者 + 调试专家"),
            ("Claude", config.anthropic_api_key, "代码分析师 + 安全专家 + 架构师"),
            ("Gemini", config.gemini_api_key, "质疑者"),
            ("Ollama", config.ollama_base_url, "检查者")
        ]
        
        available_count = 0
        for name, key_or_url, roles in providers:
            if key_or_url and key_or_url != f"your-{name.lower()}-api-key":
                print(f"✅ {name}: 已配置 ({roles})")
                available_count += 1
            else:
                print(f"❌ {name}: 未配置")
        
        print(f"\n📊 LLM可用性: {available_count}/4 个提供商已配置")
        
        if available_count == 0:
            print("⚠️ 警告: 没有配置任何LLM提供商，将使用模拟响应")
            return False
        elif available_count < 4:
            print("⚠️ 提示: 部分LLM未配置，可能影响分析质量")
        else:
            print("🎉 所有LLM提供商已配置，准备开始分析")
        
        return available_count > 0
    
    async def analyze_single_file(self, file_info, use_real_llm=False):
        """分析单个文件"""
        file_path = project_root / "examples" / file_info["name"]
        
        print(f"\n🔬 开始分析: {file_info['name']}")
        print(f"🎯 分析重点: {file_info['focus']}")
        print("=" * 60)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            if use_real_llm:
                # 使用真实的多智能体系统
                system = EnhancedMultiAgentSystem()
                result = await system.analyze_code_file(str(file_path), code_content)
                return result
            else:
                # 使用模拟分析结果
                return self.generate_mock_analysis(file_info, code_content)
                
        except Exception as e:
            print(f"❌ 分析失败: {str(e)}")
            return None
    
    def generate_mock_analysis(self, file_info, code_content):
        """生成模拟分析结果"""
        print("🤖 模拟多智能体分析过程...")
        
        # 模拟分析过程
        agents = [
            "🎯 协调者",
            "📊 代码分析师", 
            "🔒 安全专家",
            "🐛 调试专家",
            "🏛️ 架构师",
            "🤔 质疑者",
            "✅ 检查者"
        ]
        
        for i, agent in enumerate(agents, 1):
            print(f"  [{i}/7] {agent} 正在分析...")
        
        # 根据文件类型生成特定的分析结果
        if "buffer_overflow" in file_info["name"]:
            return self.generate_buffer_overflow_analysis()
        elif "memory_leaks" in file_info["name"]:
            return self.generate_memory_analysis()
        elif "race_conditions" in file_info["name"]:
            return self.generate_concurrency_analysis()
        elif "architecture" in file_info["name"]:
            return self.generate_architecture_analysis()
        else:
            return self.generate_generic_analysis()
    
    def generate_buffer_overflow_analysis(self):
        """生成缓冲区溢出分析结果"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 3.2,
                    "issues": [
                        "使用了已弃用的危险函数gets()",
                        "strcpy()函数没有边界检查",
                        "scanf()使用不当可能导致缓冲区溢出",
                        "缺少输入验证和边界检查"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "缓冲区溢出",
                            "line": 18,
                            "function": "setCredentials",
                            "description": "strcpy()函数可能导致缓冲区溢出",
                            "severity": "高危",
                            "cwe": "CWE-120"
                        },
                        {
                            "type": "已弃用函数",
                            "line": 31,
                            "function": "authenticate", 
                            "description": "gets()函数已被弃用，存在严重安全风险",
                            "severity": "严重",
                            "cwe": "CWE-242"
                        }
                    ],
                    "recommendations": [
                        "使用strncpy()或strlcpy()替代strcpy()",
                        "使用fgets()替代gets()",
                        "添加输入长度验证",
                        "使用安全的字符串处理函数"
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "第18行: 检查strcpy()前的参数长度",
                        "第31行: 监控gets()函数调用",
                        "第47行: 验证输入缓冲区大小",
                        "第55行: 检查scanf()输入长度"
                    ]
                },
                "architecture": {
                    "issues": [
                        "UserManager类职责过多",
                        "缺少输入验证层",
                        "硬编码的缓冲区大小",
                        "错误处理机制不完善"
                    ]
                },
                "critic_review": "安全专家的分析基本准确，但还需要考虑格式字符串攻击的可能性。第24行的printf()使用用户输入作为格式字符串，这也是一个严重的安全漏洞。",
                "final_review": "经过验证，代码确实存在多个严重的缓冲区溢出风险。建议立即修复这些问题，并实施代码安全审查流程。"
            }
        }
    
    def generate_memory_analysis(self):
        """生成内存管理分析结果"""
        return {
            "status": "completed", 
            "analysis_results": {
                "code_quality": {
                    "score": 4.1,
                    "issues": [
                        "存在内存泄漏风险",
                        "野指针访问问题",
                        "重复释放内存",
                        "缺少RAII模式使用"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "内存泄漏",
                            "line": 32,
                            "function": "processData",
                            "description": "backup指针重复分配但未释放旧内存",
                            "severity": "中危"
                        },
                        {
                            "type": "野指针访问",
                            "line": 44,
                            "function": "dangerousOperation",
                            "description": "使用已释放的内存指针",
                            "severity": "高危"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "第32行: 检查backup指针分配前是否已释放",
                        "第44行: 验证data指针状态",
                        "第150行: 监控ResourceManager析构",
                        "第156行: 检查异常抛出时的内存状态"
                    ]
                },
                "architecture": {
                    "recommendations": [
                        "使用智能指针(std::unique_ptr, std::shared_ptr)",
                        "实施RAII模式",
                        "添加异常安全保证",
                        "使用容器类替代原始数组"
                    ]
                },
                "critic_review": "内存管理分析较为全面，但应该强调使用现代C++特性的重要性。建议使用std::vector替代原始数组，使用智能指针管理动态内存。",
                "final_review": "代码存在多个内存管理问题，需要重构以使用现代C++内存管理技术。"
            }
        }
    
    def generate_concurrency_analysis(self):
        """生成并发分析结果"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 3.8,
                    "issues": [
                        "存在竞态条件",
                        "锁的使用不一致",
                        "可能的死锁风险",
                        "非原子操作的并发访问"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "竞态条件",
                            "line": 18,
                            "function": "BankAccount构造函数",
                            "description": "静态变量accountCounter的非线程安全访问",
                            "severity": "中危"
                        },
                        {
                            "type": "死锁风险",
                            "line": 57,
                            "function": "transferTo",
                            "description": "多个mutex的锁定顺序可能导致死锁",
                            "severity": "高危"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "第18行: 监控accountCounter的并发访问",
                        "第26行: 检查deposit函数的锁状态", 
                        "第57-58行: 监控transferTo中的锁获取顺序",
                        "第98行: 观察ThreadUnsafeCounter的竞态条件"
                    ]
                },
                "architecture": {
                    "recommendations": [
                        "使用std::atomic替代volatile变量",
                        "实施统一的锁定策略",
                        "考虑使用无锁数据结构",
                        "添加线程安全的日志记录"
                    ]
                },
                "critic_review": "并发分析准确识别了主要问题。还应该考虑使用std::lock()函数来避免死锁，以及使用条件变量来改善线程同步。",
                "final_review": "代码存在严重的线程安全问题，需要重新设计并发策略和同步机制。"
            }
        }
    
    def generate_architecture_analysis(self):
        """生成架构分析结果"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 2.5,
                    "issues": [
                        "违反单一职责原则",
                        "类的耦合度过高",
                        "方法过于复杂",
                        "参数列表过长"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "封装破坏",
                            "line": 142,
                            "function": "getDataReference",
                            "description": "返回内部数据引用，破坏封装",
                            "severity": "中危"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "第25行: 监控MegaClass构造函数的复杂初始化",
                        "第85行: 检查generateComplexReport的嵌套逻辑",
                        "第154行: 观察updateData的参数处理",
                        "第200行: 监控SpecialProcessor的异常抛出"
                    ]
                },
                "architecture": {
                    "violations": [
                        "单一职责原则: MegaClass承担了太多职责",
                        "开闭原则: 类设计不易扩展",
                        "里式替换原则: SpecialProcessor违反基类契约",
                        "接口隔离原则: 接口过于庞大",
                        "依赖倒置原则: 直接依赖具体类而非抽象"
                    ],
                    "recommendations": [
                        "将MegaClass拆分为多个职责明确的类",
                        "使用工厂模式创建对象",
                        "引入接口抽象层",
                        "减少方法参数，使用配置对象",
                        "实施依赖注入模式"
                    ]
                },
                "critic_review": "架构分析很全面，正确识别了SOLID原则的违反。建议还应该考虑使用Command模式来处理复杂的操作，以及Strategy模式来处理不同的处理策略。",
                "final_review": "代码存在严重的架构设计问题，需要进行大规模重构以改善可维护性和可扩展性。"
            }
        }
    
    def generate_generic_analysis(self):
        """生成通用分析结果"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {"score": 6.0, "issues": []},
                "security": {"critical_issues": []},
                "debug": {"breakpoints": []},
                "architecture": {"recommendations": []},
                "critic_review": "代码质量可接受。",
                "final_review": "未发现严重问题。"
            }
        }
    
    def display_analysis_summary(self, file_info, result):
        """显示分析摘要"""
        if not result:
            print("❌ 分析失败")
            return
        
        analysis = result.get("analysis_results", {})
        
        print(f"\n📊 {file_info['name']} 分析摘要:")
        print("-" * 50)
        
        # 代码质量
        quality = analysis.get("code_quality", {})
        if isinstance(quality, dict):
            score = quality.get("score", 0)
            print(f"🎯 代码质量评分: {score}/10.0")
        else:
            print(f"🎯 代码质量: {str(quality)[:50]}...")
        
        # 安全问题
        security = analysis.get("security", {})
        if isinstance(security, dict):
            issues = security.get("critical_issues", [])
            print(f"🔒 安全问题: {len(issues)}个")
            
            if issues:
                for issue in issues[:3]:  # 显示前3个问题
                    if isinstance(issue, dict):
                        print(f"   • {issue.get('type', 'Unknown')} (第{issue.get('line', '?')}行)")
                    else:
                        print(f"   • {str(issue)[:50]}...")
        else:
            print(f"🔒 安全分析: {str(security)[:50]}...")
        
        # 质疑者意见
        critic = analysis.get("critic_review", "")
        if critic:
            print(f"🤔 质疑者: {str(critic)[:100]}...")
        
        # 最终评估
        final = analysis.get("final_review", "")
        if final:
            print(f"✅ 最终评估: {str(final)[:100]}...")
        
        print()
    
    def save_results(self):
        """保存演示结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = project_root / f"demo_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 演示结果已保存: {output_file}")
    
    async def run_demo(self):
        """运行完整演示"""
        self.display_banner()
        self.display_test_files()
        
        use_real_llm = self.check_llm_availability()
        
        print(f"\n🚀 开始多智能体分析演示 ({'真实LLM' if use_real_llm else '模拟模式'})")
        print("=" * 72)
        
        for i, file_info in enumerate(self.test_files, 1):
            print(f"\n[{i}/4] 分析文件: {file_info['name']}")
            
            result = await self.analyze_single_file(file_info, use_real_llm)
            
            if result:
                self.results[file_info["name"]] = result
                self.display_analysis_summary(file_info, result)
            
            # 添加间隔
            if i < len(self.test_files):
                print("⏳ 准备下一个分析...")
                await asyncio.sleep(1)
        
        print("\n🎉 所有文件分析完成!")
        self.save_results()
        
        # 显示总结
        print("\n📈 演示总结:")
        print("-" * 30)
        total_files = len(self.test_files)
        analyzed_files = len(self.results)
        print(f"• 总文件数: {total_files}")
        print(f"• 成功分析: {analyzed_files}")
        print(f"• 成功率: {analyzed_files/total_files*100:.1f}%")
        
        if use_real_llm:
            print("• 使用了真实的LLM API进行分析")
        else:
            print("• 使用模拟模式进行演示")
        
        print(f"\n💡 建议:")
        if not use_real_llm:
            print("• 配置真实的API密钥以获得更准确的分析结果")
        print("• 可以通过 'python start.py' 启动Web界面进行交互式分析")
        print("• 查看生成的报告文件了解详细分析结果")

async def main():
    """主函数"""
    demo = DemoRunner()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
