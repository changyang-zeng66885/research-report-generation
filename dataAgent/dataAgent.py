from openai import OpenAI
import Config.config as config
import json
# from . import sqlExecuter
import sqlExecuter
import os
# from . import draw
import draw

def load_database_description(file_name):
    # 获取当前脚本文件所在目录
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_sql_query(user_query):
    db_description = load_database_description('tabel_info.md')
    prompt = f"""
    假设你是一名数据科学家，我为您提供了有关铁矿石价格、供给、需求等相关数据
    你需要根据我的数据要求，结合表的描述，生成数据查询的SQL语句。

    **数据库结构**
    ------
    {db_description}
    -------

    **查询要求**
    现在，我需要查询 "{user_query}" 相关的数据
    请您生成 SQL 语句

    **返回值要求**
    1. 返回格式为：json格式，请您不要返回除了json结果以外的任何语句
     [
       {{ "sql":<您的SQL语句1>,"desc":<这条SQL语句查询的内容> }},
       {{ "sql":<您的SQL语句2>,"desc":<这条SQL语句查询的内容> }},
       ....
     ]
    2. 如果有需要，可以返回多条SQL语句 
    3. 如果现有数据表无法满足用户的查询需求，返回示例为：{{ "sql":"","desc":"<无法满足用户的查询需求的原因>" }}, 其中 “< >” 里的内容需要根据实际情况填写
    4. 提供按月或者按年汇总的查询SQL语句，如果不能提供，请在desc属性中给出理由
    5. 如果查询的结果包含时间、日期等属性，请将这些属性作为第一个查询的属性，保证数据表的第一列为时间或者日期。

    """
    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0,
        stream=False
    )
    
    return response.choices[0].message.content
def askDataAgent(user_query):
    sql_results = generate_sql_query(user_query)
    sql_results = sql_results.replace("```", "").replace("json", "")
    results_json = json.loads(sql_results)

    tabels = \
    f"""
用户需求：{user_query}
查询结果：
    """ # 存储查询的表格，及其描述
    tabel_count = 1
    imageSavePaths = [] # 保存分析图片的保存路径
    for query in results_json:
        sql = query['sql']
        if sql == "":
            continue
        desc = query['desc']
        print(f"查找数据：{desc} ;\nExecuting sql： {sql};")
        try:
            table = sqlExecuter.execute_query(sql)  # 打印查询结果
            imageSavePath = draw.executeAndDrawByQuery(sql,desc) #绘制图表

            imageSavePaths.append(f"![{desc.replace('查询','').replace('的结果','')}]({imageSavePath})")
            tabels += f"表: {desc} \n"
            tabels += table
            tabel_count += 1
        except Exception as e:
            print(f"执行SQL出现了错误，错误原因:{e}")
    return tabels,imageSavePaths

if __name__ == "__main__":
    # 示例用户查询
    user_query = "2022年9月至2023年3月的国内铁矿石供应总量数据，以了解国内铁矿石供给情况中的矿山产能利用率"
    tabels,imageSavePaths = askDataAgent(user_query)
    print(tabels)
    for imageSavePath in imageSavePaths:
        print(imageSavePath)




