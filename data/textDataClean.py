import os
from openai import OpenAI
import Config.config as config
import json
import pandas as pd


def read_md_files(directory,saveEventFilePath):
    # 遍历指定目录
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()  # 读取所有内容
                title = filename.replace(".md","")
                print(f"研报标题:{title}")
                print(f"研报字数:{len(text)}")
                result_list = getEvents(title,text)
                df = pd.DataFrame(result_list)
                savePath = f'{saveEventFilePath}/{title}_event_list.xlsx'
                df.to_excel(savePath, index=True)
                print(f"Event数据 已保存在 {savePath}")
                print("-" * 50)

def getEvents(title,text):
    event_list = []
    text_sections = text.split("##")  # 按照小节将文本分为若干个片段
    count_section = 1
    for i in range(len(text_sections)):
        section = text_sections[i]
        if len(section) < 30:
            continue
        else:
            print("-" * 15 + f"[{count_section}]" + "-" * 10)
            print("text：")
            print(section)
            print("json result:")

            try:
                result = sortResearchReportToJson(title, section)
                result = result.replace("```", "").replace("json", "")
                result_json = json.loads(result)
                for event in result_json['events']:
                    print(f"event_date:{event['event_start_date']}-{event['event_end_date']}, topic:{event['topic']}, content:{event['content']}, type:{event['type']},type_region:{event['type_region']}")
                    event_list.append(event)
            except Exception as e:
                print(f"获取json结果出现了错误:{e}")
            count_section += 1
    return event_list

    # print("数据处理完成")




def sortResearchReportToJson(title,text):
    prompt = f"""
        你是一台从提供的研报文本中提取信息的AI系统。
        你的任务是整理研报中重要的事件+时间节点，并将信息转化成树状JSON列表，其中包含完整且未经修改的信息块。
        
        这篇研报的内容是：
        标题: {title}
        内容: {text}
        
        以下是输出格式的详细要求和示例:
        1. **完整切片**，一字不漏。
        2. **不需要解释或任何多余的输出**。
        3. 不要输出研报中任何 "预测" "预计" 的信息，输出的所有事件必须是已经发生的事情。
        4. 输出尽可能完整，要求如下:
        (1)**标准JSON**:输出的格式必须是标准的JSON，不需要包含任何解释性或额外的文本。结构化:构建树状JSON结构，叶节点为“内容”
        (2) 不要输出类似这样的 ：json:```json ``` 请您直接给出json字符串!
        (3)如果文本中含有明显的结构标志(如标题、子标题)，利用这些标志帮助结构化JSON输出。确保每个“内容”字段内的文本是自包含的，能够独立传达完整的信息。提高准确性和避免遗漏，确保每个知识片段都被正确分类和标记。格式参考:

        {{
            "report_title":"",//研报名称，例如：2022年2月报-铁矿石
            "events": // 研报中重要的事件+时间节点
            [
                {{
                    "event_start_date": "xxxx年xx月xx日", // 事件或信息的开始时间节点。请您严格按照 YYYY年M月D日的格式输出，如：2021年4月13日。例如，如果一件事情发生于2024年1月-11月，则该项输出为 2024年1月1日
                    "event_end_date": "xxxx年xx月xx日", // 事件或信息的结束时间节点。请您严格按照 YYYY年M月D日的格式输出，例如：2021年4月15日。例如，如果一件事情发生于2024年1月-11月，则该项输出为 2024年11月30日 
                    "topic":"",// 该事件的内容概括（即content属性的内容概要，要求不多于50字）
                    "content": "", // 该事件的内容
                    "type": "",// 该事件的类型；取值范围为：[价格走势、政策信息、供给端动态、需求端动态、供需关系]
                    "type_region":""// 该事件的范围；取值范围为:[国内信息，国外信息]
                }}
            ]
        }}
        
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
directory_path = '2022/markdown'  # 替换为你的目录路径
saveEventFilePath = '2022/markdown' # 当前路径
read_md_files(directory_path,saveEventFilePath)



