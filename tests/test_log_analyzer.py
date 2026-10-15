
from log_analyzer.log_analyzer import analyze_log

def test_analyze_log(log_text: str):
    result = analyze_log(log_text)
    print("错误类型", result.error_type)
    print("\n可能原因:")
    for cause in result.possible_causes:
        print("-", cause)
    print("\n解决建议：")
    for suggestion in result.suggestions:
        print("-", suggestion)

def test_analyze_log_11(log_text: str):
    result = analyze_log(log_text)
    print(result.model_dump_json(indent=2,ensure_ascii=False))


if __name__ == "__main__":
    # test_analyze_log("HikariPool-1 - Exception during pool initialization")
    # log = """
    # SLF4J: Class path contains multiple SLF4J bindings.
    # SLF4J: Found binding in [jar:file:/data/app/jar/DSMP-V4.0.0/api-server/libs/inceptor-argodb-driver-8.31.2.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    # SLF4J: Found binding in [jar:file:/data/app/jar/DSMP-V4.0.0/api-server/libs/logback-classic-1.2.11.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    # SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
    # SLF4J: Actual binding is of type [org.slf4j.impl.Log4jLoggerFactory]
    # Exception in thread "main" java.lang.IllegalArgumentException: LoggerFactory is not a Logback LoggerContext but Logback is on the classpath. Either remove Logback or the competing implementation (class org.slf4j.impl.Log4jLoggerFactory loaded from file:/data/app/jar/DSMP-V4.0.0/api-server/libs/inceptor-argodb-driver-8.31.2.jar). If you are using WebLogic you will need to add 'org.slf4j' to prefer-application-packages in WEB-INF/weblogic.xml:
    # """
    test_analyze_log_11("HikariPool-1 - Exception during pool initialization")
