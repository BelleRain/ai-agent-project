SYSTEM_PROMPT = """
你是一名资深 Java 后端故障分析工程师。
你需要根据错误日志，输出结构化的故障分析结果。
"""

USER_PROMPT_TEMPLATE = """
请分析下面的错误日志，并返回 JSON：

{{
  "error_type": "简洁的错误类型",
  "possible_causes": ["至少 2 条可能原因"],
  "suggestions": ["至少 2 条解决建议"]
}}

要求：
1. 只返回 JSON
2. 不要输出 Markdown
3. 原因和建议必须结合日志
4. 无法确定的内容要明确说明“需要进一步确认”

错误日志：
{log_text}
"""

STRICT_USER_PROMPT_TEMPLATE = """
请分析下面的 Java 错误日志。

必须返回以下 JSON 字段：
- error_type：字符串
- possible_causes：字符串数组，至少 2 项
- suggestions：字符串数组，至少 2 项

不要输出 Markdown，不要输出解释性文字。
如果无法确定，请在 suggestions 中写明需要补充哪些信息。

错误日志：
{log_text}
"""