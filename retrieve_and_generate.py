import boto3

bedrock_agent_runtime = boto3.client(service_name="bedrock-agent-runtime")


def retrieve(query, kbId, numberOfResults=3):
    return bedrock_agent_runtime.retrieve_and_generate(
        input={
            "text": query,
        },
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kbId,
                "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0",
            },
        },
    )


if __name__ == "__main__":
    response = retrieve(
        query="iphone-17-pro-max의 특징은 어떻게 되지?",
        kbId="RVYNXA3ZUK",
        numberOfResults=3,
    )
    print(response)

    citations = response["citations"]
    for citation in citations:
        for idx, ref in enumerate(citation["retrievedReferences"]):
            print(f"\n[{idx+1}] 검색 결과")
            print(f"내용 >>> {ref["content"]["text"][:50]}...")
            print(f"출처 >>> {ref["location"]["s3Location"]["uri"]}")
    print(f"\n답변 >>> {response["output"]["text"]}")
