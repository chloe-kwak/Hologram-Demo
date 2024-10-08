import boto3
#Anthropic Claude를 사용하여 응답 생성하기
def get_response_from_model(prompt_content, image_bytes, mask_prompt=None):
    session = boto3.Session()
    
    bedrock = session.client(service_name='bedrock-runtime') #creates a Bedrock client
    
    image_message = {
        "role": "user",
        "content": [
            { "text": "Image 1:" },
            {
                "image": {
                    "format": "jpeg", #this doesn't seem to matter
                    "source": {
                        "bytes": image_bytes #Base64 인코딩이 필요하지 않습니다!
                    }
                }
            },
            { "text": prompt_content }
        ],
    }
    
    response = bedrock.converse(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[image_message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.9
        },
    )
    
    output = response['output']['message']['content'][0]['text']
    
    return output


