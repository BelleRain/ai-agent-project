from pathlib import Path
from dotenv import load_dotenv
import os

#config.py 所在目录
BASE_DIR = Path(__file__).resolve().parents[1]

# #加载根目录下的 .env
# # /：路径拼接运算符
load_dotenv(BASE_DIR / ".env")

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
# MODEL_NAME = os.getenv("MODEL_NAME")

class Settings:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model_name = os.getenv("MODEL_NAME", "")

    # 单次请求超时（秒）。SDK 默认 600 秒太放纵，一个卡住的请求能挂 10 分钟
    timeout = float(os.getenv("TIMEOUT", "60"))

    # 失败重试次数，总尝试次数 = max_retries + 1
    # SDK 默认只有 2 次，累计退避约 0.5+1.0 = 1.5 秒 —— 跨不过 deepseek 的繁忙窗口
    # 设为 5 则累计退避约 0.5+1+2+4+8 ≈ 15.5 秒
    max_retries = int(os.getenv("MAX_RETRIES", "5"))

    # temperature = float(os.getenv("TEMPERATURE", "0"))
    # max_tokens = int(os.getenv("MAX_TOKENS", "800"))

    prompt_version = os.getenv("PROMPT_VERSION", "v1")


settings = Settings()


# 测试参数
# print(__file__)
# print(BASE_DIR)
# print(TAVILY_API_KEY)
# print(OPENAI_API_KEY)
# print(MODEL_ID)
# print(OPENAI_BASE_URL)

























