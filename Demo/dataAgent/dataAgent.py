from openai import OpenAI
import Config.config as config

def load_database_description(file_path):
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

    """

    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.1,
        stream=False
    )
    
    return response.choices[0].message.content

# 读取数据库描述文件


# 示例用户查询
# user_query = "2022年1月-3月，日照港铁矿石价格的变化情况"
# user_query = "2022年1月-6月，铁矿石价格的变化，数据尽量涵盖多的方面。"
user_query = """
查询需求: 2021年1月-3月 宏观经济与政策环境相关的观点数据。如果有的话，可以提供 【标题】、【主要内容】 【事件类别】等属性
"""

# 生成 SQL 查询
sql_query = generate_sql_query(user_query)
print(f"Data Agent 的查询建议：{sql_query}")