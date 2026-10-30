
from app.models import ErrorAnalysis


def score_result(
       result: ErrorAnalysis,
       expected_keywords: list[str],
) -> dict:
    text = " ".join(
        [
            result.error_type,
            *result.possible_causes,
            *result.suggestions,
        ]
    )

    evidence_text = " ".join(
        item.log_fragment for item in result.evidence
    )

    # Python 的 生成器表达式
    # (表达式 for 变量 in 可迭代对象)
    evidence_hit = any(
        keyword.lower() in evidence_text.lower()
        for keyword in expected_keywords
    )

    keyword_hits = sum(
        1 for keyword in expected_keywords
        if keyword.lower() in text.lower()
    )

    # 等价写法：
    # keyword_hits = 0
    # for keyword in expected_keywords:
    #     if keyword.lower() in text.lower():
    #         keyword_hits += 1

    score = 0

    if result.error_type.strip():
        score += 20

    if len(result.possible_causes) >= 2:
        score += 20

    if len(result.suggestions) >= 2:
        score += 20

    if len(result.evidence) >= 1:
        score += 20

    if keyword_hits >= 1:
        score += 10

    if evidence_hit:
        score += 10

    # 每项评分条件
    checks = {
        "error_type_valid": bool(result.error_type.strip()),
        "causes_enough": len(result.possible_causes) >= 2,
        "suggestions_enough": len(result.suggestions) >= 2,
        "evidence_exists": len(result.evidence) >= 1,
        "keyword_matched": keyword_hits >= 1,
        "evidence_hit": evidence_hit,
    }

    return {
        "score": score,
        "keywords_hits": keyword_hits,
        "passed": score >= 80,
        "checks": checks,
    }














































