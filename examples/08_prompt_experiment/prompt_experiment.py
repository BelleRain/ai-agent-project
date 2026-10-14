"""
今日目标：理解模型参数对输出稳定性和结果质量的影响，
并建立可重复的Prompt实验
"""

import json
from typing import List
from pydantic import BaseModel
from agent.config import *
from openai import OpenAI

from log_analyzer.log_analyzer import client

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
)

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: list[str]
    suggestions: list[str]


PROMPT = """
你是一名资深 Java 后端故障分析工程师。

请分析下面的错误日志，并严格返回 JSON：
{{
  "error_type": "简洁的错误类型",
  "possible_causes": ["至少 2 条可能原因"],
  "suggestions": ["至少 2 条解决建议"]
}}

要求：
1. 只返回 JSON
2. 不要输出 Markdown
3. 原因和建议必须结合日志
4. 不要给出无法从日志推断出的绝对结论

错误日志：
{log_text}
"""
PROMPT_SIMPLE = """
请分析下面的 Java 错误日志并返回 JSON：
{log_text}
"""

def analyze_log(log_text: str, temperature: float) -> ErrorAnalysis:
    response = client.chat.completions.create(
        model= settings.model_name,
        messages=[
            {
                "role": "system",
                "content": "你负责将 Java 错误日志转换为结构化故障分析结果。",
            },
            {
                "role": "user",
                "content": PROMPT.format(log_text=log_text),
            },
        ],
        temperature=temperature,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    return ErrorAnalysis(**data)


# 实验函数
def run_experiment(log_text: str) -> None:
    # temperatures = [0,0.3,0.7,1.0]
    temperatures = [0.3]
    for temperature in temperatures:
        print(f"=========== temperature={temperature} ===============")
        try:
            result = analyze_log(log_text,temperature)
            # print("错误类型：", result.error_type)
            # print("可能原因：", result.possible_causes)
            # print("解决建议：", result.suggestions)
            print(result.model_dump_json(indent=2, ensure_ascii=False))
        except Exception as exc:
            print("调用错误：", exc)

if __name__ == "__main__":
    # log = "HikariPool-1 - Exception during pool initialization"
    # analyze_log(log,0.3)
    run_experiment(
        "HikariPool-1 - Exception during pool initialization"
    )


























