from openai import OpenAI
import Config.config as config

client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "请您为我制作一个上海3天的旅行计划。"},
    ],
    max_tokens=1024,
    temperature=0.1,
    stream=False
)

print(response.choices[0].message.content)