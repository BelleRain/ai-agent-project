# Java 日志分析器

## 功能

- 分析 Java 错误日志，识别异常类型及可能的故障原因。
- 返回结构化故障分析结果，包括故障原因、解决建议、置信度等信息。
- 提供 FastAPI 接口，支持通过 HTTP 请求提交日志并获取分析结果。
- 对请求参数进行校验，限制日志内容长度，减少无效请求。
- 对模型调用异常、结构化输出异常等进行统一处理。
- 支持通过大模型 API 分析日志，为后续构建调度系统运维 Agent 提供基础能力。

## 技术栈

- **Python**：项目开发语言。
- **FastAPI**：构建 HTTP API 服务。
- **Pydantic**：请求参数校验、响应数据建模及结构化输出校验。
- **OpenAI-compatible API**：通过兼容 OpenAI 接口规范的大模型服务进行日志分析。
- **Uvicorn**：运行 FastAPI 应用。
- **Pytest**：编写和运行自动化测试。

## 启动方式

### 1. 创建并激活虚拟环境

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

根据项目实际配置，设置大模型 API 密钥、API 地址和模型名称。

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE_URL="your-url"
export MODEL_NAME="your-model-name"
```

请根据实际使用的模型服务和项目配置修改环境变量名称及对应值，不要将真实 API 密钥提交到 Git 仓库。

### 4. 启动服务

```bash
uvicorn app.main:app --reload
```

启动后，可通过以下地址访问服务：

- API 服务地址：`http://127.0.0.1:8000`
- Swagger 接口文档：`http://127.0.0.1:8000/docs`
- ReDoc 接口文档：`http://127.0.0.1:8000/redoc`

**注意：** `app.main:app` 表示从 `app/main.py` 模块中导入名为 `app` 的 FastAPI 应用实例。如果项目实际使用的是 `src/log_analyzer/api.py` 中的 `app`，则应使用与当前项目目录结构一致的启动命令，例如：

```bash
uvicorn log_analyzer.api:app --app-dir src --reload
```

## 接口

### 1. 分析 Java 错误日志

- **请求方式：** `POST`
- **请求路径：** `/api/v1/logs/analyze`
- **请求类型：** `application/json`
- **功能说明：** 接收 Java 错误日志，调用大模型进行分析，并返回结构化故障分析结果。

请求示例：

```json
{
  "log_text": "HikariPool-1 - Exception during pool initialization"
}
```

响应示例（具体字段以项目实际的响应模型为准）：

```json
{
  "error_type": "DatabaseConnectionError",
  "root_cause": "数据库连接池初始化失败，可能与数据库连接配置或网络连接有关",
  "solution": "检查数据库地址、端口、账号密码及网络连通性",
  "confidence": 0.85
}
```

### 2. 健康检查

- **请求方式：** `GET`
- **请求路径：** `/health`
- **功能说明：** 检查 API 服务是否正常运行。

请求示例：

```bash
curl http://127.0.0.1:8000/health
```

响应示例（以实际实现为准）：

```json
{
  "status": "ok"
}
```
