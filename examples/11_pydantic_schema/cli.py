
# log_service.py ：调用模型
# prompt_eval.py ：结果校验和评分
# cli.py ：用户交付
# PYTHONPATH=src python -m log_analyzer.cli --log "HikariPool-1 - Exception during pool initialization"

import argparse

from app.services.log_service import *
from app.services.prompt_eval import *


def main():
    parser = argparse.ArgumentParser(
        description="Java 错误日志分析器"
    )

    parser.add_argument(
        "--log",
        # required=True,
        help="要分析的错误日志"
    )

    # 增加文件输入模式
    # 新增可选参数
    parser.add_argument(
        "--file",
        help = "从文件中逐行读取日志",
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file,"r",encoding="utf-8") as file:
            logs = [line.strip() for line in file if line.strip()]
        for log in logs:
            print (f"\n正在分析：{log}")
            try:
                result = analyze_log(log)
                print(result.model_dump_json(indent=2, ensure_ascii=False))
            except Exception as exc:
                print("分析失败：",exc)

    else:
        try:
            result = analyze_log(args.log)
            warnings = validate_analysis(result)
            score = score_analysis(result)
            business_warnings = validate_business_rules(result)
            print("\n========== 分析结果 ==========")
            print("错误类型：",result.error_type)
            print("\n可能原因")
            for cause in result.possible_causes:
                print("-",cause)
            print("\n解决建议：")
            for suggestion in result.suggestions:
                print("-",suggestion)
            print("\n质量评分：", score)
            if warnings:
                print("\n质量提醒：")
                for warning in warnings:
                    print("-",warning)
            else:
                print("\n结果通过基础质量检查")
            if business_warnings:
                print("\n业务校验提醒：")
                for warning in business_warnings:
                    print("-",warning)

        except Exception as exc:
            print(f"分析失败：{exc}")


if __name__ == "__main__":
    main()











































