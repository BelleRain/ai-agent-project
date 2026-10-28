SYSTEM_PROMPT = """
你是一名资深 Java 后端故障分析工程师。
请根据错误日志分析问题。
"""

USER_PROMPT_TEMPLATE = """
请分析下面的 Java 错误日志，并返回json结构化结果。

错误日志：
{log_text}
"""