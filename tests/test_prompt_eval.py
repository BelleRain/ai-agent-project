
from log_analyzer.log_analyzer import analyze_log
from log_analyzer.prompt_eval import *

def test_validate_analysis():
    result = analyze_log("HikariPool-1 - Exception during pool initialization")
    warnings = validate_analysis(result)
    print(warnings)

def test_score_analysis():
    result = analyze_log("HikariPool-1 - Exception during pool initialization")
    score = score_analysis(result)
    print(score)

if __name__ == "__main__":
    test_validate_analysis()
    print("==================")
    test_score_analysis()

