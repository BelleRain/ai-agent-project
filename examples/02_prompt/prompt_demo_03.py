

# 同时分析3条日志
# 让同一个 Prompt 连续处理 3 条不同日志，验证模型是否能够在保持 JSON 结构一致的同时，根据不同日志生成不同的分析结果。

from openai import OpenAI

from agent.config import *

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# messages 为字典，非 json数组
#JSON 不是 Python 的数据类型，而是一种数据交换格式。

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
    print(f"\n===== 日志：{log} =====")
    print(response.choices[0].message.content)