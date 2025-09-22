#!/usr/bin/env python3
"""
简化的多智能体代码分析演示
展示 AutoGen 智能体间的对话
"""

import os
import asyncio
from pathlib import Path

async def simulate_multi_agent_analysis():
    """模拟多智能体分析过程"""
    print("🤖 启动多智能体代码分析系统...")
    print("📝 模拟智能体协作流程\\n")
    
    # 读取示例代码
    examples_dir = Path("/home/coder-gw/Interruptr/examples")
    cpp_files = list(examples_dir.glob("*.cpp"))
    
    if not cpp_files:
        print("❌ 未找到示例代码文件")
        return
    
    # 分析第一个文件
    cpp_file = cpp_files[0]
    with open(cpp_file, 'r', encoding='utf-8') as f:
        code_content = f.read()
    
    print(f"\\n{'='*60}")
    print(f"分析文件: {cpp_file.name}")
    print(f"{'='*60}")
    print(f"代码内容:")
    print("-" * 40)
    print(code_content)
    print("-" * 40)
    
    # 模拟智能体对话
    agents_dialogue = [
        {
            "agent": "coordinator",
            "message": f"收到代码分析任务：{cpp_file.name}。让我协调各个专家进行分析。首先请代码分析专家进行静态分析。"
        },
        {
            "agent": "code_analyst", 
            "message": """我是代码分析专家。分析结果如下：

1. **结构问题**：
   - 缺少必要的头文件包含
   - 函数参数类型不安全
   - 没有输入验证

2. **逻辑问题**：
   - 可能存在缓冲区边界检查不足
   - 错误处理机制缺失

请安全专家进一步检查安全漏洞。"""
        },
        {
            "agent": "security_expert",
            "message": """我是安全专家。发现以下安全风险：

🚨 **高风险漏洞**：
1. **缓冲区溢出**：strcpy/gets等函数可能导致栈溢出
2. **输入验证缺失**：用户输入未经验证直接使用
3. **内存安全**：指针操作未检查空值

🔧 **修复建议**：
- 使用安全的字符串函数（strncpy, fgets）
- 添加边界检查
- 验证所有输入参数

请调试专家分析运行时问题。"""
        },
        {
            "agent": "debug_expert",
            "message": """我是调试专家。运行时分析如下：

🐛 **潜在运行时错误**：
1. **段错误风险**：未初始化指针访问
2. **内存泄漏**：动态分配的内存未释放
3. **异常处理**：缺少异常捕获机制

🔧 **调试建议**：
- 添加空指针检查
- 使用 RAII 模式管理资源
- 添加异常处理代码

请评审专家进行最终评审。"""
        },
        {
            "agent": "critic",
            "message": """我是评审专家。综合评审结果：

✅ **分析质量评估**：
- 代码分析专家：发现了基础结构问题 ✓
- 安全专家：识别了关键安全漏洞 ✓  
- 调试专家：定位了运行时风险 ✓

📋 **遗漏问题补充**：
1. 性能优化建议
2. 代码可维护性评估
3. 单元测试建议

🎯 **最终评分**：7/10 分
建议优先修复安全漏洞，然后改进代码结构。"""
        },
        {
            "agent": "coordinator",
            "message": """感谢各位专家的分析！我来整合最终建议：

🎯 **修复优先级**：
1. **紧急**：修复缓冲区溢出漏洞
2. **重要**：添加输入验证和错误处理
3. **建议**：改进代码结构和性能

📝 **具体修复步骤**：
```cpp
// 1. 安全的字符串操作
char buffer[100];
strncpy(buffer, input, sizeof(buffer)-1);
buffer[sizeof(buffer)-1] = '\\0';

// 2. 输入验证
if (input == NULL || strlen(input) == 0) {
    return -1;
}

// 3. 错误处理
try {
    // 代码逻辑
} catch (const std::exception& e) {
    std::cerr << "错误: " << e.what() << std::endl;
    return -1;
}
```

分析完成！各智能体协作成功。"""
        }
    ]
    
    # 播放对话
    for i, dialogue in enumerate(agents_dialogue):
        agent = dialogue["agent"]
        message = dialogue["message"]
        
        print(f"\\n🤖 **{agent.upper()}** 说：")
        print("-" * 50)
        print(message)
        
        # 模拟思考时间
        await asyncio.sleep(1)
    
    print(f"\\n{'='*60}")
    print("✅ 多智能体分析完成！")
    print("🌐 AutoGen Studio 正在运行在: http://localhost:8081")
    print("📱 您可以在浏览器中查看完整的对话界面")
    print(f"{'='*60}")

def check_autogen_studio_status():
    """检查 AutoGen Studio 状态"""
    try:
        import requests
        response = requests.get("http://localhost:8081", timeout=5)
        return response.status_code == 200
    except:
        return False

async def main():
    """主函数"""
    print("🔍 检查 AutoGen Studio 状态...")
    
    if check_autogen_studio_status():
        print("✅ AutoGen Studio 正在运行")
    else:
        print("⚠️ AutoGen Studio 可能未完全启动，请稍等...")
    
    # 运行演示
    await simulate_multi_agent_analysis()

if __name__ == "__main__":
    asyncio.run(main())
