
from pydantic import BaseModel, Field
from typing import Literal

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



