"""
AWS Bedrock + LangChain + Streaming Chat Example

요구사항 반영:
1) ChatBedrock 사용
2) ChatMessageHistory 사용
3) 가장 먼저 SystemMessage 추가
4) 무한 루프 채팅
5) exit 입력 시 종료
6) .stream() 사용
7) 각 청크 사이에 | 추가, 즉시 flush
8) 매 턴 전체 대화 기록 전달
9) 완성된 응답은 AIMessage로 history에 저장
"""

from langchain_aws import ChatBedrock
from langchain_core.chat_history import InMemoryChatMessageHistory as ChatMessageHistory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


def chunk_to_text(chunk) -> str:
    """
    LangChain 스트리밍 청크에서 실제 텍스트를 안전하게 추출합니다.
    모델/버전에 따라 chunk.content 형태가 문자열 또는 리스트일 수 있으므로 대응합니다.
    """
    content = getattr(chunk, "content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                # 예: {"type": "text", "text": "..."}
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
        return "".join(parts)

    return str(content) if content is not None else ""


def main():
    # 1) ChatBedrock 초기화
    # region_name은 실제 Bedrock 사용 가능 리전으로 지정해야 합니다.
    # 예: us-east-1, us-west-2, ap-northeast-1 등
    llm = ChatBedrock(
        model_id="amazon.nova-micro-v1:0",
        region_name="us-east-1",
        model_kwargs={
            "temperature": 0.7,
            "maxTokens": 1024,
        },
    )

    # 2) ChatMessageHistory 생성
    history = ChatMessageHistory()

    # 3) SystemMessage를 가장 먼저 추가
    history.add_message(
        SystemMessage(content="당신은 사용자를 도와주는 친절한 상담사입니다.")
    )

    print("채팅을 시작합니다. 종료하려면 exit 를 입력하세요.")

    # 4) 무한 루프
    while True:
        user_input = input("\n사용자: ")

        # 5) exit 입력 시 종료 (대소문자 구분)
        if user_input == "exit":
            print("프로그램을 종료합니다.")
            break

        # 사용자 메시지를 먼저 history에 추가
        history.add_message(HumanMessage(content=user_input))

        print("AI: ", end="", flush=True)

        full_response = ""
        first_chunk = True

        # 8) 현재까지의 모든 대화 기록을 모델에 전달
        # 6) .stream() 사용
        for chunk in llm.stream(history.messages):
            text = chunk_to_text(chunk)

            # 빈 청크는 건너뜀
            if not text:
                continue

            # 7) 각 청크 사이에 | 구분자 추가 + 즉시 출력
            if not first_chunk:
                print("|", end="", flush=True)

            print(text, end="", flush=True)

            full_response += text
            first_chunk = False

        print()  # 응답 한 줄 종료

        # 9) 완성된 최종 응답을 AIMessage로 저장
        history.add_message(AIMessage(content=full_response))


if __name__ == "__main__":
    main()