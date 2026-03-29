import boto3
from datetime import datetime
import pytz
import streamlit as st

st.title("함수를 이용하는 챗봇")
st.write("---")


# 현재 날짜와 시간을 "YYYY-MM-DD HH:MI:SS" 형식으로 반환하는 함수
def get_current_time(timezone: str = "Asia/Seoul"):
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"{now} ({timezone})"


# 함수 호출을 위한 메타데이터
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_current_time",
                "description": "현재 날짜와 시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 반환합니다.",
                "inputSchema": {
                    "json": {
                        "type": "object", 
                        "properties": {
                            "timezone": {
                                "type": "string", 
                                "description": "현재 날짜와 시간을 반환할 타임존을 입력하세요. (예: Asia/Seoul)"
                            }
                        }, 
                        "required": ["timezone"]
                    }
                },
            }
        }
    ]
}


client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.nova-micro-v1:0"
system_prompt = "당신은 친절한 AI 비서로, 모든 질문에 대해 한국어로 답변합니다."

# # 대화 내용을 기록
# messages = []

# 대화 내용을 기록할 저장 공간을 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 화면 출력을 위한 대화 내용 { "role": "...", "content": "..." }
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# 대화 내용을 화면에 출력
for msg in st.session_state.conversation:
    print(msg)
    st.chat_message(msg["role"]).write(msg["content"])

# 모델에 질의하고 결과를 반환하는 함수
def get_ai_response():
    print("messages >>> ...")
    for i, msg in enumerate(st.session_state.messages):
        print(f"{i}\t{msg}")
    print()

    response = client.converse(
        modelId=model_id,
        system=[{"text": system_prompt}],
        messages=st.session_state.messages,
        toolConfig=tool_config,
    )

    print("... >>> response.output.message")    
    print(response["output"]["message"])
    return response




# while True:
#     user_input = input("사용자 >>> ")
#     if user_input.lower() in ["종료", "exit", "quit"]:
#         print("대화를 종료합니다.")
#         break
if user_input := st.chat_input():
    # 사용자 입력을 화면에 출력
    st.chat_message("user").write(user_input)
    st.session_state.conversation.append(
        {
            "role": "user",
            "content": user_input,
        }
    )
    st.session_state.messages.append(
        {
            "role": "user",
            "content": [{"text": user_input}],
        }
    )


    response = get_ai_response()
    output_message = response["output"]["message"]
    st.session_state.messages.append(output_message)

    # 도구 사용이 요청된 경우 => 도구를 호출(실행)하고 결과를 모델에 다시 전송
    if response["stopReason"] == "tool_use":

        # 모든 도구 실행 결과를 저장할 리스트 
        tool_results_list = []

        tool_requests = response["output"]["message"]["content"]
        for tool_request in tool_requests:
            if "toolUse" in tool_request:
                tool = tool_request["toolUse"]

                if tool["name"] == "get_current_time":
                    timezone = tool["input"].get("timezone", "Asia/Seoul")
                    tool_result = {
                        "toolUseId": tool["toolUseId"],
                        "content": [{"json": {"current_time": get_current_time(timezone=timezone)}}]
                    }

                    # 도구 실행 결과를 추가
                    tool_results_list.append({"toolResult": tool_result})

        if tool_results_list: 
            tool_result_message = {
                "role": "user", 
                "content": tool_results_list # [{"toolResult": tool_result}],
            }

            st.session_state.messages.append(tool_result_message)

            # 함수 호출(실행) 결과를 모델에 전달
            response = get_ai_response()
            output_message = response["output"]["message"]
            st.session_state.messages.append(output_message)
        
    # 최종 응답 출력
    for content in output_message["content"]:
        print(f"AI >>> {content["text"]}\n")

        #최종 답변을 화면에 출력
        st.chat_message("assistant").write(content["text"])
        st.session_state.conversation.append(
            {
                "role": "assistant", 
                "content": content["text"]
            }
        )
