# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI

client = OpenAI(api_key="sk-5b08c3bc0be44cf7a4826d5e77c473ba", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": 
            """
            你的知识库最新更新到什么时候的？
            
            """
        },
        # {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
