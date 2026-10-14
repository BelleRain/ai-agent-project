'''
今日目标：
1、Prompt 不应该散落在业务代码各处
2、模板化后，日志内容可以动态注入
3、单条处理和批量处理的代码结构不同
4、LLM 返回结果要做校验
5、结构化结果可以继续被程序统计和汇总

核心理解：
LLM 负责理解，Python 负责业务处理
'''
from agent.config import *
import json
from pydantic import BaseModel,ValidationError
from openai import OpenAI

from typing import List

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: List[str]
    suggestions: List[str]

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
)

PROMPT_TEMPLATE = """
你是一名资深 Java 后端故障分析工程师。

请分析下面的错误日志，并严格返回合法 JSON：
{{
  "error_type": "字符串",
  "possible_causes": ["字符串"],
  "suggestions": ["字符串"]
}}

要求：
1. error_type 必须简洁
2. possible_causes 至少返回 2 条
3. suggestions 至少返回 2 条
4. 不要输出 Markdown
5. 不要输出额外说明

错误日志：
{log_text}
"""

# Python 的 字典解包（unpacking）调用
# ErrorAnalysis(**data) = 把字典 data 拆成关键字参数传给 ErrorAnalysis，
# 字典的 key 对应参数名，value 对应参数值。
# 常见于从 JSON / LLM 返回的结构化结果构造对象。


def analyze_log(log_text: str) -> ErrorAnalysis:
    prompt = PROMPT_TEMPLATE.format(log_text=log_text)
    response = client.chat.completions.create(
        model=settings.model_name,
        messages=[
            {
                "role": "system",
                "content": "你负责将Java 错误日志转换为结构化故障分析结果"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    try:
        data = json.loads(content)
        return ErrorAnalysis(**data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"返回结果不是合法 JSON：{content}") from exc
    except ValidationError as exc:
        raise ValueError(f"返回结果字段不符合数据结构：{content}") from exc


def analyze_logs(logs: List[str]) -> List[ErrorAnalysis]:
    results = []
    for index, log_text in enumerate(logs, start=1):
        print(f"\n正在分析第 {index} 条日志...")
        try:
            result = analyze_log(log_text)
            results.append(result)
        except Exception as exc:
            print(f"分析失败：{exc}")
    return results


def print_summary(results: List[ErrorAnalysis]) -> None:
    print("\n=========分析汇总============")
    for index, result in enumerate(results,start=1):
        print(f"\n[{index}] {result.error_type}")
        print("可能原因：")
        for cause in result.possible_causes:
            print("-",cause)

        print("解决建议：")
        for suggestion in result.suggestions:
            print(" -",suggestion)

if __name__ == "__main__":
    logs = [
        "Communications link failure",
        "Unknown column 'max_run_count'",
        "sqlSessionFactory bean creation failed",
        "past MaxStartups",
    ]

    results = analyze_logs(logs)
    print_summary(results)




































