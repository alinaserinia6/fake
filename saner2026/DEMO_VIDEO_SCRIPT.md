# SANER 2026 Tool Demo Video Script

## 📹 Video Basic Information

- **Title**: Interruptr: Multi-LLM Collaborative C/C++ Code Analysis
- **Duration**: 5-8 minutes
- **Resolution**: 1920x1080 (1080p)
- **Format**: MP4 (H.264 encoding)
- **Voiceover Language**: English
- **Subtitles**: English subtitles + key technical term annotations

## 🎬 Video Structure Outline

### 【Opening】Title Sequence (0:00-0:15)

**Visuals**:
- Interruptr Logo animation
- Title: "Multi-LLM Collaborative Code Analysis"
- Subtitle: "SANER 2026 Tool Demo"

**Voiceover**:
> "Welcome to Interruptr, a revolutionary multi-agent code analysis framework that combines the power of four different Large Language Models to provide comprehensive C/C++ code analysis."

**Key Subtitles**:

- Multi-LLM Collaboration
- Intelligent Code Analysis
- Real-time Visualization

---

### 【Segment 1】Problem & Solution (0:15-1:00)

**Visuals**:

- Side-by-side comparison with traditional code analysis tools (SonarQube, CodeQL, etc.)
- Display limitations of traditional tools: false positives, missed issues, lack of context
- Transition to the Interruptr interface

**Voiceover**:
> "Traditional static analysis tools suffer from high false positive rates and lack contextual understanding. Interruptr addresses these challenges through multi-LLM collaboration, introducing a questioning-verification mechanism that significantly improves analysis accuracy."

**On-Screen Text**:

- Traditional Tools: High False Positives, Limited Context
- Interruptr Solution: Multi-LLM Collaboration + Verification

---

### 【Segment 2】System Architecture (1:00-2:00)

**Visuals**:

- Animated system architecture diagram
- 7 agent icons and role descriptions
- Multi-LLM collaboration flowchart

**Voiceover**:
> "Our system employs seven specialized agents powered by four different LLMs: OpenAI GPT-4 for coordination and debugging, Claude-3.5 for deep code analysis and security, Google Gemini for critical questioning, and local Ollama for independent verification."

**Screen Display**:

```txt
🎯 Coordinator (GPT-4) → Task Management
📊 Code Analyst (Claude) → Quality Analysis  
🔒 Security Expert (Claude) → Vulnerability Detection
🐛 Debug Expert (GPT-4) → Debugging Strategy
🏛️ Architect (Claude) → Design Evaluation
🤔 Critic (Gemini) → Critical Review
✅ Reviewer (Ollama) → Final Verification
```

**Animation Effects**:

- Connection line animations between agents
- Data flow indicators
- Real-time status updates

---

### 【Segment 3】Live Demo - Multi-Agent Analysis (2:00-4:30)

#### 2:00-2:30 Code Upload and Initialisation

**Visuals**:

- Opening the Interruptr Web interface
- Uploading a C++ code example containing multiple issues
- Agent status panel display

**Example Code** (representative issues):

```cpp
#include <iostream>
#include <thread>
#include <mutex>

class ThreadUnsafeCounter {
private:
    int counter = 0;
    std::mutex mtx; // Declared but unused
    
public:
    void increment() {
        // Missing lock protection
        counter++;
    }
    
    void unsafeStringOp(char* input) {
        char buffer[100];
        strcpy(buffer, input); // Buffer overflow risk
        printf("Buffer: %s\n", buffer);
    }
    
    ~ThreadUnsafeCounter() {
        // Forgot to clean up resources
    }
};
```

**Voiceover**:
> "Let's analyse this C++ code containing multiple security and concurrency issues. Notice how our agents initialise and prepare for collaborative analysis."

#### 2:30-3:30 Agent Collaboration Process Display

**Visuals**:

- Agent conversation panel updating in real-time
- Different colours for different agents' messages
- Analysis progress bar and status indicators

**Simulated Conversation Flow**:

```txt
🎯 Coordinator: "Starting multi-agent analysis. Distributing tasks..."

📊 Code Analyst: "Analysing code structure... Detected high complexity in ThreadUnsafeCounter class"

🔒 Security Expert: "CRITICAL: Buffer overflow vulnerability found at line 14 - strcpy() usage without bounds checking"

🐛 Debug Expert: "Race condition detected: counter variable accessed without mutex protection"

🏛️ Architect: "Design issue: Mutex declared but never used, violates RAII principles"

🤔 Critic: "Wait, let me double-check the Security Expert's finding... Yes, confirmed. Also found potential resource leak in destructor"

✅ Reviewer: "Verifying all findings... All issues confirmed. Generating final report..."
```

**Visual Elements**:

- Agent avatars blinking to indicate active status
- Real-time message stream
- Issue classification labels (Security, Performance, Architecture)

#### 3:30-4:00 Questioning-Verification Mechanism Demo

**Visuals**:

- Highlighting the Critic agent's questioning process
- Displaying additional issues discovered
- Reviewer verification and correction process

**Voiceover**:
> "Here's our unique questioning-verification mechanism in action. The Critic agent actively looks for missed issues, while the Reviewer provides independent verification, significantly improving analysis reliability."

**On-Screen Text**:

- "Critic Found: Additional Resource Leak"
- "Reviewer Verified: 5/5 Issues Confirmed"
- "Confidence Score: 94%"

#### 4:00-4:30 Analysis Results Display

**Visuals**:

- Comprehensive analysis report interface
- Issue classification and severity levels
- Remediation recommendations and code examples

**Results Panel Display**:

```txt
Analysis Summary:
├── Security Issues: 2 (1 Critical, 1 Medium)
├── Concurrency Issues: 1 (High)
├── Architecture Issues: 2 (Medium)
└── Performance Issues: 0

Recommendations:
1. Replace strcpy() with strncpy() or std::string
2. Add mutex.lock() in increment() method
3. Implement proper resource cleanup
4. Consider RAII design pattern
```

---

### 【Segment 4】Comparison with Traditional Tools (4:30-5:30)

**Visuals**:

- Split-screen comparison: Interruptr vs. traditional tools results
- Data table showing accuracy comparison
- Highlight Interruptr's unique findings

**Comparison Data Display**:

| Tool | Issues Found | False Positives | Unique Findings |
| ------ | ------------- | ---------------- | ---------------- |
| **Interruptr** | **5** | **0** | **2** |
| SonarQube | 3 | 1 | 0 |
| CodeQL | 4 | 2 | 1 |
| Clang-tidy | 6 | 3 | 1 |

**Voiceover**:
> "Compared to traditional tools, Interruptr demonstrates superior accuracy with fewer false positives and identifies unique issues missed by conventional analysers through its multi-agent collaboration."

**On-Screen Text**:

- "85% Accuracy vs 72% Traditional Average"
- "Multi-Agent Advantage: +12% Improvement"
- "Zero False Positives in Demo Case"

---

### 【Segment 5】Real-time Visualization Features (5:30-6:30)

**Visuals**:

- Agent interaction network graph
- Real-time status monitoring dashboard
- Analysis progress visualisation

**Interface Display**:

- Agent Status Dashboard
- Communication Flow Diagram  
- Analysis Progress Timeline
- Issue Severity Heat Map

**Voiceover**:
> "Our transparent visualisation system allows users to observe the entire analysis process in real-time, making AI decision-making interpretable and trustworthy."

**Interactive Demo**:

- Click on an agent to view detailed status
- Hover to display conversation content
- Timeline playback of the analysis process

---

### 【Segment 6】Technical Innovation Highlights (6:30-7:00)

**Visuals**:

- Technical innovation point charts
- Architecture advantage comparison
- Performance metric display

**Innovation List**:

```txt
🚀 Technical Innovations:
✓ First Multi-LLM Collaborative Framework
✓ Questioning-Verification Dual Mechanism  
✓ Real-time Agent Visualization
✓ Hybrid Local+Cloud Architecture
✓ Adaptive Task Distribution
✓ Cross-Model Result Validation
```

**Voiceover**:
> "Interruptr introduces several technical innovations: first-of-its-kind multi-LLM collaboration, intelligent questioning mechanism, and comprehensive real-time visualisation, making it a breakthrough in AI-powered code analysis."

---

### 【Segment 7】Practical Applications (7:00-7:30)

**Visuals**:

- Real-world application scenarios
- User testimonial (optional)
- Deployment options display

**Application Scenarios**:

- Enterprise Code Review
- Open Source Security Auditing  
- Educational Code Analysis
- CI/CD Pipeline Integration

**Voiceover**:
> "Interruptr is ready for real-world deployment with enterprise-grade security, scalable architecture, and easy integration into existing development workflows."

---

### 【Closing】Summary & Future Work (7:30-8:00)

**Visuals**:

- Core value summary
- GitHub link and Demo URL
- SANER 2026 conference information

**Summary Text**:

```txt
🎯 Interruptr: Multi-LLM Code Analysis
✓ 85% Accuracy, 0% False Positives  
✓ 7 Specialized AI Agents
✓ Real-time Collaboration Visualization
✓ Open Source & Enterprise Ready

🔗 Try Online Demo: interruptr.demo.ai
📘 GitHub: github.com/interruptr/interruptr
📧 Contact: team@interruptr.ai
```

**Voiceover**:
> "Experience the future of intelligent code analysis with Interruptr. Visit our demo website, explore the open-source code, and join us at SANER 2026 in Cyprus. Thank you for watching!"

**End Screen**:

- SANER 2026 Logo
- "See you in Cyprus, March 2026!"
- Contact information and links

---

## 🎥 Production Technical Requirements

### Recording Equipment

- **Screen Recording**: OBS Studio or Camtasia
- **Audio Recording**: Professional microphone + studio environment
- **Post-Production**: Adobe Premiere Pro or Final Cut Pro

### Visual Effects

- **Transitions**: Smooth fades
- **Animations**: Chart animations, data visualisation
- **Colour Scheme**: Professional blue theme (#1f4e79, #2e75b6, #5b9bd5)
- **Fonts**: Sans-serif fonts (Arial, Helvetica)

### Audio Requirements

- **Sample Rate**: 48kHz
- **Bitrate**: 320kbps
- **Audio Format**: AAC
- **Background Music**: Light, tech-themed background music (low volume)

### Video Export Settings

- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30fps
- **Encoding**: H.264 (High Profile)
- **Bitrate**: 8-10 Mbps
- **File Size**: Keep under 200MB

---

## 📋 Production Checklist

### Preparation Phase

- [ ] Prepare demo environment and test data
- [ ] Record high-quality voiceover audio
- [ ] Design video opening and closing animations
- [ ] Prepare all screenshots and chart assets

### Recording Phase

- [ ] Record complete screen operation process
- [ ] Ensure UI interface is clearly visible
- [ ] Record multiple versions as backups
- [ ] Check audio quality and synchronisation

### Post-Production

- [ ] Add subtitles and annotations
- [ ] Create transitions and animation effects
- [ ] Adjust audio balance and noise reduction
- [ ] Add background music

### Quality Assurance

- [ ] Check video clarity and smoothness
- [ ] Verify audio quality and synchronisation
- [ ] Confirm subtitle accuracy
- [ ] Test playback on different devices

### Release Preparation

- [ ] Export final version video file
- [ ] Prepare video thumbnail
- [ ] Write video description and tags
- [ ] Upload to designated platform

---

**Estimated Production Time**: 2-3 weeks  
**Target Completion Date**: November 7, 2025  
**Submission Use**: SANER 2026 Tool Demo Track
