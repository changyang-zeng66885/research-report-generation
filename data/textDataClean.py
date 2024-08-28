import os
#import Config.config as config

def read_md_files(directory):
    # 遍历指定目录
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()  # 读取所有内容
                title = filename.replace(".md","")
                print(f"title:{title}")
                print(f"len:{len(text)}")
                # result = sortResearchReportToJson(title,text)  
                # print("数据处理完成")
                print("-"*30)


def sortResearchReportToJson(title,text):
    prompt = f"""
        你是一台从提供的研报文本中提取信息的AI系统。你的任务是整理研报中重要的事件+时间节点，并将信息转化成树状JSON列表，其中包含完整且未经修改的信息块。以下是详细要求和示例:
        1. **完整切片**，一字不漏。
        2. **不需要解释或任何多余的输出**。
        3. 输出尽可能完整，要求如下:
        (1)**标准JSON**:输出的格式必须是标准的JSON，不需要包含任何解释性或额外的文本。结构化:构建树状JSON结构，叶节点为“内容”
        (2)如果文本中含有明显的结构标志(如标题、子标题)，利用这些标志帮助结构化JSON输出。确保每个“内容”字段内的文本是自包含的，能够独立传达完整的信息。提高准确性和避免遗漏，确保每个知识片段都被正确分类和标记。格式参考:

        ```json
        {{
            "report_title":"",//研报名称，例如：2022年2月报-铁矿石
            "events": // 研报中重要的事件+时间节点
            [
                {{
                    "event_date": "xxxx年xx月xx日", // 事件或信息的时间节点，例如：2021年，2021年4月 2021年4月13日
                    "topic":"",// 该事件的内容概括（即content属性的内容概要，要求不多于50字）
                    "content": "", // 该事件的内容
                    "type": "",// 该事件的类型；取值范围为：[价格走势、政策信息、供给端动态、需求端动态、供需关系]
                    "type_region":""// 该事件的范围；取值范围为:[国内信息，国外信息]
                }}
            ]
        }}
        
        这篇研报的内容是：
        标题: {title}
        内容: {text}
        
    """

    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        stream=False
    )
    
    return response.choices[0].message.content


# 使用示例
directory_path = 'data/2022/markdown'  # 替换为你的目录路径
read_md_files(directory_path)