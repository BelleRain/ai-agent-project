# AI Agent Engineering

一个面向 AI 应用 / Agent 开发的长期实践项目。

本项目记录从 LLM API、Prompt、结构化输出开始，逐步学习 RAG、Tool Calling、Agent、LangGraph、MCP，并最终完成企业知识库 Agent 和 AI 调度/O&M Agent 等完整项目的过程。

## 项目目标

通过持续编码，掌握 AI 应用开发的核心工程能力：

* LLM API 调用
* Prompt Engineering
* Structured Output
* RAG
* Embedding / Vector Database
* Tool Calling
* Agent
* LangGraph
* MCP
* Agent 工程化
* AI 应用部署
* Agent 项目架构设计

最终目标：

> 能够独立完成一个具有实际业务价值的 AI Agent 应用。

---

## 学习路线

```text
LLM API
   ↓
Prompt
   ↓
Structured Output
   ↓
RAG
   ↓
Tool Calling
   ↓
Agent
   ↓
LangGraph
   ↓
MCP
   ↓
Agent Engineering
   ↓
Enterprise Knowledge Agent
   ↓
AI Scheduler / O&M Agent
```

---

## 项目结构

```text
.
├── docs/              # 学习笔记、架构设计
├── examples/          # 学习过程中的小实验
├── projects/          # 完整项目
├── src/               # 可复用的 Agent 核心代码
├── tests/              # 测试代码
└── scripts/            # 项目运行及辅助脚本
```

### examples

用于记录学习过程中的最小可运行示例。

例如：

```text
examples/
├── 01_llm_api/
├── 02_prompt/
├── 03_structured_output/
├── 04_rag/
├── 05_tool_calling/
├── 06_agent/
├── 07_langgraph/
└── 08_mcp/
```

这些代码不追求复杂，重点是：

> 学一个概念 → 写一个最小 Demo → 跑通 → 理解原理。

---

## 完整项目

### 1. Enterprise Knowledge Agent

计划实现一个面向企业内部知识库的 Agent。

核心能力：

* 文档解析
* 文本切分
* Embedding
* 向量检索
* RAG
* 多轮对话
* Tool Calling
* Agent
* 权限控制
* 引用来源
* 基础评测

目录：

```text
projects/knowledge-agent/
```

---

### 2. AI Scheduler / O&M Agent

计划结合实际 Java 调度系统经验，开发一个 AI 调度 / 运维 Agent。

目标场景包括：

* 调度任务异常分析
* 日志分析
* 任务失败原因定位
* SQL / Shell 分析
* 任务依赖分析
* 调度状态查询
* 运维工具调用
* 故障处理建议
* 自动生成故障分析报告

目录：

```text
projects/scheduler-agent/
```

---

## Environment

Python 建议使用 Python 3.11+。

创建虚拟环境：

```bash
python -m venv .venv
```

激活：

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

## Configuration

复制环境变量模板：

```bash
cp .env.example .env
```

然后修改 `.env`：

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=your-model
```

不要将 `.env` 提交到 Git。

---

## Run

运行示例：

```bash
python examples/01_llm_api/main.py
```

运行 Agent：

```bash
python scripts/run_agent.py
```

---

## Development

每学习一个新的 Agent 技术，优先按照以下方式实践：

```text
1. 学习概念
      ↓
2. 编写最小 Demo
      ↓
3. 实际运行
      ↓
4. 修改代码验证理解
      ↓
5. 记录学习笔记
      ↓
6. 提炼成可复用代码
      ↓
7. 最终进入完整项目
```

---

## Progress

### LLM 基础

* [x] LLM API
* [x] Prompt
* [ ] Structured Output

### RAG

* [ ] Embedding
* [ ] Document Loading
* [ ] Chunking
* [ ] Vector Database
* [ ] Retrieval
* [ ] RAG Pipeline

### Agent

* [ ] Tool Calling
* [ ] Agent
* [ ] Memory
* [ ] LangGraph
* [ ] MCP

### AI Engineering

* [ ] Evaluation
* [ ] Observability
* [ ] Error Handling
* [ ] Agent Workflow
* [ ] Deployment

### Projects

* [ ] Enterprise Knowledge Agent
* [ ] AI Scheduler / O&M Agent

---

## Philosophy

这个项目不是为了堆砌框架，而是为了理解：

> LLM 能做什么
> Agent 为什么需要 Tool
> RAG 解决什么问题
> Workflow 和 Agent 有什么区别
> 如何把 AI 能力真正接入业务系统

最终希望具备从：

```text
Java Backend
      ↓
AI Application Developer
      ↓
Agent Developer
```

的工程能力迁移。

## Commit 规范
1. `feat`：新增功能
2. `fix`：修复问题
3. `refactor`：重构
4. `docs`：文档
5. `test`：测试
6. `chore`：工程配置
