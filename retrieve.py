import boto3

bedrock_agent_runtime = boto3.client(service_name="bedrock-agent-runtime")


def retrieve(query, kbId, numberOfResults=3):
    response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=kbId,
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": numberOfResults}
        },
        retrievalQuery={"text": query, "type": "TEXT"},
    )

    print("-" * 50)
    print(response)
    print("-" * 50)
    print()

    return response


if __name__ == "__main__":
    response = retrieve(
        query="아이폰 17 프로 맥스의 특징은 어떻게 되지?",
        kbId="RVYNXA3ZUK",
        numberOfResults=3,
    )

    results = response["retrievalResults"]
    for idx, ref in enumerate(results):
        print(f"[{idx+1}] 검색된 내용: {ref['content']['text'][:100]}...")
        print(f"출처 >>> {ref['location']['s3Location']['uri']}\n")
