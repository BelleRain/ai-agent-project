
from pydantic import BaseModel, Field
from typing import Literal

class LogAnalyzeRequest(BaseModel):
    log_text: str = Field(
        min_length=1,
        max_length=1000,
        description="待分析的错误日志"
    )

class Evidence(BaseModel):
    log_fragment: str = Field(
        description="用于支持判断的关键日志片段"
    )
    explanation: str = Field(
        description="说明该日志片段为什么支持当前判断"
    )


class ErrorAnalysis(BaseModel):
    error_type: str = Field(
        description="简洁的错误类型，例如数据库连接失败"
    )
    severity: Literal["low","medium","high"] = Field(
        description="问题严重程度"
    )
    confidence: Literal["low","medium","high"] = Field(
        description="模型对当前判断的置信度"
    )
    possible_causes: list[str] = Field(
        min_length=1,
        description="可能原因列表"
    )
    suggestions: list[str] = Field(
        min_length=1,
        description="解决建议列表"
    )
    evidence: list[Evidence] = Field(
        min_length=1,
        description="支撑判断的证据"
    )

# str | None：联合类型，表示字段可以是 str 类型或者 None，| 表示类型可以是多个候选类型之一。
# = None 表示：如果没有给 message 传值，就默认使用 None。
# 在 Pydantic 模型中，没有默认值的字段通常仍然是必填字段。

# name: str 字符串类型，没有默认值。
# name: str = "未知" 字符串类型，默认值为 "未知"。
# name: str | None 字符串或 None，但没有默认值，字段必须提供。
# name: str | None = None 字符串或 None，默认值为 None，字段可以不提供。

class LogAnalyzeResponse(BaseModel):
    success: bool
    data: ErrorAnalysis | None = None
    message: str | None = None


class ApiResponse(BaseModel):
    success: bool
    data: ErrorAnalysis | None = None
    message: str
    warnings: list[str] = []

# 批量请求
class BatchLogAnalyzeRequest(BaseModel):
    logs: list[LogAnalyzeRequest]

#批量接口
class BatchItemResult(BaseModel):
    success: bool
    data: ErrorAnalysis | None = None
    message: str | None = None

class BatchLogAnalyzeResponse(BaseModel):
    total: int
    success_count: int
    failure_count: int
    results: list[BatchItemResult]


















