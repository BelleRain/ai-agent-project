'''
今日目标
知道 JSON 字符串和 Python 对象的区别
会使用 Pydantic BaseModel
会把 LLM 返回的数据转换成结构化对象
用你工作中的 3 条真实错误日志完成测试

核心目标
不要只把 LLM 的返回结果当成字符串，而是把它转换成程序可以可靠使用的结构化对象。
Java 后端“数据接收 → DTO → 校验 → 业务处理”思维，迁移到 LLM 应用开发
LLM 负责生成内容，Pydantic 负责把内容变成程序可以理解和校验的数据结构。
'''



import json

from openai import OpenAI
from pydantic import BaseModel
from agent.config import *

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: list[str]
    suggestions: list[str]


logs = [
    "HikariPool-1 - Exception during pool initialization",
    "Communications link failure",
    "Unable to connect to any servers"
]

for log in logs:
    prompt = f""" 
请分析下面的 Java 错误日志，只返回 JSON，不要添加 Markdown 代码块。 
JSON 字段必须包含： error_type、possible_causes、suggestions。 
其中 possible_causes 和 suggestions 必须是数组。
错误日志：{log}
"""

    #用3条不同的日志作为测试，观察，是否结构不变，内容变化
    # HikariPool-1 - Exception during pool initialization
    #"Communications link failure"
    # "Unable to connect to any servers"

    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages=[
            {
                "role":"system",
                "content":(
                    "你是一名资深Java后端故障分析工程师。"
                    "回答必须简洁、分点，并区分现象、原因和建议。"
                ),
            },
            {
                "role":"user",
                "content": prompt
            }
        ]
    )
    res = response.choices[0].message.content
    print("================== Log ==================")
    # print(res)
    data = json.loads(res)
    result = ErrorAnalysis(**data)
    print(result)
    print("error_type:",result.error_type)
    print("suggestions:",result.suggestions)