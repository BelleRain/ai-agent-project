# Day 7｜今日验收标准

## 一、功能验收

- [ ] **命令行单条日志分析**
  - 能通过 `--log` 参数传入日志。
  - 能调用 LLM 并输出错误类型、可能原因和解决建议。
  - 能输出质量评分和质量提醒。

- [ ] **文件批量分析**
  - 能通过 `--file sample_logs.txt` 读取日志文件。
  - 能自动过滤空行和首尾空白字符。
  - 能逐条分析日志，并输出每条日志的分析结果。
  - 单条日志分析失败时，能够继续处理后续日志。

- [ ] **模块职责划分**
  - `log_analyzer.py`：负责模型调用和结果解析。
  - `prompt_eval.py`：负责结果校验和质量评分。
  - `cli.py`：负责命令行参数解析、用户交互和结果输出。

## 二、知识验收

- [ ] 能说清楚 OpenAI API 从请求到获取模型响应的基本流程。
- [ ] 能区分 system prompt 和 user prompt，并结合日志分析器举例。
- [ ] 能区分 JSON 字符串、Python 字典和 Pydantic 对象。
- [ ] 能解释 `JSONDecodeError` 和 `ValidationError` 的区别。
- [ ] 能解释为什么 JSON 格式正确不代表业务结果可靠。
- [ ] 能说清楚质量评分与业务校验的区别。

## 三、异常处理验收

- [ ] 能识别 JSON 解析失败的情况。
- [ ] 能识别 Pydantic 字段缺失、字段类型不匹配等校验失败的情况。
- [ ] 能结合实际错误信息定位问题，而不是只通过修改代码尝试解决。
- [ ] 能区分 API 调用失败、JSON 解析失败、结构校验失败和业务校验失败。

## 四、实验与文档验收

- [ ] 完成 `week1_review.md`，回答 5 个复盘问题，每题 2～4 句话。
- [ ] 完成一次 Prompt 实验，对比宽松 Prompt 和严格 Prompt 的输出差异。
- [ ] 记录模型返回内容、字段完整性、Pydantic 校验结果和实验结论。

## 五、运行验收

至少执行以下命令并确认结果符合预期。

### 1. 单条日志分析

```bash
PYTHONPATH=src python examples/07_cli/cli.py \
  --log "HikariPool-1 - Exception during pool initialization"
```

### 2. 测试其他类型的日志

```bash
PYTHONPATH=src python examples/07_cli/cli.py \
  --log "No Feign Client for loadBalancing"
```

### 3. 文件批量分析

如果已经实现文件批量模式，执行：

```bash
PYTHONPATH=src python examples/07_cli/cli.py \
  --file examples/07_cli/sample_logs.txt
```

验收时确认：

- [ ] 命令能够正常执行。
- [ ] 输出结果的字段完整且符合预期。
- [ ] 中文能够正常显示。
- [ ] 异常能够被捕获并给出明确提示。
- [ ] 批量处理时，单条日志失败不会影响后续日志。

## 六、今日最终通过标准

满足以下条件，即可判定 Day 7 通过：

1. 单条日志能够通过命令行完成分析。
2. 文件批量模式能够逐条处理日志。
3. 能够区分 JSON 解析、Pydantic 校验和业务校验。
4. 完成第一周复盘文档和一次 Prompt 对比实验。
5. 能够独立解释日志分析器从接收输入到输出分析结果的完整流程。

## 七、今日核心目标

将前 6 天学习的 LLM API、Prompt、结构化输出和 Pydantic 校验整合成一个可运行、可检查、可维护的命令行小工具，为后续学习 RAG 打好基础。