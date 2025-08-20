# 로깅 기능을 위한 모듈 가져오기
import logging

# FastMCP 서버를 사용하기 위한 클래스 가져오기
from mcp.server.fastmcp import FastMCP

# 로깅 설정 : INFO 레벨 이상의 로그를 출력
logging.basicConfig(level=logging.INFO)

# MCP 서버 인스턴스 생성
mcp = FastMCP("Math")

# 도구 1: 더하기 함수
@mcp.tool()
def add(a, b) -> int:
    """더하기"""
    try:
        a = int(a)
        b = int(b)
        logging.info(f"Adding {a} and {b}") # 로그 출력
        return a + b
    except Exception as e:
        # 예외 발생 시 에러 로그 출력 후 다시 예외 발생시킴
        logging.error(f"Invalid input in add: {a}, {b} - {e}")
        raise

# 도구 2: 뺴기 함수
@mcp.tool()
def Subtract(a, b) -> int:
    """빼기"""
    try:
        a = int(a)
        b = int(b)
        logging.info(f"Subtracting {a} and {b}") # 로그 출력
        return a - b
    except Exception as e:
        # 예외 발생 시 에러 로그 출력 후 다시 예외 발생시킴
        logging.error(f"Invalid input in subtract: {a}, {b} - {e}")
        raise

# MCP 서버를 stdio 방식으로 실행
if __name__ == "__main__":
    mcp.run(transport="stdio")