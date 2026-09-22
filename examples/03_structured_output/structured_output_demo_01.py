
import json
from pydantic import BaseModel

class ErrorAnalysis(BaseModel):
    error_type: str
    possible_causes: list[str]
    suggestions: list[str]


# 假设这里是模型返回的内容
content = """
{
    "error_type": "数据库连接失败",
    "possible_causes": [
        "数据库地址不可达",
         "数据库服务未启动"
    ],
    "suggestions": [
        "检查数据库服务状态", 
        "检查网络连接"
    ]
}
"""

#print(type(content))

data = json.loads(content)

result = ErrorAnalysis(**data)

print(result)
print(result.error_type)
print(result.suggestions)

















