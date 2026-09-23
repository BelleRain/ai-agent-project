# Day 4｜结构化输出异常处理 + 日志分析器函数化｜验收标准

## 一、今日学习目标

完成以下能力：

* [ ] 能够使用函数封装一次 LLM 调用
* [ ] 理解 Python 函数类型注解
* [ ] 能够捕获 `JSONDecodeError`
* [ ] 能够捕获 Pydantic `ValidationError`
* [ ] 理解 API 调用异常、JSON 解析异常、数据校验异常之间的区别
* [ ] 能够把底层异常转换成用户能够理解的错误信息

---

## 二、代码结构验收

`log_analyzer.py` 至少包含以下结构：

```text
log_analyzer.py
│
├── ErrorAnalysis
│
├── analyze_log()
│
├── print_analysis()
│
└── main
```

核心函数：

```python
def analyze_log(log_text: str) -> ErrorAnalysis:
    ...
```

需要能够解释：

```python
log_text: str
```

表示：

> `log_text` 参数预期为 `str` 类型。

```python
-> ErrorAnalysis
```

表示：

> 函数预期返回一个 `ErrorAnalysis` 类型的对象。

---

## 三、正常调用验收

分别测试以下 3 条日志：

```text
HikariPool-1 - Exception during pool initialization
```

```text
No Feign Client for loadBalancing
```

```text
zookeeper connect timeout
```

### 通过标准

* [ ] 程序能够正常启动
* [ ] 能够调用 LLM
* [ ] 能够获得模型返回结果
* [ ] `json.loads()` 能够正常解析
* [ ] `ErrorAnalysis(**data)` 能够正常创建对象
* [ ] 能够打印错误类型、可能原因和解决建议
* [ ] 至少成功完成 2 条日志分析

---

## 四、`JSONDecodeError` 验收 ⭐

主动模拟模型返回非法 JSON。

例如：

```python
content = '{"error_type": "连接超时"'
```

然后执行：

```python
data = json.loads(content)
```

### 预期结果

程序进入：

```python
except json.JSONDecodeError as exc:
```

### 必须理解

`JSONDecodeError` 是 `json.loads()` 在解析非法 JSON 时自动抛出的异常。

例如：

```text
非法 JSON
    ↓
json.loads()
    ↓
JSONDecodeError
    ↓
except 捕获
```

### 自测问题

> 为什么这里会产生 `JSONDecodeError`？

标准理解：

> 因为字符串不是合法的 JSON 格式，`json.loads()` 无法完成解析。

---

## 五、`ValidationError` 验收 ⭐

模拟一个**合法 JSON，但字段不完整**的情况：

```python
content = """
{
    "error_type": "连接超时",
    "possible_causes": ["网络异常"]
}
"""
```

然后执行：

```python
data = json.loads(content)
result = ErrorAnalysis(**data)
```

### 预期结果

`json.loads()` 正常执行，但是：

```python
ErrorAnalysis(**data)
```

进入：

```python
except ValidationError as exc:
```

### 必须理解

这里不是 `JSONDecodeError`，因为：

```text
JSON 格式
    ↓
合法
```

但是：

```text
ErrorAnalysis
    ↓
缺少 suggestions 字段
    ↓
Pydantic 校验失败
    ↓
ValidationError
```

### 自测问题

> 为什么这个例子不会产生 `JSONDecodeError`？

标准理解：

> 因为 JSON 本身是合法的，问题发生在 JSON 转换成 `ErrorAnalysis` 对象时。

---

## 六、三种异常场景验收

能够区分以下三种情况：

### ① API 调用失败

```text
网络 / Base URL / API Key / 服务异常
        ↓
LLM API 调用失败
```

例如：

```env
OPENAI_BASE_URL=http://127.0.0.1:9999/v1
```

要求：

* [ ] 能够主动制造一次 API 调用失败
* [ ] 程序能够进入最外层异常处理
* [ ] 能够向用户输出“分析失败”等可理解的信息

---

### ② JSON 解析失败

```text
模型返回非法 JSON
        ↓
json.loads()
        ↓
JSONDecodeError
```

要求：

* [ ] 能够主动模拟
* [ ] 能够进入 `except json.JSONDecodeError`
* [ ] 能够解释为什么产生这个异常

---

### ③ JSON 结构校验失败

```text
JSON 格式合法
        ↓
字段缺失 / 类型错误
        ↓
Pydantic
        ↓
ValidationError
```

要求：

* [ ] 能够主动模拟
* [ ] 能够进入 `except ValidationError`
* [ ] 能够解释为什么产生这个异常

---

## 七、异常处理代码验收

能够理解以下代码：

```python
try:
    data = json.loads(content)
    return ErrorAnalysis(**data)

except json.JSONDecodeError as exc:
    raise ValueError(
        f"模型返回的内容不是合法 JSON：{content}"
    ) from exc

except ValidationError as exc:
    raise ValueError(
        f"模型返回字段不符合要求：{content}"
    ) from exc
```

需要能够解释：

```python
except json.JSONDecodeError as exc:
```

其中：

* `JSONDecodeError`：异常类型
* `as exc`：把捕获到的异常对象保存到 `exc`

以及：

```python
raise ValueError(...) from exc
```

表示：

> 将底层异常转换成更适合业务层处理的 `ValueError`，同时保留原始异常原因。

---

## 八、Java 对照理解验收

能够把今天的代码与 Java 后端思路对应起来：

```text
Python                         Java

LLM API 调用          ←→       HTTP / RPC 调用

json.loads()          ←→       JSON 反序列化

JSONDecodeError       ←→       JSON 解析异常

Pydantic              ←→       DTO / 参数校验

ValidationError       ←→       参数校验异常

ValueError            ←→       业务层异常

try / except          ←→       try / catch
```

重点理解：

> LLM 是一个外部服务，不能假设它永远返回正确结果。AI 应用代码必须对模型输出进行解析、校验和异常处理。

---

## 九、最终口头验收

不看资料，能够回答下面 6 个问题：

### 1.

```python
def analyze_log(log_text: str) -> ErrorAnalysis:
```

是什么意思？

### 2.

`JSONDecodeError` 是谁抛出来的？

### 3.

什么情况下会出现 `JSONDecodeError`？

### 4.

为什么 JSON 合法了，仍然可能出现 `ValidationError`？

### 5.

为什么要把 LLM 调用封装进：

```python
analyze_log()
```

而不是全部写在 `main` 中？

### 6.

下面两个异常分别发生在哪一步？

```text
JSONDecodeError
ValidationError
```

---

# 🎯 Day 4 通过标准

满足以下条件即可认为 Day 4 通过：

* [ ] 能够独立运行 `log_analyzer.py`
* [ ] 能够使用 `analyze_log()` 完成日志分析
* [ ] 能够分析至少 2 条 Java / 调度平台日志
* [ ] 能够主动模拟 `JSONDecodeError`
* [ ] 能够主动模拟 `ValidationError`
* [ ] 能够主动模拟 API 调用失败
* [ ] 能够解释三种异常分别发生在哪一层
* [ ] 能够解释 `log_text: str`
* [ ] 能够解释 `-> ErrorAnalysis`
* [ ] 能够理解为什么 LLM 返回 JSON 后仍然需要校验

## 最终判断

如果你能够用自己的话说明：

> **LLM 调用可能失败；调用成功后，模型返回内容可能不是合法 JSON；即使 JSON 合法，也可能不符合我定义的 `ErrorAnalysis` 数据结构。因此需要经过 API 异常处理 → JSON 解析 → Pydantic 校验，最终才能交给业务代码使用。**

那么：

**Day 4 ✅ 通过**

今天不要求学习 Tool Calling、Agent 工具执行或 RAG。
这些内容按照原计划放到后续阶段。
