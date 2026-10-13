## Day 9｜今日验收标准：把 Prompt、模型参数和输出校验配置化

### 一、代码结构验收

- [ ] 将公共配置放入 `src/agent/config.py`。
- [ ] 将日志分析相关代码放入 `src/log_analyzer/`。
- [ ] 将 `ErrorAnalysis` 放入 `models.py`。
- [ ] 将日志分析 Prompt 放入 `prompts.py`。
- [ ] 将结果校验和评分逻辑放入 `prompt_eval.py`。
- [ ] 正确使用 Python 包导入方式，不再出现 `ModuleNotFoundError`。

### 二、配置管理验收

- [ ] 使用 `.env` 管理 API 密钥、接口地址、模型名称等配置。
- [ ] 使用 `config.py` 统一读取配置。
- [ ] 能通过修改 `TEMPERATURE` 调整模型调用参数。
- [ ] 能通过修改 `MODEL_NAME` 切换可用模型。
- [ ] 删除 `TEMPERATURE` 和 `MAX_TOKENS` 后，程序能够使用默认值。

### 三、Prompt 与结果校验验收

- [ ] 将 `SYSTEM_PROMPT` 和 `USER_PROMPT_TEMPLATE` 独立放入 `prompts.py`。
- [ ] 能够切换不同的 Prompt 模板，而不需要修改日志分析的核心业务逻辑。
- [ ] 能够使用 Pydantic 的 `ErrorAnalysis` 校验模型返回的数据结构。
- [ ] 能够调用 `validate_analysis()` 检查结果，并使用 `score_analysis()` 计算评分。

### 四、运行验收

- [ ] 在项目根目录执行 `python -m pip install -e .`，确保项目包可以正常导入。
- [ ] 能够运行日志分析器，输入错误日志并输出错误类型、可能原因和解决建议。
- [ ] 能够运行 `python -m pytest tests/ -v`，执行测试并查看测试结果。
- [ ] 明确区分真实模型调用与模拟 API 响应的测试方式。

### 五、原理理解验收

- [ ] 能够解释为什么 Prompt 和模型参数应该配置化。
- [ ] 能够解释 `src/agent/` 与 `src/log_analyzer/` 的职责区别。
- [ ] 能够解释 `from .models import ErrorAnalysis` 的含义。
- [ ] 能够说明合法 JSON 不代表数据一定符合 `ErrorAnalysis` 的字段和类型要求。

### 六、今日总结

用自己的话回答以下问题：

1. 为什么修改模型名称时，不应该修改 `log_analyzer.py` 的核心业务逻辑？
2. 为什么日志分析专用的 `prompts.py` 和 `models.py` 放在 `log_analyzer/` 中，而不是全部放在公共目录？
3. `python -m pytest tests/ -v` 的作用是什么？

### 七、完成要求

- [ ] 完成代码整理与运行验证。
- [ ] 能够独立解释今天的目录结构、配置管理和模块导入方式。
- [ ] 不要求今天引入 LangChain、RAG 或其他新框架。

**今日核心目标：让日志分析器从单文件脚本逐步演进为结构清晰、配置可调、模块可复用的小型 AI 应用。**