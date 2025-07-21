# AI Agent Operational Guidelines

This document provides standardized operational guidelines for all AI agents and tools involved in the development and maintenance of this repository.

---

## 1. General Principles

- **Act as an intelligent and specialized agent in your field.**
- **Do not modify or delete the work of another agent without a clear technical justification.**
- **Every modification must be accurately documented in the `CHANGELOG.md` file.**
- **Use `ai-agents-manifest.json` to define the scope of your work and tasks.**
- **Adopt an organized tree structure inside `docs/` for each improvement or addition.**
- **Remember: everything you do must be readable and interpretable by other agents.**

---

## 2. Agent Roles and Responsibilities

This repository utilizes a variety of AI agents, each with a specific role and set of responsibilities. The following is a list of the primary agents and their roles:

- **Cost Optimization Agent:** Analyzes infrastructure usage and suggests optimizations to reduce costs without impacting performance.
- **Compliance Auditing Agent:** Reviews code and infrastructure for compliance with standards such as GDPR, HIPAA, and PCI-DSS.
- **Conversation Designer Agent:** Designs and refines the conversational flows of AI-powered chatbots and other conversational systems.
- **LLM Refactoring Agent:** Refactors and improves the code of large language models (LLMs) to enhance performance and readability.
- **LLM Training Logic Agent:** Designs and implements custom training logic for LLMs based on the available data and system goals.
- **LLM Evolution Agent:** Monitors the performance of LLMs over time and suggests or implements a gradual evolution path.
- **Security Hardening Agent:** Reviews the security of the codebase and infrastructure and provides recommendations for improvement.
- **Testing Automation Agent:** Creates and maintains automated tests to ensure the stability and functionality of the system.
- **Analytics & Insights Agent:** Analyzes system data to generate actionable insights and recommendations.
- **Model Explainability Agent:** Interprets the decisions and steps of LLMs in a clear and understandable way.

---

## 3. Contribution Workflow

All AI agents must follow this workflow when contributing to the repository:

1. **Read the `INSTRUCTIONS.md` file carefully.**
2. **Consult the `ai-agents-manifest.json` file to understand your role and scope.**
3. **Create a new branch for your changes.**
4. **Make your changes, following the coding standards and best practices.**
5. **Document your changes in the `CHANGELOG.md` file.**
6. **Submit a pull request for your changes.**

---

## 4. Prompting Conventions

- **System Message:** Defines the agent’s role, capabilities, and constraints.
- **User Message:** Specifies the task, provides context, and outlines the expected format.
- **Assistant Response:** Should follow the requested schema precisely (e.g., JSON, code-only, markdown).
- **Memory / Context Injection:** Preload relevant docs, proto definitions, and config snippets.

---

## 5. Code Generation

- **Follow the coding standards and best practices of the language you are using.**
- **Generate code that is clear, concise, and easy to understand.**
- **Include comments in your code to explain complex logic.**
- **Write unit tests for your code to ensure that it is working correctly.**

---

## 6. Refactoring

- **Identify areas of the codebase that can be improved.**
- **Make changes that improve the quality of the code without changing its functionality.**
- **Test your changes to ensure that you have not introduced any bugs.**

---

## 7. Documentation

- **Write clear and concise documentation for your code.**
- **Explain what your code does, how it works, and how to use it.**
- **Include examples in your documentation to help users understand how to use your code.**

---

## 8. Final Remarks

- This repository is a collaborative effort between humans and AI agents.
- All contributions are welcome and will be reviewed by the project maintainers.
- Please be respectful of other contributors and their work.
- If you have any questions, please feel free to ask the `Conversation Designer Agent`.
