from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory

# 언어 모델 생성
model = ChatBedrock(model_id="amazon.nova-micro-v1:0")    #amazon.nova-micro-v1:0

# 대화 내용을 기록할 리스트
#messages = [SystemMessage(content="당신은 사용자를 도와주는 친절한 상담사입니다.")]
chat_history = ChatMessageHistory()
chat_history.add_message(SystemMessage(content="당신은 사용자를 도와주는 친절한 상담사입니다."))

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    chat_history.add_user_message(user_input)

    ai_message = model.invoke(chat_history.messages)
    chat_history.add_message(ai_message)

    print(f"상담사: {ai_message.content}")
    print()

# 사용자와 LLM이 주고 받은 내용(히스토리)을 출력
print(">" * 50)
for i, msg in enumerate(chat_history.messages):
    print(f"{i:<3} {msg.__class__.__name__:<15} {msg.content[:50]}")
print("<" * 50)
print()
