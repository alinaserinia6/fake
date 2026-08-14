#!/usr/bin/env python3
"""
AutoGen Studio Agent Configuration Import Tool
Used to quickly create and configure multi-agent teams
"""

import json
import requests
from pathlib import Path

class AutoGenStudioConfigurator:
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def load_agent_configs(self, config_file="agent_configs.json"):
        """Load agent configuration file"""
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"❌ Configuration file {config_file} does not exist")
            return None
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_studio_status(self):
        """Check if AutoGen Studio is running"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ AutoGen Studio is running")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("❌ AutoGen Studio is not running or unreachable")
        return False
    
    def print_manual_configuration_guide(self, config):
        """Print manual configuration guide"""
        print("\n" + "="*60)
        print("📋 AutoGen Studio Manual Configuration Guide")
        print("="*60)
        
        print("\n🎯 Team Information:")
        print(f"   Name: {config['team_name']}")
        print(f"   Description: {config['team_description']}")
        
        print(f"\n🤖 Agent Configuration ({len(config['agents'])} agents):")
        print("-" * 40)
        
        for i, agent in enumerate(config['agents'], 1):
            print(f"\n{i}. 【{agent['name']}】- {agent['role']}")
            print(f"   📝 Description: {agent['description']}")
            print(f"   🧠 Model: {agent['model']}")
            print(f"   🌡️  Temperature: {agent['temperature']}")
            print(f"   📊 Max tokens: {agent['max_tokens']}")
            print(f"   🛠️  Skills: {', '.join(agent['skills'])}")
            
            # Truncate system message for display
            system_msg = agent['system_message'][:200] + "..." if len(agent['system_message']) > 200 else agent['system_message']
            print(f"   💬 System prompt: {system_msg}")
        
        print("\n🔄 Workflow:")
        print("-" * 30)
        for step_info in config['workflow']['conversation_flow']:
            step_num = step_info['step']
            action = step_info['action']
            
            if 'agents' in step_info:
                agents = ', '.join(step_info['agents'])
                mode = step_info.get('mode', 'sequential')
                print(f"   Step {step_num}: {agents} ({mode}) - {action}")
            else:
                agent = step_info['agent']
                print(f"   Step {step_num}: {agent} - {action}")
        
        print("\n⚙️ Global Settings:")
        settings = config['settings']
        print(f"   🧠 Default model: {settings['default_model']}")
        print(f"   🌡️  Default temperature: {settings['temperature']}")
        print(f"   📊 Default tokens: {settings['max_tokens']}")
        print(f"   🎲 Random seed: {settings['seed']}")
        print(f"   ⏱️  Timeout: {settings['timeout']} seconds")
        
        print("\n📋 Manual Configuration Steps:")
        print("1. Open your browser and go to: http://localhost:8081")
        print("2. Click on the 'Teams' or 'Team Builder' tab")
        print("3. Click 'Create New Team' or '+'")
        print("4. Enter the team name and description")
        print("5. Create an Agent for each of the following roles:")
        print("   - Click 'Add Agent'")
        print("   - Fill in the configuration details shown above")
        print("   - Copy and paste the corresponding system prompt")
        print("6. Configure the workflow and message routing logic")
        print("7. Save the team configuration")
        print("8. Test the team in the Playground")
        
        print("\n🧪 Testing Recommendations:")
        print("Use the code from sample_code.cpp for testing")
        print("Observe the message passing and collaboration between agents")
        
    def export_agent_prompts(self, config):
        """Export each agent's prompt to a separate file"""
        prompts_dir = Path("agent_prompts")
        prompts_dir.mkdir(exist_ok=True)
        
        print(f"\n📁 Exporting agent prompts to {prompts_dir}/")
        print("-" * 40)
        
        for agent in config['agents']:
            filename = f"{agent['name'].lower()}_prompt.txt"
            filepath = prompts_dir / filename
            
            content = f"""# {agent['name']} ({agent['role']})

            ## Description
            {agent['description']}

            ## Skills
            {', '.join(agent['skills'])}

            ## Configuration
            - Model: {agent['model']}
            - Temperature: {agent['temperature']}
            - Max tokens: {agent['max_tokens']}

            ## System Prompt
            {agent['system_message']}
            """
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename}")
        
        print("\n💡 Usage Instructions:")
        print("When creating an Agent in AutoGen Studio, simply copy and paste the system prompt from the corresponding file.")

def main():
    print("🚀 AutoGen Studio Agent Configuration Tool")
    print("=" * 50)
    
    configurator = AutoGenStudioConfigurator()
    
    # Check AutoGen Studio status
    if not configurator.check_studio_status():
        print("\n⚠️  Please start AutoGen Studio first:")
        print("cd /home/coder-gw/Interruptr")
        print("nohup autogenstudio ui --port 8081 --host 0.0.0.0 > autogen_studio.log 2>&1 &")
        return
    
    # Load configuration
    config = configurator.load_agent_configs()
    if not config:
        return
    
    print("\n✅ Successfully loaded configuration file")
    print(f"   Team: {config['team_name']}")
    print(f"   Number of agents: {len(config['agents'])}")
    
    # Export prompt files
    configurator.export_agent_prompts(config)
    
    # Print configuration guide
    configurator.print_manual_configuration_guide(config)
    
    print("\n" + "="*60)
    print("🎯 Configuration complete! Please follow the guide above to manually configure in AutoGen Studio")
    print("="*60)

if __name__ == "__main__":
    main()
