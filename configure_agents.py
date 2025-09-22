#!/usr/bin/env python3
"""
AutoGen Studio 智能体配置导入工具
用于快速创建和配置多智能体团队
"""

import json
import requests
from pathlib import Path

class AutoGenStudioConfigurator:
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def load_agent_configs(self, config_file="agent_configs.json"):
        """加载智能体配置文件"""
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"❌ 配置文件 {config_file} 不存在")
            return None
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_studio_status(self):
        """检查AutoGen Studio是否运行"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ AutoGen Studio 正在运行")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("❌ AutoGen Studio 未运行或无法访问")
        return False
    
    def print_manual_configuration_guide(self, config):
        """打印手动配置指南"""
        print("\n" + "="*60)
        print("📋 AutoGen Studio 手动配置指南")
        print("="*60)
        
        print("\n🎯 团队信息:")
        print(f"   名称: {config['team_name']}")
        print(f"   描述: {config['team_description']}")
        
        print(f"\n🤖 智能体配置 ({len(config['agents'])} 个):")
        print("-" * 40)
        
        for i, agent in enumerate(config['agents'], 1):
            print(f"\n{i}. 【{agent['name']}】- {agent['role']}")
            print(f"   📝 描述: {agent['description']}")
            print(f"   🧠 模型: {agent['model']}")
            print(f"   🌡️  温度: {agent['temperature']}")
            print(f"   📊 最大tokens: {agent['max_tokens']}")
            print(f"   🛠️  技能: {', '.join(agent['skills'])}")
            
            # 系统提示词（截断显示）
            system_msg = agent['system_message'][:200] + "..." if len(agent['system_message']) > 200 else agent['system_message']
            print(f"   💬 系统提示: {system_msg}")
        
        print("\n🔄 工作流程:")
        print("-" * 30)
        for step_info in config['workflow']['conversation_flow']:
            step_num = step_info['step']
            action = step_info['action']
            
            if 'agents' in step_info:
                agents = ', '.join(step_info['agents'])
                mode = step_info.get('mode', 'sequential')
                print(f"   步骤 {step_num}: {agents} ({mode}) - {action}")
            else:
                agent = step_info['agent']
                print(f"   步骤 {step_num}: {agent} - {action}")
        
        print("\n⚙️ 全局设置:")
        settings = config['settings']
        print(f"   🧠 默认模型: {settings['default_model']}")
        print(f"   🌡️  默认温度: {settings['temperature']}")
        print(f"   📊 默认tokens: {settings['max_tokens']}")
        print(f"   🎲 随机种子: {settings['seed']}")
        print(f"   ⏱️  超时时间: {settings['timeout']}秒")
        
        print("\n📋 手动配置步骤:")
        print("1. 打开浏览器访问: http://localhost:8081")
        print("2. 点击 'Teams' 或 'Team Builder' 选项卡")
        print("3. 点击 'Create New Team' 或 '+'")
        print("4. 输入团队名称和描述")
        print("5. 为每个智能体创建Agent:")
        print("   - 点击 'Add Agent'")
        print("   - 填入上述配置信息")
        print("   - 复制粘贴对应的系统提示词")
        print("6. 配置工作流程和消息传递逻辑")
        print("7. 保存团队配置")
        print("8. 在Playground中测试团队")
        
        print("\n🧪 测试建议:")
        print("使用 sample_code.cpp 中的代码进行测试")
        print("观察agent之间的消息传递和协作过程")
        
    def export_agent_prompts(self, config):
        """导出每个智能体的提示词到单独文件"""
        prompts_dir = Path("agent_prompts")
        prompts_dir.mkdir(exist_ok=True)
        
        print(f"\n📁 导出智能体提示词到 {prompts_dir}/")
        print("-" * 40)
        
        for agent in config['agents']:
            filename = f"{agent['name'].lower()}_prompt.txt"
            filepath = prompts_dir / filename
            
            content = f"""# {agent['name']} ({agent['role']})

## 描述
{agent['description']}

## 技能
{', '.join(agent['skills'])}

## 配置
- 模型: {agent['model']}
- 温度: {agent['temperature']}
- 最大tokens: {agent['max_tokens']}

## 系统提示词
{agent['system_message']}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename}")
        
        print("\n💡 使用方法:")
        print("在AutoGen Studio中创建Agent时，直接复制粘贴对应文件中的系统提示词")

def main():
    print("🚀 AutoGen Studio 智能体配置工具")
    print("=" * 50)
    
    configurator = AutoGenStudioConfigurator()
    
    # 检查AutoGen Studio状态
    if not configurator.check_studio_status():
        print("\n⚠️  请先启动AutoGen Studio:")
        print("cd /home/coder-gw/Interruptr")
        print("nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &")
        return
    
    # 加载配置
    config = configurator.load_agent_configs()
    if not config:
        return
    
    print("\n✅ 成功加载配置文件")
    print(f"   团队: {config['team_name']}")
    print(f"   智能体数量: {len(config['agents'])}")
    
    # 导出提示词文件
    configurator.export_agent_prompts(config)
    
    # 打印配置指南
    configurator.print_manual_configuration_guide(config)
    
    print("\n" + "="*60)
    print("🎯 配置完成！请按照上述指南在AutoGen Studio中手动配置")
    print("="*60)

if __name__ == "__main__":
    main()
