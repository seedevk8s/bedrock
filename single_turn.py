import boto3
from botocore.exceptions import ClientError


while True:
    user_input = input("사용자 >>> ")
    if user_input.lower() in ["종료", "exit", "quit"]:
        print("대화를 종료합니다.")
        break


    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.nova-micro-v1:0"
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_input}],
        }
    ]


    try:
        response = client.converse(
            modelId=model_id,
            system=[{"text": "당신은 친절한 AI 비서입니다."}],
            messages=conversation,
            inferenceConfig={"maxTokens": 1000, "temperature": 0.5},
        )
        response_text = response["output"]["message"]["content"][0]["text"]


        print(f"AI비서 >>> {response_text.strip()}\n")
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
