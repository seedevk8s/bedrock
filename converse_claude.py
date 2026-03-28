import boto3
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="us-east-1")

#model_id = "anthropic.claude-3-haiku-20240307-v1:0"
model_id = "amazon.nova-lite-v1:0"

image_path = "./data/sample.png"
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()

user_message = "서문 없이 이미지를 분석한 결과를 작성해 주세요."
conversation = [
    {
        "role": "user",
        "content": [
            {"text": user_message},
            {"image": {"format": "png", "source": {"bytes": image_bytes}}},
        ],
    }
]

try:
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={  # 모든 모델에 공통적인 추론 파라미터를 지정
            "maxTokens": 4096,
            "temperature": 0.5,
            "topP": 0.9,
        },
    )
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
