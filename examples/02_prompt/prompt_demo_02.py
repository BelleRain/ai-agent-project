
# 将提示词改为要求Json


from openai import OpenAI

from agent.config import *

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# messages 为字典，非 json数组
#JSON 不是 Python 的数据类型，而是一种数据交换格式。

prompt = """ 
请分析下面的 Java 错误日志，只返回 JSON，不要添加 Markdown 代码块。 
JSON 字段必须包含： error_type、possible_causes、suggestions。 
其中 possible_causes 和 suggestions 必须是数组。
错误日志：Unable to connect to any servers
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

print(response.choices[0].message.content)


'''
result:

{
    "error_type": "HikariCP 连接池初始化失败",
    "possible_causes": [
        "数据库连接配置错误，如 JDBC URL、驱动类、用户名或密码不正确",
        "数据库服务未启动、不可达，或被防火墙/网络策略拦截",
        "数据库连接数已达上限，或账号无权限建立连接",
        "JDBC 驱动缺失、版本不匹配，或与数据库版本不兼容",
        "连接参数不兼容，如 SSL、时区、字符集、超时设置等",
        "数据库实例正在启动、维护或负载过高导致连接超时"
    ],
    "suggestions": [
        "查看完整异常堆栈和 Caused by，定位最底层错误",
        "检查 spring.datasource 或 HikariCP 的 jdbcUrl、driverClassName、username、password 配置",
        "确认数据库服务运行正常，并通过 telnet、nc 或数据库客户端测试网络连通性",
        "核对数据库账号权限、最大连接数、当前连接数及白名单/防火墙规则",
        "确认 JDBC 驱动版本与数据库版本匹配，并检查依赖是否完整",
        "调整连接超时、最大池大小、SSL、时区等参数后重试",
        "临时开启 HikariCP/数据库驱动 DEBUG 日志以获取更详细失败原因"
    ]
}

'''


















