# Day 10：JSON Mode、结构化输出与异常处理——今日验收标准

## 一、核心知识点

### 1. 理解 JSON Mode

- [ ] 能够解释不设置 `response_format`、使用 `json_object` 和使用 `json_schema` 的区别。
- [ ] 理解 JSON Mode 用于约束输出为合法 JSON，但不能保证字段齐全、字段类型正确。
- [ ] 理解 JSON Schema 在受支持的模型和 API 中，可以进一步约束输出结构。
- [ ] 知道当前使用的 DeepSeek 接口不支持本次尝试的 `parse(response_format=ErrorAnalysis)` 调用方式。

### 2. 理解 JSON 解析与 Pydantic 校验

- [ ] 能够解释 `json.loads(content)` 的作用：将合法 JSON 字符串解析为 Python 数据。
- [ ] 知道 JSON 格式不合法时，`json.loads()` 会抛出 `json.JSONDecodeError`。
- [ ] 能够解释 `ErrorAnalysis.model_validate(data)` 的作用：根据 Pydantic 模型校验数据，并创建模型对象。
- [ ] 知道 JSON 解析成功不代表数据一定符合 `ErrorAnalysis` 的定义。
- [ ] 理解 `str` 与 `Literal["low", "medium", "high"]` 的区别：后者限制字段只能取指定值。

## 二、代码实践

### 1. Prompt 模板与参数传递

- [ ] 能够解释函数实参与形参的关系。
- [ ] 能够解释为什么调用 `analyze_log(log)` 不代表日志一定会进入 API 请求。
- [ ] 能够使用 `USER_PROMPT_TEMPLATE.format(log_text=log_text)` 将日志填入 Prompt 模板。
- [ ] 能够确认发送给 API 的用户消息中包含实际日志内容。

### 2. 结构化结果校验

- [ ] 能够在 `ErrorAnalysis` 中定义 `error_type`、`possible_causes`、`suggestions` 和 `confidence` 字段。
- [ ] 能够通过 `model_validate()` 校验合法数据。
- [ ] 能够解释必填字段缺失或字段类型不匹配时为什么会校验失败。
- [ ] 能够使用 `Literal` 限制 `confidence` 的合法取值，并验证非法值会触发 `ValidationError`。

### 3. 异常处理与失败分支

- [ ] 知道模型可能返回拒答、空内容或非预期格式。
- [ ] 能够解释 `message.parsed` 为 `None` 时直接访问其属性可能引发的问题，并知道当前 JSON Mode 实现应检查 `message.content`。
- [ ] 能够识别 JSON 解析失败与 Pydantic 校验失败的区别。
- [ ] 能够使用 `try/except` 捕获预期异常，并向用户显示清晰的失败提示。
- [ ] 理解实际工程中还需要考虑 API 调用失败、超时等异常。

## 三、结合调度系统的应用理解

### 问题 1：结构化输出为什么适用于调度系统的任务日志分析和故障诊断？

**答案：**

调度系统的任务日志分析需要输出明确的错误类型、可能原因和解决建议。如果模型只返回一段自然语言，程序很难稳定地提取各项信息。

通过 JSON Mode 要求模型返回 JSON，再使用 Pydantic 校验字段和类型，可以将模型的分析结果转换为程序能够处理的 `ErrorAnalysis` 对象，方便后续展示、保存和进一步处理。

### 问题 2：为什么不能直接信任模型返回的结果，必须经过程序校验？

**答案：**

模型可能返回格式错误、缺少必填字段或类型不正确的数据。即使 JSON 解析成功，也不代表数据符合业务要求。

通过 `json.loads()` 解析 JSON，再使用 `ErrorAnalysis.model_validate()` 校验数据结构，可以尽早发现异常，避免不合格的数据进入后续业务流程。

不过，Pydantic 只能检查数据是否符合模型定义，不能保证模型给出的故障原因和解决建议在业务上一定正确。因此，故障诊断还需要结合日志证据和实际系统状态进行判断。

### 问题 3：如何设计基本的失败提示，避免将未经校验的诊断结果直接交给用户？

**答案：**

程序应区分不同的失败情况，并向用户提供清晰、可理解的提示。

- 模型返回空内容：提示“未获取到有效的分析结果，请稍后重试”。
- JSON 解析失败：提示“分析结果格式异常，请稍后重试”。
- Pydantic 校验失败：提示“分析结果不符合预期，暂时无法提供诊断建议”。
- API 调用失败或超时：提示“分析服务暂时不可用，请稍后重试”。

同时，应在服务端记录必要的异常类型和诊断信息，供开发人员排查。只有通过必要校验的结果才能进入正常业务流程，不能把未经校验的内容当作可靠诊断结论。

## 四、今日最终验收问题及参考答案

### 问题 1：JSON Mode 为什么不能代替 Pydantic 校验？

**答案：**

JSON Mode 主要要求模型输出合法 JSON，但不保证字段齐全、字段类型正确或字段值符合业务要求。

Pydantic 可以根据 `ErrorAnalysis` 的定义检查必填字段、数据类型和约束条件。因此，JSON Mode 负责约束输出格式，Pydantic 负责在程序端校验数据结构，两者不能互相替代。

### 问题 2：`json.loads()` 与 `model_validate()` 分别解决什么问题？

**答案：**

`json.loads(content)` 将 JSON 字符串解析为 Python 数据。如果字符串不是合法 JSON，通常会抛出 `json.JSONDecodeError`。

`ErrorAnalysis.model_validate(data)` 则根据 Pydantic 模型校验解析后的数据，并在校验通过后创建 `ErrorAnalysis` 对象。如果必填字段缺失或字段类型不符合要求，会抛出 `ValidationError`。

因此，前者解决“能不能解析 JSON”，后者解决“数据是否符合模型定义”。

### 问题 3：为什么 Prompt 已经要求模型返回 JSON，仍然建议设置 `response_format`？

**答案：**

Prompt 是自然语言指示，模型不一定严格遵守；`response_format={"type": "json_object"}` 则通过 API 参数明确要求输出 JSON 格式。

两者结合可以减少非 JSON 输出的情况，但 JSON Mode 仍不能保证返回结果符合业务模型，所以还需要 Pydantic 校验。

### 问题 4：为什么函数已经接收到 `log_text`，API 仍可能没有收到实际日志？

**答案：**

调用 `analyze_log(log)` 时，实参 `log` 已经传递给形参 `log_text`。但函数接收到参数，不代表会自动把它发送给 API。

如果请求中的 `content` 只使用 `USER_PROMPT_TEMPLATE`，没有将 `log_text` 填入模板，API 就收不到实际日志。

可以使用以下代码：

```python
{
    "role": "user",
    "content": USER_PROMPT_TEMPLATE.format(
        log_text=log_text
    ),
}
```

这样才能将日志内容填入 Prompt 并发送给模型。

### 问题 5：如果模型返回空内容、非法 JSON 或缺少必填字段，程序应该如何处理？

**答案：**

程序应先检查返回内容是否为空，再使用 `json.loads()` 解析 JSON，最后通过 `ErrorAnalysis.model_validate()` 校验数据。

- 空内容：返回明确的失败提示。
- 非法 JSON：捕获 `JSONDecodeError`。
- 字段缺失或类型错误：捕获 `ValidationError`。
- API 调用失败或超时：根据具体异常进行处理，并向用户返回友好的提示。

不应将解析失败或校验失败的结果直接交给后续业务流程。对于真实拒答，还应根据当前 API 的实际响应格式进行识别，不能仅凭空内容判断。

### 问题 6：当前 DeepSeek 接口不支持本次 Structured Outputs 调用方式时，如何继续完成日志分析器？

**答案：**

可以使用当前接口支持的 JSON Mode，并结合 Pydantic 完成基本的结构化输出处理：

1. 在 Prompt 中明确要求模型返回 JSON，并说明需要的字段。
2. 设置 `response_format={"type": "json_object"}`。
3. 使用 `json.loads()` 将返回内容解析为 Python 数据。
4. 使用 `ErrorAnalysis.model_validate()` 校验字段和类型。
5. 对空内容、JSON 解析失败、数据校验失败和 API 调用失败进行异常处理。

## 五、完成标准

- [ ] 能够用自己的话回答上述核心问题，而不是只背诵定义。
- [ ] 当前日志分析器能够将实际日志传入 API，并解析、校验正常返回结果。
- [ ] 能够处理至少空内容、JSON 解析失败和 Pydantic 校验失败这几种情况。
- [ ] 能够说明本次未实际验证的 Structured Outputs 实验结论及其适用前提。

**今日学习原则：** 以理解和实际应用为验收依据，不以是否听完推荐课程作为唯一标准。对于当前接口不支持的实验，理解原理、记录限制即可，不必为了完成实验而额外更换模型或付费。


