import json
from datetime import datetime

from app.evaluation.dataset import TEST_CASES
from app.evaluation.scorer import score_result
from app.services.log_service import analyze_log
from config import settings


def evaluate_prompt(prompt_version: str) -> dict:
    results = []
    total_score = 0
    passed_count = 0

    for case in TEST_CASES:
        try:
            result = analyze_log(
                case["log_text"],
                prompt_version=prompt_version,
            )

            score_info = score_result(
                result,
                case["expected_keywords"],
            )

            total_score += score_info["score"]

            if score_info["passed"]:
                passed_count += 1

            results.append(
                {
                    "case_id": case["id"],
                    "success": True,
                    "score": score_info["score"],
                    "passed": score_info["passed"],
                    "checks": score_info["checks"],
                    "result": result.model_dump(),
                }
            )

        except Exception as exc:
            results.append(
                {
                    "case_id": case["id"],
                    "success": False,
                    "score": 0,
                    "passed": False,
                    "error": str(exc)
                }
            )

    return {
        "prompt_version": prompt_version,
        "model_name": settings.model_name,
        "run_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_cases": len(TEST_CASES),
        "passed_count": passed_count,
        "average_score": (
            # 三元表达式：结果A if 条件 else 结果B
            total_score / len(TEST_CASES)
            if TEST_CASES
            else 0
        ),
        "results": results,
    }


if __name__ == "__main__":
    from config import settings

    report = {
        "v1": evaluate_prompt("v1"),
        "v2": evaluate_prompt("v2"),
    }

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
    )































