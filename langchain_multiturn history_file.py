from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import FileChatMessageHistory

model = ChatBedrock(model_id="amazon.nova-micro-v1:0")      # 

chat_history = FileChatMessageHistory(file_path="./data/history.json")
chat_history.add_message(
    SystemMessage(content="당신은 사용자를 도와주는 친절한 상담사입니다.")
)

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    chat_history.add_user_message(user_input)

    ai_message = model.invoke(chat_history.messages)
    chat_history.add_message(ai_message)

    print(f"상담사: {ai_message.content}")
    print()


print(">" * 50)
for i, msg in enumerate(chat_history.messages):
    print(f"{i:<3} {msg.__class__.__name__:<15} {msg.content[:50]}")
print("<" * 50)
print()
