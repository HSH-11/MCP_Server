# MCP 서버 및 도구 실행 시 context 정보 처리
from mcp.server.fastmcp import FastMCP, Context
from langchain_openai import ChatOpenAI # OpenAI의 LLM을 랭체인 인터페이스로 사용하기 위한 클래스
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# MCP 서버 초기화 ("GPT-4o MCP"는 서버 식별 이름이며, 클라이언트에 표시됨)
mcp = FastMCP("GPT-4o MCP")

# GPT-4o 질문에 보내는 도구 정의
@mcp.tool()
async def ask_gpt(ctx: Context, question: str) -> str: # context : 요청 정보나 사용자 세션 같은 내용이 담김. 로그를 남기거나 대화 내용을 저장할 때 활용
    # GPT-4o 모델 인스턴스 생성 (온도는 0.3으로 설정)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    # 사용자의 질문을 모델에 전달하고 결과를 반환
    return llm.invoke(question)

# MCP 서버 실행 (stdio 표준 입출력 기반으로 통신)
if __name__ == "__main__":
    mcp.run(transport="stdio")