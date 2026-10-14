"""
今日目标：
理解链路：
Pydantic Model
      ↓
JSON Schema
      ↓
API 原生约束
      ↓
直接解析为对象
      ↓
业务校验

理解三个层次：
普通文本：
模型自由输出

JSON Mode：
保证尽量是合法 JSON

Structured Outputs：
按 Schema 约束字段、类型和结构

注意：结构正确 ≠ 内容正确

"""

# 由于接口不支持json_schema,所以本次代码使用的是 json_object 方式

from openai import OpenAI

from agent.config import settings
from pydantic import BaseModel, ValidationError
import json
from typing import Literal, List


# Prompt 是软约束，Schema 是结构层面的硬约束。
# Literal["low", "medium", "high"] 表示：
# confidence 只能是这三个字符串中的一个，不能随意填写其他字符串。
class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: list[str]
    suggestions: list[str]
    #confidence: str
    confidence: Literal["low", "medium", "high"]

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
)

SYSTEM_PROMPT = """
你是一名资深 Java 后端故障分析工程师。
请根据错误日志，给出简洁、可执行、基于证据的故障分析。
如果无法确定，请明确说明需要进一步确认。
"""

USER_PROMPT_TEMPLATE = """
请分析下面的错误日志，并返回 JSON：

{{
  "error_type": "简洁的错误类型",
  "possible_causes": ["至少 2 条可能原因"],
  "suggestions": ["至少 2 条解决建议"],
  "confidence": "low、medium 或 high"
}}

confidence 表示你对本次错误分析结论的置信程度：
- low：日志证据不足，无法明确判断原因
- medium：有一定证据，但仍存在多种可能
- high：日志证据明确，结论有较强依据

confidence 只能返回 low、medium、high 这三个值之一。

要求：
1. 只返回 JSON
2. 不要输出 Markdown
3. 原因和建议必须结合日志
4. 无法确定的内容要明确说明“需要进一步确认”

错误日志：
{log_text}
"""


def analyze_log(log_text: str) -> ErrorAnalysis:
    response = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(log_text=log_text),
            },
        ],
        response_format={'type': 'json_object'}, # 指定返回JSON格式，确保输出结构化数据
        temperature=0,
    )

    content = response.choices[0].message.content
    if not content or not content.strip():
            raise ValueError("模型返回内容为空")
    try:
        data = json.loads(content)
        # print("api返回结果:", data)
    except json.JSONDecodeError as exc:
        raise ValueError("模型返回的不是合法 JSON") from exc
    try:
        return ErrorAnalysis.model_validate(data)
    except ValidationError as exc:
        raise ValueError("模型返回的数据不符合要求") from exc

# 结果校验函数
def validate_analysis(result: ErrorAnalysis) -> List[str]:
    warnings = []
    if len(result.possible_causes) < 5:
        warnings.append("可能原因少于5条")
    if len(result.suggestions) < 5:
        warnings.append("解决建议少于5条")
    if len(result.error_type.strip()) < 5:
        warnings.append("错误类型描述太短")
    return warnings


if __name__ == "__main__":
    log = "HikariPool-1 - Exception during pool initialization"
    result = analyze_log(log)
    print("\n错误类型", result.error_type)
    print("\n可能原因:")
    for cause in result.possible_causes:
        print("-", cause)
    print("\n解决建议：")
    for suggestion in result.suggestions:
        print("-", suggestion)
    print("\n置信度：", result.confidence)
    print("\n========warnings========")
    warnings = validate_analysis(result)
    print(warnings)
















