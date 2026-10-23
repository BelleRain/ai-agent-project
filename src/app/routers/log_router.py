
import uuid
from fastapi import APIRouter, HTTPException

from app.exceptions import LLMServiceError,StructuredOutputError
from app.services.log_service import analyze_log
from app.models import *

# @app.post: FastAPI 实例,直接在应用中注册接口,常见位置：main.py
# @router.post: APIRouter 实例,将接口组织到独立路由模块,常见位置：routers/log_router.py
router = APIRouter(
    prefix="/api/v1/logs",
    tags=["日志分析"],
)


@router.post('/analyze',response_model = ApiResponse)
def analyze_log_api(request: LogAnalyzeRequest):
    # try:
        result_id = str(uuid.uuid4())
        result = analyze_log(request.log_text)
        return ApiResponse(
            success=True,
            data=result,
            message=f"分析成功,request_id={result_id}"
        )
    # 同一组 except 只负责处理
    # try 代码块抛出的异常，不负责捕获其自身处理器中再次抛出的异常。
    # except LLMServiceError as exc:
    #     raise HTTPException(
    #         status_code=502,
    #         detail=str(exc),
    #     )
    # except StructuredOutputError as exc:
    #     raise HTTPException(
    #         status_code=422,
    #         detail=str(exc)
    #     )
    # except Exception as exc:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="服务内部错误",
    #     ) from exc


@router.post("/analyze-batch",
          response_model = BatchLogAnalyzeResponse)
def analyze_batch(request: BatchLogAnalyzeRequest):
    results = []
    success_count = 0
    failure_count = 0

    for item in request.logs:
        try:
            result = analyze_log(log_text=item)
            results.append(
                BatchItemResult(
                    success=True,
                    data=result,
                    message="分析成功"
                )
            )
            success_count += 1

        except Exception as exc:
            results.append(
                BatchItemResult(
                    success=False,
                    message=str(exc)
                )
            )
            failure_count += 1

    return BatchLogAnalyzeResponse(
        total=len(request.logs),
        success_count=success_count,
        failure_count=failure_count,
        results=results
    )

























