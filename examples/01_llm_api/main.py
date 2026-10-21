
from openai import OpenAI

from config import *

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
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
    model = settings.model_name,
    messages=[
        {
            "role":"user",
            "content":question
        }
    ]
)

print(response.choices[0].message.content)






















