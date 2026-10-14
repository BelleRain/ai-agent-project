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
from openai import OpenAI

from agent.config import settings
from pydantic import BaseModel
import json

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: list[str]
    suggestions: list[str]

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
  "suggestions": ["至少 2 条解决建议"]
}}

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
                "content": USER_PROMPT_TEMPLATE,
            },
        ],
        response_format={'type': 'json_object'}, # 指定返回JSON格式，确保输出结构化数据
        temperature=0,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    print("api返回结果:",data)
    result = ErrorAnalysis.model_validate(data)
    print("\n错误类型", result.error_type)
    print("\n可能原因:")
    for cause in result.possible_causes:
        print("-", cause)
    print("\n解决建议：")
    for suggestion in result.suggestions:
        print("-", suggestion)



if __name__ == "__main__":
    log_text = "HikariPool-1 - Exception during pool initialization"
    analyze_log(log_text)















