from app.prompts import v1,v2

PROMPT_REGISTRY = {
    "v1":{
        "system":v1.SYSTEM_PROMPT,
        "user_template":v1.USER_PROMPT_TEMPLATE,
    },
    "v2":{
        "system":v2.SYSTEM_PROMPT,
        "user_template":v2.USER_PROMPT_TEMPLATE,
    }
}