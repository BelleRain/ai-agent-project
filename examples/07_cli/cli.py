"""
今日目标：
命令行输入
    ↓
Prompt 模板
    ↓
LLM API
    ↓
JSON 解析
    ↓
Pydantic 校验
    ↓
结果评分
    ↓
终端输出
"""

# log_analyzer.py ：调用模型
# prompt_eval.py ：结果校验和评分
# cli.py ：用户交付


import argparse
import json
from agent.config import settings
from pydantic import BaseModel,ValidationError
from openai import OpenAI
from typing import List



client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,
)

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: List[str]
    suggestions: List[str]


SYSTEM_PROMPT = """
你是一名资深 Java 后端故障分析工程师。

请根据错误日志进行保守分析：
1. 只能基于日志内通推断
2. 无法确认时，confidence输出low
3. 必须给出支持判断的日志证据
4. 不要编造日志中不存在的信息
"""

USER_PROMPT_TEMPLATE = """
请分析下面的 Java 错误日志，并返回json格式的结构化结果：

要求：
1. error_type: 简洁描述错误类型
2. severity 只能输出 low、medium、high
3. confidence: 只能是 low、medium、high
4. possible_causes: 至少返回 5 条可能原因
5. suggestions: 至少返回 5 条执行建议
6. evidence: 至少返回 1 个证据对象
7. evidence 中包含两个字段 log_fragment、explanation
8. evidence.log_fragment 必须引用输入日志中的原文或关键片段
9. 无法确认时，必须降低 confidence
10. 不要输出 Markdown
11. 不要输出额外解释

错误日志：
{log_text}
"""


def analyze_log(log_text: str) -> ErrorAnalysis:
    user_prompt = USER_PROMPT_TEMPLATE.format(log_text=log_text)
    response = client.chat.completions.create(
        model = settings.model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
              "role":"user",
              "content": user_prompt
            },
        ],
        response_format={"type": "json_object"}
        # temperature=settings.temperature,
        # max_tokens=settings.max_tokens,
    )

    content = response.choices[0].message.content
    if not content or not content.strip():
        raise ValueError("模型返回内容为空")
    try:
        data = json.loads(content)
        return ErrorAnalysis.model_validate(data)
    # 非法JSON
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"模型返回的内容不是合法JSON ：{content}"
        ) from exc
    #字段异常
    except ValidationError as exc:
        raise ValueError(
            f"模型返回字段不符合要求：{content}"
        ) from exc


def validate_analysis(result: ErrorAnalysis) -> List[str]:
    warnings = []
    if len(result.possible_causes) < 10:
        warnings.append("可能原因少于10条")
    if len(result.suggestions) < 10:
        warnings.append("解决建议少于10条")
    if len(result.error_type.strip()) < 10:
        warnings.append("错误类型描述太短")
    return warnings


# 简单评分函数
#将一些业务要求转换为可自动检查的规则
def score_analysis(result: ErrorAnalysis) -> int:
    score = 100
    if len(result.possible_causes) < 10:
        score -= 20
    if len(result.suggestions) < 10:
        score -=20
    if len(result.error_type.strip()) < 10:
        score -= 20
    return max(score,0)




def main():
    parser = argparse.ArgumentParser(
        description="Java 错误日志分析器"
    )

    parser.add_argument(
        "--log",
        # required=True,
        help="要分析的错误日志"
    )

    # 增加文件输入模式
    # 新增可选参数
    parser.add_argument(
        "--file",
        help = "从文件中逐行读取日志",
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file,"r",encoding="utf-8") as file:
            logs = [line.strip() for line in file if line.strip()]
        for log in logs:
            print (f"\n正在分析：{log}")
            try:
                result = analyze_log(log)
                print(result.model_dump_json(indent=2, ensure_ascii=False))
            except Exception as exc:
                print("分析失败：",exc)

    else:
        try:
            result = analyze_log(args.log)
            warnings = validate_analysis(result)
            score = score_analysis(result)
            print("\n========== 分析结果 ==========")
            print("错误类型：",result.error_type)
            print("\n可能原因")
            for cause in result.possible_causes:
                print("-",cause)
            print("\n解决建议：")
            for suggestion in result.suggestions:
                print("-",suggestion)
            print("\n质量评分：", score)
            if warnings:
                print("\n质量提醒：")
                for warning in warnings:
                    print("-",warning)
            else:
                print("\n结果通过基础质量检查")

        except Exception as exc:
            print(f"分析失败：{exc}")


if __name__ == "__main__":
    main()











































