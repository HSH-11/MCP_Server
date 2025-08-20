# MCP Server Labs with Cursor AI

나만의 MCP 서버 구축/실습 모음<br>
Cursor와 MCP를 연동해 다양한 도구(Math, 파일검색, PDF/오피스 RAG, 웹 검색 요약, SSE 기반 챗봇, Function Calling)를 단계적으로 구현합니다.

추가적으로 스미더리에서 MCP 서버를 불러오는 작업을 수행합니다.<br>

- Sequential Thinking
- Tavily
- Brave Search

또한 이 과정을 ClaudeDesktop에서도 실습합니다.

## 사용 API
- OpenAI API
- Tavily API : 웹 검색 결과를 실시간으로 가져와 요약 및 정리해주는 LLM용 검색 API
- Brave Search API : 사용자의 정보를 수집하지 않으면서 필요한 정보를 찾아주는 안전하고 빠른 검색 엔진
- Google maps API : 지도 보기, 길 찾기, 주변 장소 검색 등 제공

## 폴더 구조

```
MCP_Server/
  ├─ Call_Weather_API.py              # OpenAI Function Calling + OpenWeather API 데모
  ├─ Cursor/
  │  ├─ order.py                      # 주문 객체 생성 유틸
  │  └─ payment.py                    # 결제/배송/영수증 처리 유틸
  ├─ explorer-server/
  │  └─ main.py                       # C:/ 전체 파일명 검색 MCP 서버(File-Search)
  ├─ math-server/
  │  └─ math_server.py                # 사칙연산 도구 MCP 서버(Math)
  ├─ rag-server/
  │  ├─ main.py                       # PDF 기반 RAG MCP 서버(PDF-RAG)
  │  ├─ office.py                     # Word/Excel 기반 RAG MCP 서버(Office-RAG)
  │  ├─ 스마트팜.pdf
  │  └─ office/
  │     ├─ 미세먼지가 치매에 미치는 영향.docx
  │     ├─ 자동차_리뷰.xlsx
  │     ├─ 책_리뷰.xlsx
  │     └─ 한옥의 장점과 단점.docx
  ├─ test-server/
  │  ├─ function_calling.py           # LangChain Tool + OpenAI Functions 에이전트 데모
  │  ├─ main.py                       # 간단 인사 스크립트
  │  ├─ mcp_basic.py                  # 최소 MCP 서버(add) 예제
  │  ├─ mcp_client.py                 # SSE 클라이언트 예제(직접 함수 호출 데모 포함)
  │  ├─ mcp_sample.py                 # (샘플 예제 파일)
  │  ├─ mcp_server.py                 # GPT-4o MCP 서버(ask_gpt)
  │  ├─ pyproject.toml                # test-server 의존성 정의 예시
  │  ├─ sse_client.py                 # SSE 클라이언트: /sse 엔드포인트 접속
  │  └─ sse_server.py                 # FastAPI + MCP + SSE 서버(chatbot)
  └─ web-search-server/
     └─ main.py                       # Tavily 기반 웹 검색 요약 MCP 서버(WebSearch)
  
```

## 사전 준비

- Python 3.11 이상 권장
- 필수 패키지 설치

```bash
pip install -U \
  mcp \
  langchain langchain-openai langchain-community \
  chromadb \
  python-dotenv requests \
  pandas openpyxl python-docx \
  fastapi uvicorn

# 함수호출/날씨 데모에 필요
pip install -U openai
```

- 환경 변수(.env) 설정 예시

```
OPENAI_API_KEY=sk-...        # OpenAI 키
TAVILY_API_KEY=tvly-...      # Tavily 웹 검색 API 키
```

## Cursor 연동(MCP 서버 등록)

`c:\Users\user\.cursor\mcp.json` 예시:

```json
{
  "mcpServers": {
    "math-server": {
      "command": "C:/Users/user/anaconda3/python.exe",
      "args": ["C:/Users/user/MCP_Server/math-server/math_server.py"]
    },
    "rag-server": {
      "command": "C:/Users/user/anaconda3/python.exe",
      "args": ["C:/Users/user/MCP_Server/rag-server/main.py"]
    },
    "file-search": {
      "command": "C:/Users/user/anaconda3/python.exe",
      "args": ["C:/Users/user/MCP_Server/explorer-server/main.py"]
    },
    "office-server": {
      "command": "C:/Users/user/anaconda3/python.exe",
      "args": ["C:/Users/user/MCP_Server/rag-server/office.py"]
    },
    "web-search": {
      "command": "C:/Users/user/anaconda3/python.exe",
      "args": ["C:/Users/user/MCP_Server/web-search-server/main.py"]
    },
    "mcp-sequentialthinking-tools": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@xinzhongyouhai/mcp-sequentialthinking-tools",
        "--key",
        "key"
      ]
    },
    "brave-search": {
        "command": "npx",
        "args": [
            "-y",
            "@smithery/cli@latest",
            "run",
            "@smithery-ai/brave-search",
            "--key",
            "key",
            "--profile",
            "profile"
          ]
        }
  }
}
```

## 각 실습별 실행 및 사용법

### 1) Math MCP 서버 (`math-server/math_server.py`)
- 실행: `python math-server/math_server.py`
- 도구
  - `add(a, b)` 더하기
  - `Subtract(a, b)` 빼기

### 2) 파일 검색 MCP 서버 (`explorer-server/main.py`)
- 실행: `python explorer-server/main.py`
- 도구
  - `find_file(keyword)` → 기본 루트 `C:/`에서 파일명 기준 검색. 필요 시 소스의 `ROOT_DIR` 변경 가능

### 3) PDF RAG MCP 서버 (`rag-server/main.py`)
- 실행: `python rag-server/main.py`
- 도구
  - `ask_pdf(query)` → `rag-server/스마트팜.pdf`를 분할/임베딩 후 검색 기반 응답
- 참고: 다른 PDF를 쓰려면 소스의 `PDF_PATH` 수정

### 4) Office RAG MCP 서버 (`rag-server/office.py`)
- 실행: `python rag-server/office.py`
- 도구
  - `ask_office(query)` → `rag-server/office/` 내 Word/Excel 문서 전체를 로드·분할·임베딩 후 검색 기반 응답
- 요구 패키지: `pandas`, `openpyxl`, `python-docx`

### 5) 웹 검색 요약 MCP 서버 (`web-search-server/main.py`)
- 실행: `python web-search-server/main.py`
- 도구
  - `web_search(query)` → Tavily API로 검색 후 GPT 요약
- 환경 변수: `TAVILY_API_KEY` 필요, OpenAI 키도 필요
- 모델: 기본 `gpt-4`(요약용). 필요 시 `gpt-4o` 등으로 변경 가능

### 6) SSE 기반 챗봇 서버/클라이언트(`test-server/sse_server.py`, `test-server/sse_client.py`)
- 서버 실행: `python test-server/sse_server.py` → `http://127.0.0.1:3000/sse`
- 클라이언트 실행: `python test-server/sse_client.py http://127.0.0.1:3000/sse`
- 도구
  - 서버 내부 MCP 툴 `chat(input)` → GPT-4o 대화

### 7) OpenAI Function Calling + Agent 실습
- LangChain Functions Agent: `python test-server/function_calling.py`
  - 등록된 `add/subtract` 툴을 자동 선택하여 실행
- OpenAI 함수호출 + 날씨 API: `python Call_Weather_API.py`
  - 파일 내 `openai_api_key`, `weather_api_key` 값 설정 필요

### 8) ClaudeDesktop
- Google Map
- Tavily

### 9) 기타 샘플
- `test-server/mcp_basic.py`: 최소 MCP 서버(add) → `python test-server/mcp_basic.py`
- `test-server/mcp_server.py`: GPT-4o MCP 서버(ask_gpt) → `python test-server/mcp_server.py`
- `test-server/mcp_client.py`: 간단 호출 데모(동일 프로세스 호출) → `python test-server/mcp_client.py`

## 실습 목표 요약
- MCP 서버 작성 및 Cursor 연동 방법 이해
- LangChain 기반 RAG 구현(PDF, Word/Excel)
- 외부 검색 API(Tavily) + LLM 요약 파이프라인 구성
- SSE(서버-클라이언트)로 스트리밍 기반 MCP 통신 구현
- https://smithery.ai/에서 mcp 서버 불러오기
- OpenAI Function Calling 및 도구 선택 에이전트 체험

## 트러블슈팅
- OpenAI/Tavily 키 미설정: `.env`에 `OPENAI_API_KEY`, `TAVILY_API_KEY` 추가
- Excel 로딩 오류: `openpyxl` 설치 필요(`pip install openpyxl`)
- Chroma/임베딩 에러: `chromadb`, `langchain-community` 버전 확인 및 재설치
- Windows 경로 문제: 실행 경로/절대경로 확인, `mcp.json`의 파이썬 경로 점검

