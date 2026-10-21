
from fastapi import FastAPI
from app.routers.log_router import router as log_router


app = FastAPI(
    title="Java 日志分析器",
    version="0.2.0",
)

@app.get("/health")
def health():
    return {
        "status":"UP",
        "service":"log-analyzer"
    }

app.include_router(log_router)