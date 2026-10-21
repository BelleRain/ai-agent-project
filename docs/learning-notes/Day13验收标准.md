# Day 13｜今日学习验收标准：异常处理与 FastAPI 接口异常转换

## 一、今日学习目标

- [ ] 理解 Python 自定义异常类的作用及继承关系。
- [ ] 理解 `raise`、`try-except` 和 `raise ... from exc` 的用法。
- [ ] 能够区分模型调用异常、JSON 解析异常和字段校验异常。
- [ ] 理解多个 `except` 的匹配顺序，以及 `except Exception` 的捕获范围。
- [ ] 理解为什么在 `try` 代码块中主动抛出的 `StructuredOutputError` 会被最后的 `except Exception` 捕获。
- [ ] 能够在 FastAPI 中将业务异常转换为合适的 HTTP 状态码。
- [ ] 理解 `@app.post` 与 `@router.post` 的区别。

## 二、核心知识验收

### 问题 1：自定义异常类的作用是什么？

回答应包含：

- 自定义异常可以对不同类型的业务错误进行分类。
- 自定义异常可以继承 Python 内置的 `Exception` 或其他业务异常类。
- 自定义异常即使没有额外属性和方法，也可以通过 `pass` 定义。
- 继承关系示例：

```python
class LogAnalyzeError(Exception):
    pass

class LLMServiceError(LogAnalyzeError):
    pass

class StructuredOutputError(LogAnalyzeError):
    pass
```

- `LLMServiceError` 和 `StructuredOutputError` 都属于 `Exception` 的子类。

**答：**

自定义异常类的作用是**对不同类型的业务错误进行分类，便于在不同层级进行针对性处理**。

例如：

```python
class LogAnalyzeError(Exception):
    """日志分析业务异常"""
    pass

class LLMServiceError(LogAnalyzeError):
    """模型调用异常"""
    pass

class StructuredOutputError(LogAnalyzeError):
    """结构化输出异常"""
    pass
```

- `Exception` 是 Python 内置的普通异常基类。
- `LogAnalyzeError` 继承 `Exception`，表示日志分析业务异常。
- `LLMServiceError` 和 `StructuredOutputError` 继承 `LogAnalyzeError`，分别表示模型调用异常和结构化输出异常。
- `pass` 表示暂时不添加其他属性或方法，但类仍然可以被实例化、抛出和捕获。

继承关系如下：

```text
Exception
    └── LogAnalyzeError
          ├── LLMServiceError
          └── StructuredOutputError
```

因此，既可以单独捕获 `LLMServiceError`，也可以通过 `except LogAnalyzeError` 捕获它和其他日志分析业务异常。

对照 Java，类似于定义多个继承自 `RuntimeException` 的自定义异常类。

### 问题 2：`raise ... from exc` 有什么作用？

回答应包含：

- `raise` 用于主动抛出异常。
- `from exc` 用于明确指定当前异常的原始原因。
- 保留异常链有助于排查错误。
- 示例：

```python
try:
    data = json.loads(content)
except json.JSONDecodeError as exc:
    raise StructuredOutputError("模型返回的内容不是合法 JSON") from exc
```

**答：**

`raise` 用于主动抛出异常，`from exc` 用于明确指定当前异常的原始原因，保留异常之间的因果关系，方便排查问题。

例如：

```python
try:
    data = json.loads(content)
except json.JSONDecodeError as exc:
    raise StructuredOutputError(
        "模型返回的内容不是合法 JSON"
    ) from exc
```

执行过程：

1. `json.loads(content)` 解析失败，抛出 `JSONDecodeError`。
2. `except` 捕获该异常，并将其赋值给变量 `exc`。
3. `raise StructuredOutputError(...) from exc` 抛出新的业务异常。
4. Python 保留原始异常信息，便于查看错误原因和异常链。

这里有两个不同的异常：

- 原始异常：`JSONDecodeError`，说明 JSON 解析失败。
- 新异常：`StructuredOutputError`，说明模型输出不符合业务要求。

这样既能统一对外的异常类型，又能保留底层错误信息

### 问题 3：为什么空内容时主动抛出的 `StructuredOutputError` 会被最后的 `except Exception` 捕获？

回答应包含：

- 空内容检查发生在 `try` 代码块中。
- `StructuredOutputError` 继承自 `Exception`。
- 前面的 `except` 没有专门捕获 `StructuredOutputError`，因此最后的 `except Exception` 会匹配它。
- 如果希望原样抛出该异常，可以增加 `except StructuredOutputError: raise`。
- 更推荐将模型调用、JSON 解析和字段校验拆分到不同的 `try-except` 中，明确各阶段的异常边界。

**答：**

因为空内容检查发生在 `try` 代码块内部，而 `StructuredOutputError` 是 `Exception` 的子类。

例如：

```python
try:
    if not content or not content.strip():
        raise StructuredOutputError("模型未返回有效内容")

    data = json.loads(content)
    return ErrorAnalysis.model_validate(data)

except json.JSONDecodeError as exc:
    raise StructuredOutputError(
        "模型返回的内容不是合法 JSON"
    ) from exc

except ValidationError as exc:
    raise StructuredOutputError(
        "模型返回字段不符合要求"
    ) from exc

except Exception as exc:
    raise LLMServiceError("模型调用失败") from exc
```

当 `content` 为空时：

1. 主动抛出 `StructuredOutputError`。
2. Python 按顺序检查同一组 `except`。
3. 前两个处理器分别匹配 `JSONDecodeError` 和 `ValidationError`，都不匹配当前异常。
4. 最后一个 `except Exception` 匹配成功，因为 `StructuredOutputError` 继承自 `Exception`。
5. 原本的 `StructuredOutputError` 被包装成 `LLMServiceError`。

这会导致异常分类不准确：模型可能调用成功，只是没有返回有效内容，却被误判为模型调用失败。

如果希望原样抛出，可以增加：

```python
except StructuredOutputError:
    raise
```

将它放在最后的 `except Exception` 之前。

更推荐的方式是将模型调用、JSON 解析和字段校验拆分到不同的 `try-except` 中，明确各自的异常处理范围。

### 问题 4：为什么 JSON 解析异常处理器中抛出的 `StructuredOutputError` 不会被同一组最后的 `except Exception` 捕获？

回答应包含：

- `json.loads()` 抛出的 `JSONDecodeError` 由对应的 `except` 捕获。
- 处理器内部抛出的新异常不会被同一组后续 `except` 再次捕获。
- 如果存在外层的 `try-except`，外层处理器仍可能捕获该异常。

**答：**

例如：

```python
try:
    data = json.loads(content)

except json.JSONDecodeError as exc:
    raise StructuredOutputError(
        "模型返回的内容不是合法 JSON"
    ) from exc

except Exception as exc:
    raise LLMServiceError("模型调用失败") from exc
```

当 JSON 解析失败时：

1. `json.loads(content)` 抛出 `JSONDecodeError`。
2. Python 匹配第一个 `except`。
3. 第一个处理器主动抛出 `StructuredOutputError`。
4. Python 不会继续检查同一组中后面的 `except Exception`。

**核心区别在于异常发生的位置：**

- 空内容场景：`StructuredOutputError` 在 `try` 代码块中抛出，因此会被该组的 `except` 检查。
- JSON 解析场景：`StructuredOutputError` 在第一个 `except` 的处理器内部抛出，不会被同一组后续的处理器捕获。

但如果外层还有一个 `try-except`，外层的 `except Exception` 仍然可以捕获这个 `StructuredOutputError`。

### 问题 5：为什么不建议使用 `except Exception` 统一处理所有错误？

回答应包含：

- 它会捕获当前 `try` 代码块中绝大多数普通异常，包括自定义业务异常。
- 如果不区分异常类型，可能把输出格式错误误判成模型调用失败。
- 应优先捕获具体异常，例如 `json.JSONDecodeError`、Pydantic 的 `ValidationError`。
- 通用异常处理器应放在具体异常处理器之后，并控制好捕获范围。

**答：**

因为 `except Exception` 的捕获范围很广，会捕获当前 `try` 代码块中绝大多数普通异常，包括自定义业务异常。

例如：

```python
try:
    data = json.loads(content)
    return ErrorAnalysis.model_validate(data)

except Exception as exc:
    raise LLMServiceError("模型调用失败") from exc
```

这段代码的问题是：

- JSON 格式错误可能被误判为模型调用失败。
- Pydantic 字段校验错误可能被误判为模型调用失败。
- 代码中的其他普通错误也可能被错误归类。

更合理的做法是优先处理具体异常：

```python
try:
    data = json.loads(content)
except json.JSONDecodeError as exc:
    raise StructuredOutputError(
        "模型返回的内容不是合法 JSON"
    ) from exc

try:
    return ErrorAnalysis.model_validate(data)
except ValidationError as exc:
    raise StructuredOutputError(
        "模型返回字段不符合要求"
    ) from exc
```

模型 API 调用则单独处理：

```python
try:
    response = client.chat.completions.create(...)
except Exception as exc:
    raise LLMServiceError("模型调用失败") from exc
```

这里的 `except Exception` 仍然较宽泛。实际项目中，最好优先捕获模型 SDK 明确提供的 API 异常、连接异常或超时异常，再根据需要保留通用兜底处理。

原则是：**具体异常优先，通用异常兜底；每个 `try` 尽量只包围同一阶段的操作。*

### 问题 6：`HTTPException` 与 `Exception` 是什么关系？

回答应包含：

- FastAPI 的 `HTTPException` 继承自 Python 的 `Exception`。
- 在接口层可以使用 `HTTPException` 返回合适的 HTTP 状态码。
- 同一组 `except` 中，处理器内部抛出的 `HTTPException` 不会被后续的 `except Exception` 捕获。
- 外层的 `except Exception` 仍可能捕获内层抛出的 `HTTPException`。

示例：

```python
try:
    analyze_log()
except StructuredOutputError as exc:
    raise HTTPException(status_code=422, detail=str(exc))
except Exception as exc:
    raise HTTPException(status_code=500, detail="服务内部错误") from exc
```

**答：**

FastAPI 的 `HTTPException` 继承自 Python 的 `Exception`，因此它也属于普通异常体系。

例如：

```python
try:
    analyze_log()

except StructuredOutputError as exc:
    raise HTTPException(
        status_code=422,
        detail=str(exc)
    )

except Exception as exc:
    raise HTTPException(
        status_code=500,
        detail="服务内部错误"
    ) from exc
```

这里有两种情况：

### 情况一：`analyze_log()` 抛出 `StructuredOutputError`

- 匹配第一个 `except`。
- 抛出 HTTP 422 异常。
- 不会再检查同一组的第二个 `except Exception`。

### 情况二：`analyze_log()` 抛出其他普通异常

- 匹配第二个 `except Exception`。
- 抛出 HTTP 500 异常。

需要注意：如果在外层使用 `except Exception` 包围这段代码，那么内层处理器抛出的 `HTTPException` 仍可能被外层捕获。

常见 HTTP 状态码的含义：

| 状态码 | 含义 | 示例 |
|---|---|---|
| 200 | 请求成功 | 日志分析成功 |
| 422 | 请求或数据不符合要求 | 请求字段不符合约束，或业务输出无法满足约定 |
| 500 | 服务内部发生未预期错误 | 未处理的程序异常 |

补充：请求体字段缺失或不符合 FastAPI/Pydantic 请求模型的约束时，FastAPI 通常会自动返回 422。业务异常转换属于另一种使用场景。

### 问题 7：`@app.post` 与 `@router.post` 有什么区别？

回答应包含：

- `@app.post` 直接向 FastAPI 应用注册接口。
- `@router.post` 向 `APIRouter` 注册接口。
- 使用路由模块时，需要在应用中通过 `app.include_router(router)` 注册路由。
- 两者都是 FastAPI 支持的接口定义方式。

**答：**

两者都是 FastAPI 支持的路由注册方式，主要区别在于注册对象不同。

### 方式一：使用 `@app.post`

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/analyze")
def analyze_log_api():
    return {"message": "分析成功"}
```

- `app` 是 FastAPI 应用实例。
- `@app.post("/analyze")` 直接向应用注册 POST 接口。
- 适合接口数量较少、路由比较简单的应用。

### 方式二：使用 `@router.post`

在 `api.py` 中：

```python
from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
def analyze_log_api():
    return {"message": "分析成功"}
```

在应用入口中：

```python
from fastapi import FastAPI
from log_analyzer.api import router

app = FastAPI()

app.include_router(router)
```

- `APIRouter` 用于将相关接口组织成一个路由模块。
- `@router.post("/analyze")` 将接口注册到 `router`，此时还没有直接注册到 `app`。
- `app.include_router(router)` 将路由模块纳入 FastAPI 应用。

| 写法 | 注册对象 | 典型用途 |
|---|---|---|
| `@app.post` | FastAPI 应用实例 | 直接定义接口 |
| `@router.post` | `APIRouter` 实例 | 按模块组织接口 |

例如，日志分析项目以后可能增加日志分析、任务状态查询、故障诊断等多个接口，可以将它们按功能拆分为不同的路由模块。

注意：如果出现 `router` 未定义、导入路径错误或忘记调用 `app.include_router(router)` 等情况，接口可能无法正常注册或访问。这不代表 `@router.post` 不受 FastAPI 支持。

## 三、代码实战验收

### 任务 1：定义业务异常

在 `exceptions.py` 中定义以下异常：

- [ ] `LogAnalyzeError`
- [ ] `LLMServiceError`
- [ ] `StructuredOutputError`

验收要求：

- [ ] 三个类的继承关系正确。
- [ ] 每个类都有清晰的文档字符串。
- [ ] 能够通过 `raise` 主动抛出异常。

### 任务 2：完善日志分析器的异常处理

在日志分析器中实现以下异常分类：

| 场景 | 异常类型 |
|---|---|
| 模型 API 调用失败 | `LLMServiceError` |
| 模型返回空内容 | `StructuredOutputError` |
| 模型返回非法 JSON | `StructuredOutputError` |
| 模型返回字段不符合 Pydantic 模型要求 | `StructuredOutputError` |

验收要求：

- [ ] 使用 `json.loads()` 解析模型返回的 JSON。
- [ ] 使用 `ErrorAnalysis.model_validate(data)` 校验字段。
- [ ] 使用 `except json.JSONDecodeError` 捕获 JSON 解析异常。
- [ ] 使用 `except ValidationError` 捕获 Pydantic 字段校验异常。
- [ ] 不使用宽泛的 `except Exception` 直接代替所有具体异常处理。
- [ ] 模型调用异常不会错误地覆盖结构化输出异常。

### 任务 3：完善 FastAPI 接口异常转换

在 `api.py` 中实现业务异常到 HTTP 异常的转换。

验收要求：

- [ ] `StructuredOutputError` 转换为 HTTP 422。
- [ ] 未预期的普通异常转换为 HTTP 500。
- [ ] 异常处理器顺序正确。
- [ ] HTTP 响应中不向客户端暴露完整的内部堆栈或敏感信息。
- [ ] 能够通过接口请求验证返回的 HTTP 状态码。

## 四、测试验收

至少完成以下测试：

| 编号 | 测试场景 | 预期结果 |
|---|---|---|
| 1 | 模型返回空字符串 | 抛出 `StructuredOutputError` |
| 2 | 模型返回非法 JSON | 抛出 `StructuredOutputError` |
| 3 | 模型返回缺少必填字段的 JSON | 抛出 `StructuredOutputError` |
| 4 | 模型 API 调用发生异常 | 抛出 `LLMServiceError` |
| 5 | 结构化输出异常经过 FastAPI 接口 | HTTP 422 |
| 6 | 未预期的普通异常经过 FastAPI 接口 | HTTP 500 |

- [ ] 至少验证一次异常的原始原因，即 `raise ... from exc`。
- [ ] 至少验证一次 `except Exception` 对自定义异常的捕获行为。
- [ ] 确认修复后，异常类型与预期一致。

## 五、最终验收标准

满足以下条件，即视为今日学习通过：

- [ ] 能够不看资料解释核心知识验收中的 7 个问题。
- [ ] 能够独立编写三个自定义异常类。
- [ ] 能够正确区分模型调用、JSON 解析和字段校验异常。
- [ ] 能够解释同一组 `except` 与外层 `except` 的捕获区别。
- [ ] 能够完成 FastAPI 业务异常到 HTTP 状态码的转换。
- [ ] 能够运行至少 6 个测试场景，并验证实际结果。
- [ ] 将代码与测试结果提交到 `ai-agent-project` 项目中。

## 六、今日学习总结

请用自己的话回答以下问题：

1. 为什么不能简单地使用一个 `except Exception` 处理所有异常？
2. 为什么需要将 `LLMServiceError` 和 `StructuredOutputError` 区分开？
3. 在调度系统运维 Agent 中，如果模型调用成功，但返回的故障诊断结果缺少必需字段，应该归类为哪一种异常？为什么？
4. 为什么要在日志分析器中处理业务异常，而在 FastAPI 接口层转换为 HTTP 异常？

**今日最终交付物：** 完善后的 `exceptions.py`、日志分析器异常处理代码、FastAPI 接口异常转换代码，以及对应的测试结果。

## 七、扩展知识验收

### 问题 1：为什么不能在路由函数里直接写全部模型调用逻辑？

严格来说，不是不能写，而是不推荐把所有业务逻辑都写在路由函数里。

主要原因有三个：

1. **职责分离**：路由函数负责接收 HTTP 请求、参数校验和返回响应；模型调用、JSON 解析、字段校验等逻辑属于业务处理。
2. **便于复用**：将模型调用逻辑封装在独立的业务模块中，CLI、FastAPI 接口和后续 Agent 都可以复用，不需要重复编写。
3. **便于测试和维护**：业务逻辑独立后，可以单独测试模型调用、异常处理和输出校验，不必每次都启动 Web 服务。

例如，可以按以下方式分层：

```text
api.py                  # 接口层：接收请求、返回响应
    ↓
log_analyzer.py         # 业务层：组织日志分析流程
    ↓
LLM API                 # 模型调用
```

路由函数可以写成：

```python
@router.post("/analyze")
def analyze_log_api(request: LogAnalyzeRequest):
    result = analyze_log(request.log_text)
    return result
```

这样，路由函数只负责接口相关工作，具体的分析逻辑由 `analyze_log()` 完成。

**总结：** 不是禁止在路由函数中写业务代码，而是通过分层降低耦合，让代码更容易复用、测试和维护。

### 问题 2：为什么模型调用失败更适合返回 502，而不是 500？

因为两种状态码表达的错误含义不同。

| 状态码 | 含义 | 适用场景 |
|---|---|---|
| 500 Internal Server Error | 当前服务发生内部错误 | 本服务出现未预期的程序异常 |
| 502 Bad Gateway | 当前服务从上游服务获得了无效响应 | 模型服务返回异常响应，导致当前服务无法正常完成请求 |
| 504 Gateway Timeout | 等待上游服务响应超时 | 模型服务响应超时 |

当日志分析服务调用外部大模型 API 时，可以把大模型理解为上游服务。

```text
客户端
   ↓ HTTP 请求
FastAPI 日志分析服务
   ↓ API 调用
大模型服务
```

如果模型服务返回无效响应，日志分析服务可以根据实际情况返回 `502`；如果等待模型响应超时，可以返回 `504`。

但是，并不是所有模型调用失败都必须返回 `502`：

- 上游服务返回无效响应：可以考虑 `502`。
- 上游服务响应超时：可以考虑 `504`。
- 当前服务内部出现未预期的程序错误：适合 `500`。
- 上游服务暂时不可用：也可以根据实际语义考虑 `503`。

**总结：** `502` 更适合表达上游服务交互失败，`500` 更适合表达当前服务内部的未预期错误。具体使用哪个状态码，应根据真实失败原因决定。

### 问题 3：批量分析为什么要返回 `success_count` 和 `failure_count`？

因为批量分析可能出现**部分成功、部分失败**的情况，不能只用一个整体成功或失败的状态描述结果。

例如，一次提交 10 条日志：

- 8 条分析成功。
- 2 条分析失败。

如果只返回一个 `success: true`，调用方可能误以为 10 条日志全部分析成功；如果整体直接返回失败，又可能丢失已经成功的 8 条结果。

因此，可以设计如下响应：

```json
{
  "total_count": 10,
  "success_count": 8,
  "failure_count": 2,
  "results": [
    {
      "index": 0,
      "success": true,
      "result": {
        "error_type": "database",
        "confidence": 0.95
      }
    },
    {
      "index": 1,
      "success": false,
      "error": "模型调用失败"
    }
  ]
}
```

其中：

- `total_count`：本次提交的日志总数。
- `success_count`：分析成功的数量。
- `failure_count`：分析失败的数量。
- `results`：每条日志对应的分析结果或失败信息。

通常应满足：

\[
\text{total\_count}
=
\text{success\_count}
+
\text{failure\_count}
\]

这样设计有三个好处：

1. **便于调用方判断结果**：知道有多少条成功、多少条失败。
2. **支持失败重试**：可以只重试失败的日志，不必重新分析全部日志。
3. **便于监控和统计**：可以计算批量分析的成功率，发现模型服务或数据质量问题。

例如：

\[
\text{成功率}
=
\frac{\text{success\_count}}{\text{total\_count}}
\times 100\%
\]

需要注意，当 `total_count = 0` 时，应避免除以零。

**总结：** 批量分析返回 `success_count` 和 `failure_count`，是为了准确表达部分成功的执行结果，并为失败重试、运行监控和后续 Agent 调度提供依据。

## 八、今日学习总结补充

通过以上扩展问题，我进一步理解了以下工程设计原则：

1. **分层设计**：路由层负责 HTTP 请求与响应，业务层负责日志分析流程，模型调用逻辑独立封装，降低模块之间的耦合。
2. **合理使用 HTTP 状态码**：根据错误发生的位置和实际原因区分 `500`、`502`、`503` 和 `504`，提高接口语义的准确性。
3. **支持部分成功的批量处理**：通过 `total_count`、`success_count`、`failure_count` 和逐条 `results` 描述执行情况，便于失败重试和运行监控。
4. **面向后续 Agent 扩展**：清晰的模块边界、准确的异常分类和结构化执行结果，可以为后续任务状态查询、故障诊断、运维知识库检索及 Agent 工具调用提供基础。

**今日核心原则：合理划分模块职责、准确表达错误语义、完整记录批量执行结果，让日志分析服务更容易扩展和维护。**











