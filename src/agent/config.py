from pathlib import Path
from dotenv import load_dotenv
import os

#config.py 所在目录
BASE_DIR = Path(__file__).resolve().parents[2]

#加载根目录下的 .env
# /：路径拼接运算符
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")


# 测试参数
# print(__file__)
# print(BASE_DIR)
# print(TAVILY_API_KEY)
# print(OPENAI_API_KEY)
# print(MODEL_ID)
# print(OPENAI_BASE_URL)

























