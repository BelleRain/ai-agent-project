SYSTEM_PROMPT = """
你是一名资深 Java 后端故障分析工程师。

请根据错误日志进行保守分析：
1. 只能基于日志内通推断
2. 无法确认时，confidence输出low
3. 必须给出支持判断的日志证据
4. 不要编造日志中不存在的信息
"""

USER_PROMPT_TEMPLATE = """
请分析下面的 Java 错误日志，并返回json格式的结构化结果：

要求：
1. error_type: 简洁描述错误类型
2. severity 只能输出 low、medium、high
3. confidence: 只能是 low、medium、high
4. possible_causes: 至少返回 5 条可能原因
5. suggestions: 至少返回 5 条执行建议
6. evidence: 至少返回 1 个证据对象
7. evidence 中包含两个字段 log_fragment、explanation
8. evidence.log_fragment 必须引用输入日志中的原文或关键片段
9. 无法确认时，必须降低 confidence
10. 不要输出 Markdown
11. 不要输出额外解释

错误日志：
{log_text}
"""


# {{
#   "error_type": "简洁的错误类型",
#   "possible_causes": ["至少 2 条可能原因"],
#   "suggestions": ["至少 2 条解决建议"]
# }}
#
# 要求：
# 1. 只返回 JSON
# 2. 不要输出 Markdown
# 3. 原因和建议必须结合日志
# 4. 无法确定的内容要明确说明“需要进一步确认”


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