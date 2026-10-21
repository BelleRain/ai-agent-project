import os
import sys

# 直接 `python tests/test_conn.py` 也能跑：把 src 加进模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from config import settings
from openai import OpenAI


def mask(key: str | None) -> str:
    if not key:
        return "<未设置>"
    return f"{key[:6]}...{key[-4:]} (len={len(key)})"


print("=== 环境检查 ===")
print("base_url :", settings.base_url)
print("model    :", settings.model_name)
print("api_key  :", mask(settings.api_key))
for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "NO_PROXY"):
    if os.getenv(name):
        print(f"proxy {name} = {os.getenv(name)}")

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,  # 走 .env，默认 5 次；调成 0 可逼出真实的 503
)

print(f"timeout  : {settings.timeout}s")
print(f"重试次数 : {settings.max_retries}")

print("\n=== 开始测试 API ===")
try:
    response = client.chat.completions.create(
        model=settings.model_name,
        messages=[{"role": "user", "content": "请只回复：OK"}],
        timeout=settings.timeout,
    )
    print("API 返回成功")
    print(response.choices[0].message.content)
except Exception as e:
    # 503 的关键信息在响应体里，必须打出来才知道是谁返回的
    print(f"\n调用失败: {type(e).__name__}")
    print("message :", e)
    print("status  :", getattr(e, "status_code", None))
    print("request :", getattr(getattr(e, "request", None), "url", None))
    body = getattr(e, "response", None)
    if body is not None:
        print("headers :", dict(body.headers))
        print("body    :", body.text)
    raise
