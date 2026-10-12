"""
核心目标
1.Prompt 约束不等于绝对可靠
2.JSON 可解析不等于字段完整
3.结构化结果必须做校验
4.AI 应用需要最基本的评估数据
"""

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
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# PROMPT_A 返回信息无法解析，没有对象规定字段，直接抛出异常
# PROMPT_B 返回的结果可用
PROMPT_A = """
请分析下面的 Java 错误日志，返回 JSON。

错误日志：
{log_text}
"""

PROMPT_B = """
你是一名资深 Java 后端故障分析工程师。

请严格返回 JSON，字段如下：

{{
  "error_type": "简洁的错误类型",
  "possible_causes": ["至少 2 条可能原因"],
  "suggestions": ["至少 2 条解决建议"]
}}

要求：
1. 只返回 JSON
2. 不要 Markdown
3. 不要输出额外解释
4. 原因和建议必须是数组
5. 内容必须结合日志，不要泛泛而谈

错误日志：
{log_text}
"""

def analyze_log(log_text: str) -> ErrorAnalysis:
    # prompt = PROMPT_A.format(log_text=log_text)
    prompt = PROMPT_B.format(log_text=log_text)
    response = client.chat.completions.create(
        model=MODEL_NAME,
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

# 注意：Pydantic 解决的是 数据结构是否符合要求
# validate_analysis() 解决的是：
# 虽然结构正确，但是业务内容是否基本合格

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


# 简单评分函数
#将一些业务要求转换为可自动检查的规则
def score_analysis(result: ErrorAnalysis) -> int:
    score = 100
    if len(result.possible_causes) < 5:
        score -= 20
    if len(result.suggestions) < 5:
        score -=20
    if len(result.error_type.strip()) < 5:
        score -= 20
    return max(score,0)

if __name__ == "__main__":
    logs = "HikariPool-1 - Exception during pool initialization"
    result = analyze_log(logs)
    warnings = validate_analysis(result)
    score = score_analysis(result)
    print("评分：", score)
    if warnings:
        print("质量提醒：")
        for warning in warnings:
            print("-",warning)
    else:
        print("结果通过基础质量检查")
































