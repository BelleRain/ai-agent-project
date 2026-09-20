
from openai import OpenAI

from agent.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    MODEL_NAME
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


# response = client.chat.completions.create(
#     model = MODEL_NAME,
#     messages=[
#         {
#             "role":"user",
#             "content":"你好，请用一句话介绍一下你自己。"
#         }
#     ]
# )
#
# print(response.choices[0].message.content)


question = input("请输入问题")

response = client.chat.completions.create(
    model = MODEL_NAME,
    messages=[
        {
            "role":"user",
            "content":question
        }
    ]
)

print(response.choices[0].message.content)






















