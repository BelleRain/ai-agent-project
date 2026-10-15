
import json
from openai import OpenAI
from pydantic import ValidationError

from agent.config import settings
from log_analyzer.models import ErrorAnalysis
from log_analyzer.prompts import *


client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,
)


def analyze_log(log_text: str) -> ErrorAnalysis:
    user_prompt = USER_PROMPT_TEMPLATE.format(log_text=log_text)
    response = client.chat.completions.create(
        model = settings.model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
              "role":"user",
              "content": user_prompt
            },
        ],
        response_format={"type": "json_object"}
        # temperature=settings.temperature,
        # max_tokens=settings.max_tokens,
    )

    content = response.choices[0].message.content
    if not content or not content.strip():
        raise ValueError("模型返回内容为空")
    try:
        data = json.loads(content)
        return ErrorAnalysis.model_validate(data)
    # 非法JSON
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"模型返回的内容不是合法JSON ：{content}"
        ) from exc
    #字段异常
    except ValidationError as exc:
        raise ValueError(
            f"模型返回字段不符合要求：{content}"
        ) from exc



























