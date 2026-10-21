

class LogAnalyzeError(Exception):
    """日志分析业务异常"""
    pass

class LLMServiceError(LogAnalyzeError):
    """调用模型异常"""
    pass

class StructuredOutputError(LogAnalyzeError):
    """结构化输出解析异常"""
    pass


