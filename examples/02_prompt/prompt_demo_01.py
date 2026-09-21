'''
今日目标：
System Prompt：规定模型的身份、规则和输出要求
User Prompt：本次具体任务和输入数据
Few-shot：给模型看少量输入/输出示例
Structured Output：让模型返回固定 JSON 结构

理解核心：
普通提问：模型自由回答
结构化要求：模型输出可以被程序继续处理的数据
'''

from openai import OpenAI

from agent.config import *

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

# messages 为字典，非 json数组
#JSON 不是 Python 的数据类型，而是一种数据交换格式。
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
            "content":(
                "请分析下面的错误日志：\n"
                "Unable to connect to any servers"
            )
        }
    ]
)

print(response.choices[0].message.content)

#用三条日志观察输出 结构以及内容的变化
#"HikariPool-1 - Exception during pool initialization"
#"Communications link failure"
#"Unable to connect to any servers"

'''
result:
/Users/mengxinyu/pycharmProject/ai-agent-project/.venv/bin/python /Users/mengxinyu/pycharmProject/ai-agent-project/examples/02_prompt/prompt_demo_01.py 
**现象**
- HikariCP 的 `HikariPool-1` 在初始化阶段失败，连接池未创建成功。
- 应用通常启动失败，或首次访问数据库时报错。
- 这一行只是概述，真正根因在后续堆栈的 `Caused by`。

**原因**
- 网络/数据库不可达：host、port 错，DB 未启动，防火墙/安全组拦截，DNS 或容器网络异常。
- 认证/库问题：用户名密码错误，数据库不存在，权限不足。
- JDBC 配置/驱动：URL 格式错，驱动缺失或版本不匹配，时区/SSL 参数不兼容。
- 连接池配置：`connectionTimeout`、`initializationFailTimeout` 过短，`connectionInitSql` 或 `validationQuery` 错误。
- 数据库端限制：最大连接数满、IP 白名单、强制 SSL、实例启动中或只读。

**建议**
1. 先看完整日志，重点定位第一个 `Caused by`。
2. 常见映射：
   - `Connection refused`：DB 未启动或端口错。
   - `UnknownHostException`：DNS/主机名错。
   - `Access denied`：账号密码或权限错。
   - `No suitable driver`：JDBC 驱动依赖缺失。
   - `Communications link failure`：网络、SSL、超时问题。
3. 核对 `url/username/password/driver-class-name` 与实际数据库一致。
4. 网络排查：`telnet dbHost dbPort`、`nc -vz dbHost dbPort`；容器环境检查 service name、端口映射、网络。
5. DB 侧检查：进程、监听端口、最大连接数、白名单、SSL 要求。
6. 用 DBeaver、mysql/psql 或最小 JDBC 程序，以相同参数直连验证。
7. 开启 Hikari DEBUG：`logging.level.com.zaxxer.hikari=DEBUG`。
8. 确保驱动版本匹配，如 MySQL 8 使用 `com.mysql.cj.jdbc.Driver`，必要时补时区/SSL 参数。

**结论**
仅凭这一行无法确定根因，必须结合后续 `Caused by` 和完整堆栈。优先排查：网络连通、账号密码、JDBC URL、驱动依赖、数据库状态。

Process finished with exit code 0

'''






























