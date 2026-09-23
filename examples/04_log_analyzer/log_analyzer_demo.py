'''
今日目标
1、API调用失败时，程序不能直接崩溃
2、模型返回内容可能不是合法JSON
3、JSON能解析，不代表字段一定完整
4、把 “调用模型” 封装成函数，方便后续复用

对应到 Java 后端开发，可以理解为：

远程调用
   ↓
异常捕获
   ↓
返回值校验
   ↓
DTO 转换
   ↓
业务层继续处理

三条测试日志：
HikariPool-1 - Exception during pool initialization
No Feign Client for loadBalancing
zookeeper connect timeout
'''


from agent.config import *
import json
from pydantic import BaseModel,ValidationError
from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_cause: list[str]
    suggestions: list[str]


def analyze_log(log_text: str) -> ErrorAnalysis:
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一名资深 Java 后端故障分析工程师。"
                    "只返回合法 JSON, 不要输出 Markdown 代码块。"
                )
            },
            {
              "role":"user",
              "content":f"""
                    请分析下面的错误日志，并严格返回 JSON：
                    {{
                          "error_type": "字符串",
                          "possible_causes": ["字符串"],
                          "suggestions": ["字符串"]
                    }}
                    错误日志：
                    {log_text}
            """,
            },
        ],
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return ErrorAnalysis(**data)
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


def print_analysis(result: ErrorAnalysis) -> None:
    print("错误类型" , result.error_type)
    print("\n可能原因:")
    for cause in result.possible_cause:
        print("-",cause)
    print("\n解决建议：")
    for suggestion in result.suggestions:
        print("-",suggestion)

if __name__ == "__main__":
    log_text = input("请输入错误日志：")
    try:
        result = analyze_log(log_text)
        print_analysis(result)
    except Exception as exc:
        print("分析失败：",exc)


























