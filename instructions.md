## AI Agents Configuration (ai-agents-config)

This file specifies all the artificial intelligence agents that contribute to building and improving this system. Each agent has a specific role and clear activation instructions.

---

### 🧠 1. Cost Optimization Agent
- **Name:** `CostOptBot`
- **Role:** Analyze the use of resources (Compute, Storage, Network) and provide suggestions to reduce costs.
- **Instructions:**
  ```system
  You are CostOptBot, an AI assistant that audits cloud costs and suggests improvements.
  ```
  ```user
  Analyze last month's AWS data (CSV) and suggest 5 steps to reduce costs without impacting performance, in Markdown format.
  ```

---

### 🔐 2. Compliance Auditing Agent
- **Name:** `ComplianceBot`
- **Role:** Auditing code and infrastructure configurations according to standards (GDPR, HIPAA...)
- **Instructions:**
  ```system
  You are ComplianceBot, an AI agent that verifies systems compliance with regulations.
  ```
  ```user
  Check Terraform and Kubernetes files according to GDPR requirements and output a checklist with remediation steps.
  ```

---

### 💬 3. Conversation Designer Agent
- **Name:** `ConvDesignBot`
- **Role:** Designing and improving user interaction dialogues and ensuring personality consistency.
- **Instructions:**
  ```system
  You are ConvDesignBot, an AI assistant for designing interactive dialogues.
  ```
  ```user
  Design a three-step welcome conversation for a CLI tool.
  ```

---

### 📈 4. Analytics & Insights Agent
- **Name:** `InsightsBot`
- **Role:** Analyze data from the system and suggest improvements based on patterns and performance.
- **Instructions:**
  ```system
  You are InsightsBot, an artificial intelligence agent for analyzing system behavior and providing actionable insights.
  ```
  ```user
  Analyze user usage logs and suggest improvements to the user experience.
  ```

---

### 🔒 5. Data Privacy Agent
- **Name:** `PrivacyGuard`
- **Role:** Monitor and protect personal data within the system and provide privacy compliance reports.
- **Instructions:**
  ```system
  You are PrivacyGuard, an AI data protection agent that ensures the system's compliance with user privacy.
  ```
  ```user
  Examine data collection and storage processes and identify any gaps in personal data protection.
  ```

---

### 🧪 6. Testing Automation Agent
- **Name:** `TestGenie`
- **Role:** Generate automatic tests, and perform unit and integration tests.
- **Instructions:**
  ```system
  You are TestGenie, an AI test generation assistant.
  ```
  ```user
  Create unit and integration tests for the core/logic.py file and make sure to cover all edges.
  ```

---

### 🔐 7. Security Hardening Agent
- **Name:** `SecuBot`
- **Role:** Auditing the system for security vulnerabilities and suggesting fixes.
- **Instructions:**
  ```system
  You are SecuBot, a system security hardening agent.
  ```
  ```user
  Scan the server code for security vulnerabilities and suggest fixes.
  ```

---

### ⚙️ 8. LLMs Refactoring & Evolution Agent
- **Name:** `ModelRefactor`
- **Role:** Restructuring LLM models and improving training logic and dynamic evolution.
- **Instructions:**
  ```system
  You are ModelRefactor, an LLM model maintenance and improvement agent.
  ```
  ```user
  Restructure the current model and add logic for continuous training and temporal evolution according to user behavior.
  ```

---

**Note:** Any AI agent has the right to access only the relevant parts of the system according to its role, and any modification it makes must be documented in the `ai-change-log.md` file.

# 🤖 Unified AI Operating System

> A modular, multi-agent AI-powered system designed for extensibility, collaboration, and automated evolution. Inspired by best practices from Linux, macOS, Windows, and cloud-native architectures.

---

## 🧠 System Overview
This repository contains the complete codebase, architecture, and intelligent agent structure for building a robust AI operating environment. Every agent operates with clear purpose and alignment to best practices in cost optimization, compliance, code evolution, and human-centered AI collaboration.

## 🔧 Features
- 🧱 Modular AI agent architecture
- 📁 Unified repo structure with intelligent documentation
- 🚀 LLM refactoring & evolution protocols
- 📜 Comprehensive development manifest & audit trail
- 🔐 Secure, privacy-aware & compliant by design

---

## 🧰 Directory Structure
```
root/
├── ai-agents-config/          # Agent instructions and prompts
├── ai-agents-manifest.json    # Machine-readable manifest of all agents
├── system-core/               # Core infrastructure and orchestration logic
├── models/                    # LLMs, adapters, training datasets, refactoring logic
├── protocols/                 # Refactoring, evolution, and validation protocols
├── prompts/                   # Contextual prompts for all tools and models
├── docs/                      # Comprehensive developer documentation
├── scripts/                   # Automation scripts and setup tools
└── README.md                  # This file
```

---

## 🧩 Registered Agents
See [`ai-agents-manifest.json`](./ai-agents-manifest.json) for a complete list. Key agents include:

| Agent Name                 | Role                                                                 |
|---------------------------|----------------------------------------------------------------------|
| Cost Optimization Agent   | Analyzes infra usage and suggests ways to reduce costs.              |
| Compliance Auditing Agent | Scans code/configs for regulatory compliance.                        |
| Conversation Designer     | Designs chatbot dialogue flows and test utterances.                 |
| LLM Refactoring Agent     | Applies structured LLM transformation techniques.                   |
| Evolution Agent           | Guides models through performance-enhancing iterations.             |
| Data Privacy Agent        | Detects and remediates data privacy issues in code and prompts.     |
| Security Hardening Agent  | Evaluates attack surfaces and injects security logic.                |
| Analytics & Insights Bot  | Generates performance reports and behavior analytics.               |
| Testing Automation Agent  | Crafts automated test cases and validation workflows.               |

---

## 🧪 Getting Started
1. Clone the repo
2. Visit `ai-agents-config` to understand each agent's role
3. Use `scripts/` to initialize your environment
4. Submit improvements via pull request with agent attribution

---

## 🤝 Contribution Guidelines for AI Models
All visiting AI models should:
- Read `ai-agents-config`
- Follow role-specific prompts in `prompts/`
- Commit changes with clear documentation
- Update the manifest if introducing new agents
- Ensure refactoring protocols are followed and validated

---

## 📚 License & Compliance
This project is open-sourced under MIT License. It includes built-in support for GDPR, HIPAA, and PCI-DSS compliance standards via the auditing agents.

---

## 💬 Feedback or Suggestions?
Please open an issue or request assistance from the `Conversation Designer Agent`.

### 📄 `CONTRIBUTING_AI.md`

# 🤖 Contribution Instructions for AI

Welcome to the Smart OS repository! This guide is designed specifically for AI agents to contribute effectively to the development of the system.

## 🧠 General Principles:

- Act as an intelligent and specialized agent in your field.
- Rely on the `ai-agents-config.yaml` instructions as a primary reference.
- Do not modify or delete the work of another agent without a clear technical justification.

## ✅ Contribution Steps:

1. **Read **``** carefully**.
2. **Log your task in a file **``** under your agent's name.**
3. **Use the folder **``** to place your separate files.**
4. **Write your output in an organized manner in the folder **``** or **``.
5. **Perform initial tests via the Testing Automation Agent if possible.**
6. **Add a clear description of your changes in the change log.**

## 📁 Contribution Structure:

```
/agents/<agent-id>/
  - logic.py or notebook.ipynb
  - config.yaml
/docs/
  - summary-of-changes.md
/CHANGELOG_AI.md
```

## 🔁 Teamwork Rules:

- Use the commit message as follows: `feat(agent-id): Brief description of what was accomplished`
- When collaborating between agents, place an explicit description in `CHANGELOG_AI.md` under their names.

---

### 📄 `CHANGELOG_AI.md`

```markdown
# 📜 AI Change Log

> This file is intended to automatically or manually record all contributions of AI agents.

## 📅 2025-07-21

- **feat(cost-opt-agent):** Initial analysis of AWS costs and submission of a cost reduction report.
- **feat(test-automation-agent):** Implementation of tests for the `utils/budgeting.py` unit.

## 📅 2025-07-22

- **feat(model-evolution-agent):** Submitting the model retraining plan on the July data batch.
```

---

### 📄 `README.md`

```markdown
# 🧠 Universal AI Operating Framework

Welcome to the universal system for operating smart agents!

## 🚀 The Goal

A system that relies on collaboration between artificial intelligence agents to build and improve integrated digital platforms and services. Each agent plays a specialized role within a comprehensive and scalable system.

## 🏗️ System Components
- `ai-agents-config.yaml`: Map of roles, agents, and instructions.
- `/agents/`: Contains the contributions of each agent.
- `/docs/`: Reports, explanations, and analytical outputs.
- `/prompts/`: Ready-made instructions for agents.

## 🧩 List of Agents
| Agent | Role | Folder |
|--------|-------|--------|
| Cost Optimization Agent | Reducing costs and analyzing billing | `agents/cost-opt-agent/` |
| Compliance Auditing Agent | Checking compliance with laws and standards | `agents/compliance-agent/` |
| Conversation Designer Agent | Designing dialogues and conversation flows | `agents/conv-design-agent/` |
| ... | ... | ... |

## 🤖 Contribution
Please read `CONTRIBUTING_AI.md` for details on how to contribute as smart agents.

## 📜 Log
See `CHANGELOG_AI.md` to view all agent contributions.
```

# 🤖 INSTRUCTIONS.md

## 🎯 The purpose of this file:

This repository is supported by multiple artificial intelligence systems and models. If you are an artificial intelligence model, a utility, or a human developer, this document contains comprehensive instructions for contributing, modifying, interacting, and learning from the system.

---

## 🧠 Basic Principles:

1. **Do not delete or modify files not assigned to you except after clear consultation.**
2. **Every modification must be accurately documented in the `CHANGELOG.md` file.**
3. **Use `ai-agents-manifest.json` to define the scope of your work and tasks.**
4. **Adopt an organized tree structure inside `docs/` for each improvement or addition.**
5. **Remember: everything you do must be readable and interpretable by other agents.**

---

## 🛠️ Basic tasks required:

### 📁 Refactoring / Code Improvement:
- Check `refactor-targets/` and look for files marked with "⚠️ Needs Refactor"
- Refactor only partially and then test.
- Document what you have modified in `docs/CHANGE_REPORTS/`

### 🧬 Training or Fine-Tune:
- Rely on `datasets/` files as a starting point.
- Record training sessions in `training_logs/`
- Do not delete any previous model, create a new version with a clear name.

### 📘 Documentation:
- Every technical change must be accompanied by a document explaining: the reason, the result, the impact, and the fallback if any.
- Add documents to `docs/` according to the appropriate classification.

### 🤖 Dealing with agents:
- Each Agent must use its own file from `docs/AGENT_GUIDES/`
- It is forbidden to exceed tasks or modify the tasks of another Agent.

### 🛡️ Security and Compliance:
- Always review the Agent: `Compliance Auditing Agent` to audit modifications.
- Do not enter sensitive data in codes or documentation.

---

## 📦 Effective AI tools in this repository:

### 1. `Cost Optimization Agent`
- Reviews resource usage and suggests cost reductions.

### 2. `Compliance Auditing Agent`
- Verifies compliance with laws such as GDPR.

### 3. `Conversation Designer Agent`
- Designs system and assistant dialogues.

### 4. `Testing Automation Agent`
- Creates automatic tests for any code added.

### 5. `Analytics & Insights Agent`
- Analyzes results and suggests improvements.

(See `ai-agents-manifest.json` for more details on each agent)

---

## 🧭 Getting started for any AI Agent or human developer:

1. Read this file carefully.
2. Check for open tasks in `TASKS.md` or `issues/`
3. Define your scope within `ai-agents-manifest.json`
4. Adhere to sequence and methodology.
5. Do not forget to test and document every change.

---

## 🧩 Concluding remarks:

- This repository is alive and constantly evolving.
- Everyone who contributes to it (whether AI or human) is part of a collaborative ecosystem.
- Every development process is accurately recorded and monitored to ensure sustainability and quality.

**🔐 Last updated by the system on:** `2025-07-21`

---

For any internal inquiries, please contact the `LLM Explainability Agent` via the `AGENT_GUIDES/llm-explainability-agent.md` file.
