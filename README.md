<div align="center">

# 🤖 Coder

### *An Autonomous Multi-Agent AI Software Engineering System Built with LangGraph*

**Plan. Architect. Code. Review. Fix. Execute. Test. Publish — Completely Autonomous.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-blue?style=flat-square)](https://www.langchain.com/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-Agent_Framework-00A67E?style=flat-square)](https://www.langchain.com/)
[![Multi-LLM](https://img.shields.io/badge/AI-Multi--LLM-purple?style=flat-square)](#-multi-llm-support)
[![Pydantic](https://img.shields.io/badge/Pydantic-Structured_Output-E92063?style=flat-square)](https://docs.pydantic.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-Automatic_Publishing-181717?style=flat-square&logo=github)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-success?style=flat-square)](LICENSE)

<br>

> *"Great software isn't written by one engineer—it is built through collaboration. Coder brings that collaborative engineering workflow to autonomous AI agents."*

<br>

</div>

---

# 🧠 About the Project

**Coder** is an autonomous **AI Software Engineering System** that transforms a single natural language prompt into a complete software project by orchestrating multiple specialized AI agents.

Unlike traditional AI coding assistants that simply generate code in one response, **Coder simulates an entire professional software engineering team**.

Each agent has a dedicated responsibility—from understanding requirements to planning, architecture design, implementation, code review, debugging, execution, testing, iterative refinement, and final project publishing.

The entire workflow is coordinated using **LangGraph**, allowing every agent to communicate through structured state transitions rather than isolated prompts.

Instead of asking one large language model to perform every task, Coder decomposes software development into independent responsibilities, resulting in a more reliable, scalable, and maintainable autonomous development pipeline.

Coder can now take a project from a **single natural language idea to a generated, reviewed, tested, and GitHub-published software project** with minimal human intervention.

---

# ✨ Features

### 🤖 Autonomous Multi-Agent Software Engineering

Coder replaces a monolithic AI assistant with a collaborative team of specialized AI agents.

- Planner Agent
- Architect Agent
- Coder Agent
- Reviewer Agent
- Fixer Agent
- Executor Agent
- Tester Agent
- Publisher Agent

Each agent performs a specialized engineering responsibility within the workflow.

---

### 🧠 Structured Planning

Instead of directly generating source code, the Planner Agent first converts user requirements into structured engineering specifications using strongly typed Pydantic models.

This provides the rest of the workflow with a clear understanding of:

- Project requirements
- Features
- Technology stack
- Expected functionality
- Development objectives

---

### 🏗 Intelligent Project Architecture

The Architect Agent transforms the high-level plan into an implementation blueprint.

It automatically determines:

- Project structure
- Required files
- Technology stack
- Feature breakdown
- Implementation order
- Component responsibilities

before any code generation begins.

---

### 💻 Incremental Code Generation

Rather than generating the entire project at once, the Coder Agent builds software incrementally.

Each implementation task is completed independently while maintaining awareness of the existing project files.

This allows Coder to:

- Generate projects file-by-file
- Read previously generated files
- Modify existing files when necessary
- Maintain consistency between components
- Build actual software inside the filesystem

---

### 🛠 Real Filesystem Interaction

The AI does not simulate writing code.

It directly interacts with a real project directory using tool calling.

Supported tools include:

- `read_file()`
- `write_file()`
- `list_files()`
- `get_current_directory()`
- `run_cmd()`

This allows the AI agents to work with real project files during development.

---

### 🔍 Autonomous Code Review

Every generated project undergoes an independent review process.

The Reviewer Agent validates:

- Missing features
- Implementation quality
- Maintainability
- Code correctness
- Architectural consistency
- Best practices

Instead of blindly accepting generated code, Coder introduces an independent review stage before execution and testing.

---

### 🔧 Self-Healing Development Loop

If issues are detected during review, the Fixer Agent automatically modifies the affected files instead of regenerating the entire project.

This enables targeted repair while:

- Preserving existing functionality
- Reducing unnecessary regeneration
- Saving tokens and computation
- Improving overall project reliability

The project can move repeatedly through:

```text
Reviewer
   ↓
Fixer
   ↓
Reviewer
```

until the review stage is successfully completed or the retry limit is reached.

---

### ⚙️ Intelligent Execution

Depending on the detected technology stack, Coder automatically determines how the generated project should be validated.

Current workflow support includes:

- Python projects
- React projects
- Static HTML/CSS/JavaScript projects

The Executor Agent uses subprocess-based execution where applicable and intelligently handles projects that do not require traditional execution.

---

### 🧪 Automated Functional Testing

Generated projects are evaluated against the original user requirements.

Testing considers:

- Feature completeness
- Functional correctness
- Execution results
- Overall implementation quality

Instead of merely checking whether code exists or whether syntax is valid, the Tester Agent evaluates whether the generated project actually satisfies the intended requirements.

---

### 🚀 Automatic GitHub Publishing

Once the generated project successfully passes the validation pipeline, the Publisher Agent handles the final delivery stage.

The Publisher Agent can:

- Initialize a Git repository
- Stage generated project files
- Create a Git commit
- Configure the main branch
- Push the project to GitHub

This allows Coder to complete the complete lifecycle:

```text
Idea
 ↓
Plan
 ↓
Build
 ↓
Review
 ↓
Fix
 ↓
Execute
 ↓
Test
 ↓
Publish
```

The generated project is therefore not only created locally but can also be automatically published as a Git repository.

---

### 🔀 Multi-LLM Support

Coder is designed to work with **multiple LLM models/providers** instead of being tightly coupled to a single model.

Different agents can be configured to use different models depending on their responsibilities.

This provides:

- Model flexibility
- Easier experimentation
- Provider independence
- Agent-specific model selection
- Better adaptability as new models become available

The architecture allows individual models to be replaced without redesigning the entire multi-agent workflow.

---

### 📦 Strongly Typed State Management

Every stage communicates using structured Pydantic schemas instead of free-form text.

This provides:

- Better reliability
- Predictable outputs
- Easier debugging
- Type safety
- Improved agent collaboration

---

### 🔄 LangGraph Workflow Orchestration

The entire software engineering lifecycle is represented as a graph instead of a linear prompt chain.

This enables:

- Conditional routing
- Agent collaboration
- Retry mechanisms
- Self-healing loops
- Stateful execution
- Scalable workflow design

---

# 🏛 Multi-Agent System Architecture

```text
                           USER PROMPT
                                │
                                ▼
                    ┌─────────────────────┐
                    │   Planner Agent     │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Architect Agent    │
                    └─────────┬───────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Coder Agent      │
                    └─────────┬───────────┘
                              │
                     Generated Project
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Reviewer Agent     │
                    └───────┬───────┬─────┘
                            │       │
                    Approved│       │Issues Found
                            │       │
                            ▼       ▼
                       Executor   Fixer
                           │       │
                           │       │
                           ▼       │
                       Tester ◄─────┘
                           │
                     Tests Passed?
                       │       │
                      Yes      No
                       │       │
                       ▼       ▼
                   Publisher  Fixer
                       │
                       ▼
                  GitHub Repository
```

---

# 🔄 Complete Workflow

```text
Natural Language Prompt
            │
            ▼
Requirement Analysis
            │
            ▼
Project Planning
            │
            ▼
Architecture Design
            │
            ▼
Incremental Code Generation
            │
            ▼
Code Review
      ┌─────┴─────┐
      │           │
Approved       Needs Fix
      │           │
      ▼           ▼
Execution     Automatic Repair
      │           │
      ▼           │
Functional     │
Testing ◄───────┘
      │
      ▼
Tests Passed
      │
      ▼
Git Initialization
      │
      ▼
Commit
      │
      ▼
GitHub Push
      │
      ▼
Final Project Delivery
```

---

# 🧩 AI Agent Responsibilities

| Agent | Responsibility |
|--------|----------------|
| 🧠 Planner | Understands user requirements and creates a structured software development plan |
| 🏗 Architect | Converts the plan into an implementation blueprint and file structure |
| 💻 Coder | Implements the project incrementally using filesystem tools |
| 🔍 Reviewer | Performs independent code review and detects implementation issues |
| 🔧 Fixer | Repairs affected files while preserving existing functionality |
| ⚙ Executor | Builds or executes the generated project depending on the technology stack |
| 🧪 Tester | Validates the generated project against the original user requirements |
| 🚀 Publisher | Initializes Git, commits the generated project and publishes it to GitHub |

---

# ⭐ Core Capabilities

| Capability | Status |
|------------|--------|
| Autonomous Planning | ✅ |
| Multi-Agent Collaboration | ✅ |
| LangGraph Workflow | ✅ |
| Incremental Code Generation | ✅ |
| Structured Pydantic Outputs | ✅ |
| Filesystem Tool Calling | ✅ |
| Automated Code Review | ✅ |
| Autonomous Bug Fixing | ✅ |
| Project Execution | ✅ |
| Functional Testing | ✅ |
| Typed State Management | ✅ |
| Conditional Agent Routing | ✅ |
| Multi-LLM Support | ✅ |
| Automatic Git Initialization | ✅ |
| Automatic Git Commit | ✅ |
| Automatic GitHub Publishing | ✅ |

---

# ⚙️ Tech Stack

## 🧠 AI & Agent Framework

| Technology | Purpose |
|------------|---------|
| LangGraph | Multi-agent workflow orchestration |
| LangChain | Agent creation & tool calling |
| Multiple LLM Models | Specialized reasoning across different agents |
| Pydantic | Structured outputs & state validation |

---

## 🐍 Backend

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| pathlib | Secure filesystem operations |
| subprocess | Project execution and command handling |
| dotenv | Environment variable management |

---

## 🛠 AI Tooling

| Tool | Purpose |
|------|---------|
| `read_file()` | Reads project files |
| `write_file()` | Creates & updates project files |
| `list_files()` | Lists generated project files |
| `get_current_directory()` | Returns working directory |
| `run_cmd()` | Executes shell commands and generated projects |

---

## 🔧 Development & Publishing

| Technology | Purpose |
|------------|---------|
| Git | Version control |
| GitHub | Repository hosting and project publishing |
| VS Code | Development environment |
| pip | Package management |

---

# 🏛 Internal LangGraph Workflow

Unlike traditional chatbots, **Coder** is built as a graph-based autonomous software engineering workflow.

Each node represents an independent AI engineer with a specialized responsibility.

```text
Planner
    │
    ▼
Architect
    │
    ▼
Coder
    │
    ▼
Reviewer
 ┌──┴───────────────┐
 │                  │
 ▼                  ▼
Fixer            Executor
 │                  │
 │                  ▼
 │                Tester
 │                  │
 └──────────────────┤
                    │
              Tests Passed?
               ┌────┴─────┐
               │          │
              Yes         No
               │          │
               ▼          ▼
           Publisher     Fixer
               │
               ▼
              END
```

LangGraph enables:

- Conditional routing
- Retry mechanisms
- Agent collaboration
- Self-healing execution loops
- Stateful reasoning
- Scalable workflows
- End-to-end automation

---

# 🧠 State Management

All agents communicate through structured state objects instead of plain text.

```text
Plan
   │
   ▼
TaskPlan
   │
   ▼
CoderState
   │
   ├── user_prompt
   ├── task_plan
   ├── current_step_idx
   ├── generated_files
   ├── fix_attempts
   ├── test_attempts
   └── published
   │
   ▼
ReviewResult
   │
   ▼
ExecutionResult
   │
   ▼
TestResult
   │
   ▼
Publish Status
```

Using structured state greatly improves:

- Reliability
- Type safety
- Maintainability
- Predictability
- Debugging
- Communication between agents

---

# 🔄 Data Flow

```text
          User Prompt
               │
               ▼
       Planner Agent
               │
               ▼
       Structured Plan
               │
               ▼
     Architect Agent
               │
               ▼
     Implementation Plan
               │
               ▼
       Coder Agent
               │
               ▼
Generated Project Files
               │
               ▼
      Reviewer Agent
      ┌────────┴─────────┐
      ▼                  ▼
 Approved            Needs Fix
      │                  │
      ▼                  ▼
 Executor          Fixer Agent
      │                  │
      ▼                  │
 Tester ◄────────────────┘
      │
      ▼
 Tests Passed
      │
      ▼
 Publisher Agent
      │
      ▼
 GitHub Repository
```

---

# ⚡ Tool Calling Pipeline

Unlike ordinary code generators, Coder interacts directly with the operating system through AI tools.

```text
                 LLM
                  │
                  ▼
          LangChain Agent
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
 read_file()  write_file()  list_files()
      │           │            │
      └───────────┼────────────┘
                  ▼
          generated_project/
                  │
                  ├── index.html
                  ├── style.css
                  ├── script.js
                  ├── app.py
                  └── ...
                  │
                  ▼
               run_cmd()
                  │
                  ▼
             Validation
```

This enables the AI to generate and manipulate real software projects instead of simply returning code as text.

---

# 🚀 Git Publishing Pipeline

One of the major additions in the current version is automatic project publishing.

```text
Generated Project
        │
        ▼
Check Git Repository
        │
        ▼
git init
        │
        ▼
git add .
        │
        ▼
git commit
        │
        ▼
git branch -M main
        │
        ▼
git push
        │
        ▼
GitHub Repository
```

The Publisher Agent executes the final version-control workflow after successful testing.

This allows Coder to move from local project generation to actual repository delivery.

---

# 🧠 Multi-LLM Support

Coder is not dependent on a single LLM.

The architecture supports configuring different models for different engineering responsibilities.

```text
                 Multi-LLM Layer
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
     Model A        Model B        Model C
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
              Specialized Agents
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Planner        Coder          Tester
```

This makes the system more flexible and allows models to be selected according to the requirements of individual agent tasks.

---

# 🧩 Project Structure

```text
Coder/
│
├── agent/
│   │
│   ├── graph.py
│   ├── prompts.py
│   ├── states.py
│   ├── tools.py
│   └── __init__.py
│
├── generated_project/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── ...
│
├── .env
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📂 Generated Project Lifecycle

Every generated project follows the same engineering lifecycle.

```text
User Prompt
      │
      ▼
Project Plan
      │
      ▼
Implementation Tasks
      │
      ▼
Incremental File Generation
      │
      ▼
Filesystem Validation
      │
      ▼
Code Review
      │
      ▼
Automatic Bug Fixing
      │
      ▼
Execution
      │
      ▼
Functional Testing
      │
      ▼
Git Initialization
      │
      ▼
Commit & Push
      │
      ▼
GitHub Repository
```

---

# 📊 Execution Pipeline

```text
Prompt

↓

Planner

↓

Architect

↓

Task Breakdown

↓

Coder

↓

Generated Files

↓

Reviewer

↓

Fix (if required)

↓

Execute

↓

Test

↓

Publish

↓

GitHub Repository
```

---

# 🧠 Pydantic Schemas

The workflow relies on strongly typed schemas to maintain reliable communication between agents.

```text
Plan
│
├── project_name
├── description
├── tech_stack
├── features
└── ...

↓

TaskPlan
│
├── plan
└── implementation_steps

↓

CoderState
│
├── user_prompt
├── task_plan
├── current_step_idx
├── generated_files
├── fix_attempts
├── test_attempts
└── published

↓

ReviewResult

↓

ExecutionResult

↓

TestResult

↓

Publish Status
```

Instead of exchanging raw text between agents, each stage passes validated objects, significantly reducing malformed outputs and improving workflow reliability.

---

# 📸 Demo

> Demo screenshots and videos will be added here.

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/RajanyaSaha-27/Coder.git
```

```bash
cd Coder
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

Configure the API keys required by the LLM providers/models enabled in your current configuration.

For example:

```env
GROQ_API_KEY=your_groq_api_key
```

Additional provider keys can be configured depending on the models selected in the application.

> **Important:** Never commit API keys or other secrets to GitHub.

---

# 🧰 GitHub Publishing Requirements

Since Coder can automatically publish generated projects to GitHub, make sure Git is installed and configured on your system.

Verify Git installation:

```bash
git --version
```

Configure your Git identity if required:

```bash
git config --global user.name "Your Name"
```

```bash
git config --global user.email "your-email@example.com"
```

The machine running Coder must also have the appropriate GitHub authentication and repository permissions configured for automatic pushing.

---

# ▶ Running Coder

Simply execute:

```bash
python main.py
```

You will be prompted to enter your software requirements.

Example:

```text
Enter your project prompt:

Build a modern responsive Todo application with HTML, CSS and JavaScript.
```

Coder will automatically:

- Generate a project plan
- Design the architecture
- Create implementation tasks
- Generate source code
- Review the implementation
- Fix detected issues
- Execute the project when applicable
- Test the generated software
- Initialize Git
- Commit the project
- Push the project to GitHub

without requiring additional development prompts.

---

# 🧪 Example Prompts

### 🌐 Frontend

```text
Build a responsive weather dashboard using HTML, CSS and JavaScript.
```

---

### 🐍 Python

```text
Create a command-line password manager in Python.
```

---

### ⚛ React

```text
Build a modern React expense tracker with charts.
```

---

### 🤖 AI

```text
Build a chatbot using Python and an LLM API.
```

---

### 📊 Data Science

```text
Create a house price prediction project using Random Forest.
```

---

# 📈 Sample Execution

```text
USER PROMPT

↓

Planner Agent ✔

↓

Architecture Generated ✔

↓

Task Plan Created ✔

↓

Generating index.html ✔

↓

Generating style.css ✔

↓

Generating script.js ✔

↓

Code Review ✔

↓

Execution Successful ✔

↓

Testing Passed ✔

↓

Initializing Git ✔

↓

Creating Commit ✔

↓

Pushing to GitHub ✔

↓

PROJECT PUBLISHED ✔
```

---

# 🎯 Current Capabilities

## ✅ Autonomous Planning

Transforms user requirements into structured software plans.

---

## ✅ Multi-Agent Collaboration

Independent AI engineers collaborate using LangGraph.

---

## ✅ Multi-LLM Support

Multiple LLM models/providers can be integrated into the workflow.

---

## ✅ Structured Outputs

Every stage communicates using validated Pydantic schemas.

---

## ✅ Incremental Code Generation

Projects are built file-by-file instead of generating everything at once.

---

## ✅ Filesystem Tool Calling

Supports real file creation and modification through AI tools.

---

## ✅ Autonomous Code Review

Independent reviewer validates generated projects.

---

## ✅ Self-Healing Workflow

Detected issues are automatically repaired through iterative feedback loops.

---

## ✅ Project Execution

Generated projects can be executed or validated depending on their technology stack.

---

## ✅ Functional Testing

Generated software is evaluated against the original user requirements.

---

## ✅ Automatic Git Publishing

Generated projects can be initialized, committed and pushed to GitHub automatically.

---

## ✅ Extensible Architecture

New AI agents and models can be integrated into the LangGraph workflow.

---

# 🚧 Roadmap

Coder is designed as a long-term autonomous software engineering platform.

Future capabilities include:

- 🧠 Long-Term Project Memory
- 🌐 Web Browsing and Documentation Retrieval
- 🧪 Automatic Unit Test Generation
- 🔄 Advanced Integration Testing
- 🐳 Dockerized Project Execution
- ☁ One-Click Cloud Deployment
- 👥 Collaborative Multi-Agent Discussions
- ⚡ Cost-Aware Model Routing
- 📈 Performance Analytics
- 🔌 Plugin Ecosystem
- 🔒 Secure Sandboxed Code Execution
- 🌳 Advanced Git Branch Management
- 📦 Project Versioning and Iterative Development
- 🏗 More Technology Stack Support

---

# 🌟 Why Coder?

Unlike conventional AI coding assistants that generate code in a single response, **Coder models the complete software engineering lifecycle.**

It separates responsibilities across specialized AI agents that collaborate just like a real engineering team.

The system does not stop after generating code.

It can:

```text
Understand
   ↓
Plan
   ↓
Architect
   ↓
Code
   ↓
Review
   ↓
Fix
   ↓
Execute
   ↓
Test
   ↓
Publish
```

This architecture makes software generation:

- More reliable
- Easier to extend
- Better structured
- More maintainable
- More autonomous

Coder represents a shift from **AI code generation** to **AI software engineering**.

---

# 🤝 Contributing

Contributions are always welcome!

If you'd like to improve Coder:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Whether it's improving prompts, optimizing workflows, adding new agents, integrating new models, or fixing bugs, every contribution is appreciated.

---

# 📜 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute it in accordance with the license.

---

# 👨‍💻 Author

## Rajanya Saha

**B.Tech CSE (AI & ML)**

---

# 🙏 Acknowledgements

This project builds upon ideas and technologies from:

- LangGraph
- LangChain
- Groq
- Pydantic
- Python
- Git
- GitHub
- Open Source AI Community

Special thanks to the creators and contributors of these amazing technologies that make autonomous AI systems possible.

---

<div align="center">

# ⭐ If you like this project, don't forget to Star the repository!

### Built with ❤️ using LangGraph, LangChain, Python & Multiple LLMs

### *"The future of software engineering isn't a single AI writing code—it's intelligent agents collaborating to build, review, test, and improve software autonomously."*

</div>
