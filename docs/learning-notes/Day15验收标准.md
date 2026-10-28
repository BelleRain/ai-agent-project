# Day 15｜Prompt 版本管理 + 配置切换实验：今日验收标准

> 学习主题：Prompt 版本管理、配置切换、A/B 对比实验  
> 学习日期：2026-09-15  
> 学习阶段：LLM API / Python / Prompt / Structured Output  
> 核心目标：让 Prompt 从写死在业务代码中的文本，升级为可切换、可比较、可追踪的配置。

---

## 一、代码实践验收

### 1. Prompt 版本拆分

- [x] 创建独立的 Prompt 版本文件 `v1.py`、`v2.py`。
- [x] 在 `PROMPT_REGISTRY` 中注册不同版本的 Prompt。
- [x] 理解 `PROMPT_REGISTRY["v1"]` 与 `PROMPT_REGISTRY["v2"]` 的作用。

**验收要求：**

能够说明 Prompt 注册表的作用：集中管理不同版本的 Prompt，使业务代码不必直接写死提示词，并为后续版本切换和效果比较提供基础。

### 2. Prompt 配置切换

- [x] 在 `.env` 中增加 `PROMPT_VERSION` 配置。
- [x] 在 `config.py` 中读取 `prompt_version`。
- [x] 在 Service 层根据配置选择对应版本的 Prompt。

**验收要求：**

能够通过修改 `PROMPT_VERSION=v1` 或 `PROMPT_VERSION=v2` 选择不同的 Prompt，而不必直接修改业务代码中的提示词。

注意：修改环境变量后，如果应用只在启动时加载配置，需要重启服务才能确保使用新配置。

### 3. Prompt A/B 对比实验

- [x] 使用同一条日志分别测试 V1、V2。
- [x] 观察两种 Prompt 对模型输出的影响。
- [x] 打印并比较 V1、V2 的 Prompt 内容。

测试日志：

```text
HikariPool-1 - Exception during pool initialization
```

本次实验结果：

| 对比项 | V1 | V2 |
|---|---|---|
| 接口结果 | `STRUCTURED_OUTPUT_ERROR` | HTTP 200 |
| 结构化输出 | 未成功返回 | 成功返回 |
| 错误类型 | 无可用结果 | HikariCP 连接池初始化失败 |
| 置信度 | 无可用结果 | `low` |
| 证据引用 | 无可用结果 | 引用了原始日志 |

**实验结论：**

本次测试中，V1 未能成功返回结构化结果，V2 成功返回了分析结果。V2 增加了更多输出约束，可能有助于改善结果质量，但由于每个版本只测试了一次，暂时不能认定 V2 一定优于 V1，也不能确定 V1 失败的具体原因。

### 4. 记录 Prompt 版本

- [x] 在 `ErrorAnalysis` 中增加 `prompt_version` 字段。
- [x] 在解析模型返回内容后，由程序写入当前 Prompt 版本。
- [x] 在接口返回的 `data` 中看到 `"prompt_version": "v2"`。

示例：

```python
data = json.loads(content)
data["prompt_version"] = settings.prompt_version

return ErrorAnalysis.model_validate(data)
```

**验收要求：**

能够解释为什么 `prompt_version` 应由应用程序写入，而不是完全依赖模型生成。

### 5. 理解统一 API 响应

- [x] 能够区分内层 `data` 和外层响应字段。
- [x] 能够初步定位 `warnings` 等外层字段的来源。

示例：

```json
{
  "success": true,
  "data": {
    "error_type": "HikariCP连接池初始化失败",
    "prompt_version": "v2"
  },
  "message": "分析成功",
  "warnings": []
}
```

**验收要求：**

能够理解 `data` 是日志分析业务结果，而 `success`、`message`、`warnings` 属于统一 API 响应结构。具体字段的来源应通过检查 `ApiResponse` 模型、接口返回代码及相关处理逻辑确认。

---

## 二、核心知识验收

### 问题 1：为什么 Prompt 需要版本管理？

**参考答案：**

Prompt 会直接影响大模型的分析行为和输出结果。随着业务需求变化，我们可能需要调整角色定义、分析规则、证据要求和输出约束。

如果 Prompt 直接写在业务代码中，每次调整都可能需要修改代码，增加维护和回归测试的成本。

通过 Prompt 版本管理，可以将不同版本独立保存，并通过配置切换版本，比较修改前后的效果，出现问题时也可以切回之前的版本。

因此，Prompt 版本管理有助于提高 AI 应用的可维护性、可测试性和可追踪性。

### 问题 2：为什么 A/B 测试必须固定输入？

**参考答案：**

A/B 测试的目的是比较不同 Prompt 对模型输出的影响。

如果测试 V1 和 V2 时使用不同的日志，那么输出差异可能来自输入内容，也可能来自 Prompt 本身，无法判断真正的影响因素。

因此，应当固定测试输入，只改变 Prompt 版本，并尽量保持模型名称、模型参数和其他测试条件一致。

这样才能更合理地比较两个版本在错误识别、证据引用、原因分析和建议可执行性等方面的差异。

### 问题 3：Prompt V2 比 V1 增加了哪些约束？

**参考答案：**

V1 主要要求模型扮演 Java 后端故障分析工程师，并根据输入日志返回 JSON 结构化结果。

V2 在此基础上增加了以下约束：

1. **分析依据：** 只能基于输入日志进行推断。
2. **置信度：** 无法确认时应降低 `confidence`。
3. **证据要求：** 必须引用日志中的关键证据。
4. **字段要求：** 明确规定 `error_type`、`severity`、`confidence` 等字段的含义或取值范围。
5. **数量要求：** `possible_causes` 至少包含 2 条，`suggestions` 至少包含 2 条，`evidence` 至少包含 1 条。
6. **证据结构：** `evidence` 中包含 `log_fragment` 和 `explanation` 两个字段。
7. **原文引用：** `evidence.log_fragment` 必须引用输入日志中的原文或关键片段。
8. **输出格式：** 不输出 Markdown 或额外解释。

这些约束让任务要求更明确，但最终效果仍需要通过实际测试验证。

### 问题 4：为什么 Structured Output 不能替代 Prompt？

**参考答案：**

Structured Output 与 Prompt 解决的是不同的问题。

Structured Output 主要约束模型输出的数据结构，例如字段名称、字段类型、枚举值等，便于程序解析和后续处理。

Prompt 主要规定任务目标、分析依据、行为要求和输出内容，例如要求模型基于日志推断原因、引用关键证据，以及在信息不足时降低置信度。

例如，Schema 可以要求 `confidence` 是字符串或枚举值，但仅靠字段类型无法保证模型在缺乏证据时选择 `low`。

因此，Prompt 负责指导模型如何完成任务，Structured Output 负责约束输出结构。对于重要的业务规则，还需要通过 Pydantic 校验和业务逻辑进一步验证。

### 问题 5：线上排查时，为什么要记录 `model_name` 和 `prompt_version`？

**参考答案：**

模型名称和 Prompt 版本都是影响模型输出的重要因素。

当线上出现分析结果不准确、结构不符合预期或不同时间输出差异较大时，如果没有记录这些信息，就难以还原当时的运行环境。

记录 `model_name` 和 `prompt_version`，可以帮助开发人员：

1. 确认当时使用的是哪个模型和哪版 Prompt。
2. 比较不同模型或 Prompt 版本的输出差异。
3. 复现问题并开展回归测试。
4. 判断问题是否与模型切换、Prompt 修改或配置变更有关。
5. 必要时回滚到已验证的版本。

实际工程中，还可以记录模型参数、Schema 版本、请求 ID、输入摘要和调用时间等信息，以便更完整地追踪问题。

---

## 三、今日完成情况

- [x] 完成 Prompt V1、V2 的独立管理。
- [x] 完成通过 `.env` 切换 Prompt 版本。
- [x] 完成同一条日志的 V1、V2 初步对比。
- [x] 打印并分析两个版本的约束差异。
- [x] 为 `ErrorAnalysis` 增加 `prompt_version`。
- [x] 将当前 Prompt 版本写入解析后的业务数据。
- [x] 理解 `warnings` 等外层 API 响应字段与 `ErrorAnalysis` 的区别。
- [x] 完成 5 个核心知识问题的复盘。

---

## 四、今日总结

今天完成了从静态 Prompt 到可配置 Prompt 版本管理的初步升级。

通过 Prompt 注册表和环境变量，日志分析器可以选择不同版本的 Prompt；通过固定输入开展对比，可以初步观察不同版本对模型输出的影响；通过在结果中记录 `prompt_version`，可以为后续的问题复现和效果追踪提供依据。

需要注意，本次 V1、V2 各测试一次，只能形成初步观察，不能证明 V2 的整体效果一定更好。后续还需要通过多条固定测试日志、重复测试和明确的评价指标来验证。

**今日核心收获：**

Prompt 不只是给模型的一段文本，它也是 AI 应用中需要管理、测试、追踪和迭代的重要配置。

这项能力将成为后续开发企业知识库 Agent 和调度运维 Agent 的基础。
