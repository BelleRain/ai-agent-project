

TEST_CASES = [
    {
        "id": "db_pool_init",
        "log_text": (
            "HikariPool-1 - Exception during pool initialization"
        ),
        "expected_keywords": ["数据库", "连接"],
    },
    {
        "id": "feign_client_missing",
        "log_text": "No Feign Client for loadBalancing",
        "expected_keywords": ["Feign","客户端"],
    },
    {
        "id": "zk_timeout",
        "log_text": "zookeeper connect timeout",
        "expected_keywords": ["ZooKeeper", "连接"],
    },
    {
        "id": "port_bind_fail",
        "log_text": (
            "NettyRemotingServer bind fail, address already in use"
        ),
        "expected_keywords": ["端口", "占用"],
    }
]