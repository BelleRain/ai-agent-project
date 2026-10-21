"""
练习：建立最小评估集
"""

from config import *
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
    prompt = PROMPT_B.format(log_text=log_text)
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


# def annlyze_logs(logs: List[str]) -> List[ErrorAnalysis]:
#     results = []
#     for index, log_text in enumerate(logs , 1):
#         print(f"\n正在分析第 {index} 条日志...")
#         try:
#             result = analyze_log(log_text)
#             results.append(result)
#         except Exception as exc:
#             print(f"分析失败：{exc}")
#     return results

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

# 批量测试 + 结果校验 + 质量评分 + 平均分统计
# 批量评估函数
def evaluate_logs(logs: List[str]) -> None:
    total_score = 0
    for index, log_text in enumerate(logs, 1):
        print(f"\n======= 第 {index} 条日志 =======")
        print(log_text)
        try:
            result = analyze_log(log_text)
            warnings = validate_analysis(result)
            score = score_analysis(result)
            total_score += score
            print("错误评分：", result.error_type)
            print("评分：", score)
            if warnings:
                print("质量提醒：")
                for warning in warnings:
                    print("-",warning)
            else:
                print("结果通过基础质量检查")
        except Exception as exc:
            print(f"分析失败：{exc}")
    if logs:
        print(f"\n总分：{total_score} , 平均分：{total_score/len(logs) : .2f}")


# 固定测试集 -> 运行 Prompt -> 得到结果 -> 自动评分 -> 比较不同结果
if __name__ == "__main__":
    # Evaluation Dataset（评估数据集）
    logs = [
        "HikariPool-1 - Exception during pool initialization",
        "Communications link failure",
        "No Feign Client for loadBalancing",
        "zookeeper connect timeout",
        "NettyRemotingServer bind fail",
    ]
    evaluate_logs(logs)

































