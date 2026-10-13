
from typing import List
from log_analyzer.models import ErrorAnalysis

# 注意：Pydantic 解决的是 数据结构是否符合要求
# validate_analysis() 解决的是：
# 虽然结构正确，但是业务内容是否基本合格

# 结果校验函数
def validate_analysis(result: ErrorAnalysis) -> List[str]:
    warnings = []
    if len(result.possible_causes) < 5:
        warnings.append("可能原因少于5条")
    if len(result.suggestions) < 5:
        warnings.append("解决建议少于5条")
    if len(result.error_type.strip()) < 5:
        warnings.append("错误类型描述太短")
    return warnings


# 简单评分函数
#将一些业务要求转换为可自动检查的规则
def score_analysis(result: ErrorAnalysis) -> int:
    score = 100
    if len(result.possible_causes) < 5:
        score -= 20
    if len(result.suggestions) < 5:
        score -=20
    if len(result.error_type.strip()) < 5:
        score -= 20
    return max(score,0)


































