from pyexpat.errors import messages

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppBaseError
from app.models import ErrorResponse
from app.routers.log_router import router as log_router


app = FastAPI(
    title="Java 日志分析器",
    version="0.3.0",
)

@app.exception_handler(AppBaseError)
async def app_error_handler(
    request: Request,
    exc: AppBaseError
):
    status_code = 502

    if exc.error_code == "STRUCTURED_OUTPUT_ERROR":
        status_code = 422

    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
        ).model_dump()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="请求参数校验失败"
        ).model_dump()
    )

@app.exception_handler(Exception)
async def unknown_exception_handler(
        request: Request,
        exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="服务内部错误"
        ).model_dump()
    )


@app.get("/health")
def health():
    return {
        "status":"UP",
        "service":"log-analyzer"
    }

app.include_router(log_router)