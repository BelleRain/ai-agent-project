
from log_analyzer.log_analyzer import analyze_log

def test_analyze_log(log_text: str):
    result = analyze_log(log_text)
    print("错误类型", result.error_type)
    print("\n可能原因:")
    for cause in result.possible_causes:
        print("-", cause)
    print("\n解决建议：")
    for suggestion in result.suggestions:
        print("-", suggestion)


if __name__ == "__main__":
    test_analyze_log("HikariPool-1 - Exception during pool initialization")