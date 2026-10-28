

from app.prompts import PROMPT_REGISTRY

TEST_LOGS = [
    "HikariPool-1 - Exception during pool initialization",
    "No Feign Client for loadBalancing",
    "zookeeper connect timeout",
    "NettyRemotingServer bind fail",
]

def print_prompt_diff() -> None:
    v1 = PROMPT_REGISTRY["v1"]
    v2 = PROMPT_REGISTRY["v2"]

    print("========v1========")
    print(v1["system"])
    print(v1["user_template"])

    print("========v2=========")
    print(v2["system"])
    print(v2["user_template"])

if __name__ == "__main__":
    print_prompt_diff()