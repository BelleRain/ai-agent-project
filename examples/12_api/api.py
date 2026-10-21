from pyexpat.errors import messages

from fastapi import FastAPI, HTTPException
from app.services.log_service import analyze_log
from app.models import LogAnalyzeRequest, LogAnalyzeResponse, BatchLogAnalyzeRequest
from app.services.prompt_eval import validate_analysis,validate_business_rules


app = FastAPI(
    title="Java 日志分析器",
    version="0.1.0"
)

# uvicorn log_analyzer.api:app --app-dir src --reload --host 0.0.0.0 --port 8000
# http://127.0.0.1:8000/docs
@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "log-analyzer",
    }


# 注意：注解有无response_model的区别
# response_model明确了返回值的结构
# response_model=LogAnalyzeResponse：FastAPI 接口层使用的响应模型
@app.post(
    "/api/vi/logs/analyze",
    response_model=LogAnalyzeResponse,
)
def analyze_log_api(request: LogAnalyzeRequest):
    try:
        result = analyze_log(request.log_text)
        warnings = validate_analysis(result)
        business_warnings = validate_business_rules(result)
        all_warnings = warnings + business_warnings
        message = "分析成功"
        if all_warnings:
            message = "分析成功，但存在质量提醒：" + "；".join(all_warnings)
        return LogAnalyzeResponse(
            success=True,
            data=result,
            message=message
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"日志分析失败：{exc}"
        )

# 批量接口
@app.post("/api/vi/logs/analyze-batch")
def analyze_batch(request: BatchLogAnalyzeRequest):
    results = []
    for item in request.logs:
        try:
            result = analyze_log(item)
            # warnings = validate_analysis(result)
            # business_warnings = validate_business_rules(result)
            # all_warnings = warnings + business_warnings
            # messages = "分析成功"
            # if all_warnings:
            #     messages = "分析成功，但存在质量提醒：" + ";".join(all_warnings)
            results.append({
                "success": True,
                "data": result,
                "message": "分析成功"
            })
        except Exception as exc:
            results.append({
                "success": False,
                "data": None,
                "message": f"日志分析失败：{exc}"
            })
    return {
        "total": len(request.logs),
        "results": results,
    }




























