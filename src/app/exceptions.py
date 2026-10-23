
class AppBaseError(Exception):
    def __init__(
            self,
            message: str,
            error_code: str = "APP_ERROR"
    ):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class LogAnalyzeError(Exception):
    """日志分析业务异常"""
    pass

class LLMServiceError(AppBaseError):
    """调用模型异常"""
    def __init__(self, message="模型服务调用失败"):
        super().__init__(message,"LLM_SERVICE_ERROR")

class StructuredOutputError(AppBaseError):
    """结构化输出解析异常"""
    def __init__(self, message="结构化输出解析失败"):
        super().__init__(message, "STRUCTURED_OUTPUT_ERROR")


