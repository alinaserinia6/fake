# 🎯 AutoGen Studio Configuration Methods Summary

## Answering Your Question: Is there a way to upload files to assign roles?

### ✅ Yes! We offer multiple methods:

## 🔧 Method 1: Configuration File Approach (Recommended)

### Files we have prepared for you:
1. **`agent_configs.json`** – Complete team configuration file
   - Contains detailed configurations for all 5 agents
   - Workflow definitions
   - Model parameter settings

2. **`agent_prompts/` directory** – Prompt files for each agent
   - `coordinator_prompt.txt` – Coordinator
   - `code_analyst_prompt.txt` – Code Analyst
   - `security_expert_prompt.txt` – Security Expert
   - `debug_expert_prompt.txt` – Debug Expert
   - `quality_critic_prompt.txt` – Quality Critic

3. **`configure_agents.py`** – Automatic configuration tool
   - Checks AutoGen Studio status
   - Exports agent configurations
   - Generates detailed configuration guides

### How to use:

```bash
# Run the configuration tool to generate all files
python configure_agents.py

# When creating a team in AutoGen Studio:
# 1. Refer to the configuration in agent_configs.json
# 2. Copy and paste the contents of the corresponding prompt files
```

## 🖱️ Method 2: Visual Drag‑and‑Drop Approach

### Built‑in AutoGen Studio features:

1. **Team Builder** – Drag‑and‑drop team builder
   - Drag to create agent nodes
   - Visually connect message‑routing paths
   - Real‑time workflow diagram preview

2. **Agent Configuration** – Agent configuration interface
   - Graphically configure each agent
   - Drag to adjust execution order
   - Set parallel / serial modes

3. **Workflow Designer** – Workflow designer
   - Drag to set up message‑routing relationships
   - Visually edit decision branches
   - Configure termination conditions

## 🚀 Recommended Configuration Workflow

### Step 1: Get started quickly with configuration files

```bash
cd /home/coder-gw/Interruptr
python configure_agents.py
```

### Step 2: Configure in AutoGen Studio

1. Visit <http://localhost:8081>
2. Go to Team Builder
3. Create a new team: "C/C++ Code Analysis Team"
4. Add the 5 agents according to the generated configuration file
5. Copy and paste the contents of the corresponding prompt files

### Step 3: Adjust the workflow

1. Drag to connect agent nodes
2. Set up the message‑routing path:

   ```txt
   User → Coordinator → [Parallel: Code_Analyst, Security_Expert, Debug_Expert] → Coordinator → Quality_Critic → User
   ```

3. Configure execution modes and termination conditions

### Step 4: Test and optimise

1. Test using `sample_code.cpp`
2. Observe the message passing between agents
3. Adjust parameters based on the results

## 📁 File Structure Overview

```txt
/home/coder-gw/Interruptr/
├── agent_configs.json              # 🔧 Team configuration file
├── configure_agents.py             # 🛠️ Configuration tool
├── agent_prompts/                  # 📂 Prompts directory
│   ├── coordinator_prompt.txt      # Coordinator configuration
│   ├── code_analyst_prompt.txt     # Code Analyst configuration
│   ├── security_expert_prompt.txt  # Security Expert configuration
│   ├── debug_expert_prompt.txt     # Debug Expert configuration
│   └── quality_critic_prompt.txt   # Quality Critic configuration
├── sample_code.cpp                 # 🧪 Test code
├── autogen_workflow_guide.md       # 📖 Detailed guide
└── setup_check.sh                  # ✅ Status check
```

## 🎯 Key Advantages

### Configuration‑file approach:

- ✅ **Quick deployment** – Generate all configurations with one click
- ✅ **Standardisation** – Ensures configuration consistency
- ✅ **Reusable** – Save and share configurations
- ✅ **Version control** – Track configuration changes

### Drag‑and‑drop approach:

- ✅ **Intuitive and easy** – Visual operation interface
- ✅ **Real‑time preview** – Instantly see workflow results
- ✅ **Flexible adjustments** – Modify connection relationships at any time
- ✅ **Interactive** – WYSIWYG configuration experience

## 🚀 Get Started Now

**You don't need to manually drag and drop everything!** We have already prepared for you:

1. **Complete configuration files** – Use them directly or as a reference
2. **Detailed prompts** – Copy and paste them straight in
3. **Automation tools** – Generate all required files with one click
4. **Configuration guide** – Step‑by‑step instructions with illustrations

Visit <http://localhost:8081> now and use the configuration files we've prepared to quickly create your multi‑agent team! 🎯
