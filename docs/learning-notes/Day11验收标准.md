# Day11｜Pydantic Schema 设计验收标准

## 一、今日学习目标

将日志分析器中的 `ErrorAnalysis` 从简单字段集合升级为更接近 Java 后端 DTO 的结构化对象，掌握字段约束、嵌套模型以及业务校验的基本方法。

核心目标：

- 理解 `Literal`、`Field` 和嵌套 `BaseModel` 的作用。
- 能够使用 Pydantic 定义更严格的 Schema。
- 能够通过 Structured Output 获取结构化分析结果。
- 能够区分结构校验与业务校验。
- 能够识别低置信度、高严重程度等需要人工关注的情况。

## 二、核心知识验收

### 1. Literal 与枚举约束

- [ ] 能解释 `Literal["low", "medium", "high"]` 的作用。
- [ ] 能说明 `Literal` 与普通 `str` 的区别。
- [ ] 能理解固定取值约束可以减少非法字段值。
- [ ] 能结合 `severity` 和 `confidence` 说明使用场景。

**验收问题：**

为什么 `severity: str` 不如 `severity: Literal["low", "medium", "high"]` 严格？

### 2. Pydantic 嵌套模型

- [ ] 能定义 `Evidence(BaseModel)`。
- [ ] 能在 `ErrorAnalysis` 中使用 `list[Evidence]`。
- [ ] 能理解嵌套对象与普通字符串列表的区别。
- [ ] 能解释为什么证据需要同时包含 `log_fragment` 和 `explanation`。

**验收问题：**

为什么将证据设计成独立的 `Evidence` 模型，比直接使用 `list[str]` 更适合后续业务处理？

### 3. Field 字段描述与约束

- [ ] 能使用 `Field(description=...)` 描述字段含义。
- [ ] 能使用 `min_length=1` 限制列表不能为空。
- [ ] 能区分字段描述与实际校验约束。
- [ ] 能理解 Schema 约束不等于所有业务规则都已得到验证。

**验收问题：**

`description` 和 `min_length=1` 分别起什么作用？

### 4. Structured Output

- [ ] 能使用 `client.beta.chat.completions.parse()` 调用模型。
- [ ] 能将 `ErrorAnalysis` 传入 `response_format`。
- [ ] 能通过 `message.parsed` 获取 Pydantic 对象。
- [ ] 能处理模型拒答和未获取到结构化结果的情况。
- [ ] 能说明严格 Schema 与普通 JSON 输出的区别。

**验收问题：**

为什么使用 `response_format=ErrorAnalysis` 后，不需要再手动调用 `json.loads()` 解析模型响应？

## 三、代码实操验收

### 1. 完成 Schema 改造

- [ ] `models.py` 中包含 `Evidence` 和 `ErrorAnalysis`。
- [ ] `ErrorAnalysis` 包含 `error_type`、`severity`、`confidence`、`possible_causes`、`suggestions` 和 `evidence`。
- [ ] `severity` 和 `confidence` 只能取 `low`、`medium`、`high`。
- [ ] `possible_causes`、`suggestions` 和 `evidence` 均具有非空列表约束。
- [ ] `evidence` 中的每个元素都符合 `Evidence` 模型结构。

### 2. 完成 Prompt 修改

- [ ] 明确要求模型保守分析，只根据日志推断。
- [ ] 明确规定 `severity` 和 `confidence` 的合法取值。
- [ ] 要求 `possible_causes` 至少返回 2 条。
- [ ] 要求 `suggestions` 至少返回 2 条。
- [ ] 要求 `evidence` 至少返回 1 个对象。
- [ ] 要求 `evidence.log_fragment` 引用输入日志中的真实片段。
- [ ] 要求证据不足时降低 `confidence`。

### 3. 测试不同日志

分别使用以下日志执行分析：

```text
HikariPool-1 - Exception during pool initialization
```

```text
Communications link failure during query execution
```

```text
NettyRemotingServer bind fail, address already in use
```

检查以下内容：

- [ ] 三条日志均能得到结构化结果，或能明确识别失败原因。
- [ ] `severity` 符合日志所能支持的判断。
- [ ] `confidence` 与证据充分程度相符。
- [ ] `evidence.log_fragment` 确实来自输入日志。
- [ ] `possible_causes` 与日志存在合理关联。
- [ ] `suggestions` 具有可执行性，而非泛泛而谈。

注意：日志片段本身往往不足以确认真实根因，因此不要求三条日志必须对应固定的严重程度；重点是判断有依据、置信度合理。

### 4. 验证 Schema 错误

- [ ] 将 Prompt 中的严重程度要求故意修改为 `critical`。
- [ ] 保留 `Literal["low", "medium", "high"]`。
- [ ] 观察模型或 API 是否拒绝不兼容的 Schema、返回错误，或产生解析失败。
- [ ] 能解释为什么不能只依赖 Prompt 保证字段取值合法。

**验收要求：** 能够说明，具体失败发生在服务端请求校验、模型生成还是客户端解析阶段，需要结合实际异常信息判断；不要求每次实验都产生同一种错误。

## 四、业务校验验收

### 1. 实现 `validate_business_rules()`

- [ ] 在 `prompt_eval.py` 中新增业务校验函数。
- [ ] 当 `confidence == "low"` 且 `severity == "high"` 时，生成需要人工确认的提醒。
- [ ] 检查证据内容是否为空或只有空白字符。
- [ ] 返回 `list[str]`，而不是直接终止程序。
- [ ] 能在 CLI 中展示业务校验提醒。

### 2. 理解结构校验与业务校验

- [ ] 能解释 Pydantic 负责字段类型、必填性和声明式约束。
- [ ] 能解释业务函数负责跨字段关系和业务规则。
- [ ] 能举例说明结构合法的结果仍可能不合理。
- [ ] 能理解模型给出的 `confidence` 是模型的自我评估标签，不是经过校准的真实概率。

**验收问题：**

为什么一个符合 `ErrorAnalysis` Schema 的结果，仍然可能需要人工复核？

## 五、结合 Java 后端的应用理解

- [ ] 能将 `BaseModel` 类比为 Java DTO。
- [ ] 能将 `Literal` 类比为受固定取值约束的枚举字段。
- [ ] 能将 `Evidence` 类比为 DTO 中的嵌套对象。
- [ ] 能区分 DTO 参数校验与业务服务中的规则判断。
- [ ] 能说明结构化日志分析结果如何交给调度系统进一步处理。

**验收要求：**

能够描述以下流程：

```text
调度系统获取异常日志
        ↓
调用日志分析器
        ↓
大模型返回结构化结果
        ↓
Pydantic 校验数据结构
        ↓
业务规则检查
        ↓
输出分析结果与风险提醒
        ↓
上层系统决定是否告警或人工复核
```

## 六、今日最终验收问题

### 问题 1：Literal 和普通 str 的区别是什么？

回答应包含：

- `str` 允许任意字符串。
- `Literal` 将字段限制为指定的有限取值。
- 该约束有助于减少非法字段值，并让 Schema 更明确。

**答：** `str` 允许字段接收任意字符串，而 `Literal["low", "medium", "high"]` 将字段值限制在指定的三个选项中。例如，`severity` 使用 `str` 时可以接收 `"critical"`，使用 `Literal` 时则不允许该值通过正常的 Pydantic 校验。

在日志分析器中，使用 `Literal` 可以让 `severity` 和 `confidence` 的取值范围更加明确，减少非法字段值，使结构化输出更容易被后续业务代码处理。


### 问题 2：为什么要增加 evidence 字段？

回答应包含：

- 让分析结论具有可检查的日志依据。
- 将日志原文片段与解释分开保存。
- 方便后续人工复核、结果展示和业务处理。
- 证据存在不代表结论必然正确，仍需判断证据是否充分。

**答：** 增加 `evidence` 字段，是为了让模型的分析结论有可检查的日志依据，而不只是直接给出错误类型、可能原因和解决建议。通过嵌套的 `Evidence` 模型，可以分别保存 `log_fragment`（日志原文片段）和 `explanation`（该片段支持当前判断的原因）。

这样，后续系统或开发人员就可以检查分析依据，进行人工复核，并将证据用于结果展示和业务处理。但需要注意，证据存在并不意味着结论一定正确，还需要判断证据是否充分、解释是否合理。

### 问题 3：为什么 confidence 不能直接当成真实概率？

回答应包含：

- `low`、`medium`、`high` 是模型输出的置信度标签。
- 它们不等于经过统计校准的概率。
- 需要结合日志证据、历史表现或人工复核评估判断可靠性。

**答：** `confidence` 中的 `low`、`medium`、`high` 是模型生成的置信度标签，用于表达模型对当前判断的主观把握程度，并不等于经过统计校准的真实概率。例如，模型输出 `confidence="high"`，并不意味着该结论有 90% 或其他固定概率的正确率。

在日志分析器中，应该结合日志证据是否充分、历史分析结果的准确性以及人工复核情况评估结论的可靠性。如果要将置信度用于定量决策，还需要通过实际数据进行评估和校准。

### 问题 4：为什么 Schema 校验通过后还要做业务校验？

回答应包含：

- Schema 主要检查数据结构和声明式约束。
- Schema 无法自动保证所有字段之间的业务逻辑合理。
- 例如高严重程度与低置信度同时出现时，可以触发人工复核提醒。

**答：** Schema 校验主要检查数据结构、字段类型、必填性以及明确声明的约束，例如 `severity` 是否属于指定选项、`evidence` 是否为非空列表。但 Schema 校验通过，并不代表模型给出的结论在业务上一定合理。

例如，模型可能同时输出 `severity="high"` 和 `confidence="low"`。这两个值单独来看都符合 Schema，但结合业务场景，就意味着问题可能比较严重，而模型又缺乏充分把握，因此应该触发人工复核提醒。通过业务校验函数，可以检查这类跨字段关系及其他业务规则。


### 问题 5：为什么不能只依赖 Prompt 保证输出合法？

回答应包含：

- Prompt 是对模型行为的指引，不是可靠的程序级校验机制。
- Structured Output 和 Pydantic Schema 可以对输出结构及字段取值施加约束。
- 业务规则仍需在应用层独立检查。

**答：** Prompt 用于指导模型如何分析日志、选择字段值和组织结果，但它本质上是对模型行为的指引，不能单独作为可靠的程序级校验机制。即使明确要求 `severity` 只能输出 `low`、`medium` 或 `high`，也不能只依靠这段文字保证输出始终满足要求。

使用 Structured Output 配合 Pydantic Schema，可以对结构、字段类型和受支持的字段约束进行更严格的控制与校验，减少不符合要求的输出。但这仍然不能保证所有业务判断都正确，因此应用层还需要独立执行业务校验。通过这几层配合，日志分析器才能更可靠地处理模型结果。


## 七、今日学习总结

### 1. 今日掌握的核心知识

- **枚举约束：** 使用 `Literal` 限制字段的合法取值，让输出结构更加明确。
- **嵌套对象：** 使用 `Evidence` 描述证据片段和解释，使复杂结果具有清晰的层次。
- **字段描述与约束：** 使用 `Field` 为字段添加描述，并通过 `min_length` 等参数声明约束。
- **结构化输出：** 使用 `response_format=ErrorAnalysis` 获取符合指定模型结构的结果。
- **业务校验：** 在 Pydantic 校验之外，检查跨字段关系、证据质量以及需要人工复核的风险。

### 2. 今日最重要的理解

今天的重点不只是让大模型返回一份格式正确的 JSON，而是让日志分析结果更接近真实后端系统可以使用的 DTO。

整个过程可以概括为：

```text
Prompt 指导模型分析
        ↓
Structured Output 约束输出格式
        ↓
Pydantic 校验数据结构
        ↓
业务函数检查规则合理性
        ↓
输出分析结果与风险提醒
        ↓
交给上层系统处理
```

其中，结构合法不等于业务合理，业务合理也不等于结论绝对正确。对于缺乏充分证据的分析结果，仍然需要保守处理或人工复核。

### 3. 与 Java 后端开发的联系

这套设计与 Java 后端开发中的分层思想类似：

| Python / Pydantic | Java 后端中的近似概念 |
|---|---|
| `BaseModel` | DTO |
| `Literal` | 固定取值约束，类似枚举字段 |
| 嵌套 `BaseModel` | 嵌套 DTO |
| `Field` | 字段描述及部分校验元数据 |
| Pydantic 校验 | 数据绑定与参数校验 |
| `validate_business_rules()` | 业务规则校验 |

需要注意，这些是概念上的类比，并不是完全一一对应的实现。

## 八、今日最终通过标准

### 必须完成

- [ ] 完成 `models.py` 的 Schema 改造。
- [ ] 完成 `prompts.py` 的 Prompt 修改。
- [ ] 使用 `response_format=ErrorAnalysis` 获取结构化结果。
- [ ] 完成至少一条日志的端到端运行。
- [ ] 实现并调用 `validate_business_rules()`。
- [ ] 完成 `day11_schema_notes.md`，回答四个核心问题。

### 进阶完成

- [ ] 分析三条不同日志并比较输出质量。
- [ ] 完成一次 Schema 错误实验并记录真实异常。
- [ ] 测试低置信度与高严重程度同时出现的业务提醒。
- [ ] 检查证据片段是否真实来自输入日志。


**通过原则：** 不要求模型每次都给出完全一致的分析结论。重点是 Schema 设计合理、结果结构可验证、业务风险能被识别，并且你能解释每一层的职责。

今天先把 Pydantic Schema、Structured Output 和业务校验练扎实，暂不进入 Tool Calling。



