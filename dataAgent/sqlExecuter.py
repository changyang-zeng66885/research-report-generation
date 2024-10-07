import sqlite3
import matplotlib.pyplot as plt
import Config.config as config

def execute_query(sql_query):
    conn = sqlite3.connect(config.databaseDir)
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # 获取列名
    column_names = [description[0] for description in cursor.description]

    # 关闭连接
    cursor.close()
    conn.close()

    # 格式化输出结果
    result = format_output(column_names, rows)

    # 绘制折线图
    return result




def format_output(column_names, rows):
    # 创建表头
    header = "  " + "   ".join(column_names) + "\n"
    separator = "-" * (len(header) - 1) + "\n"

    # 创建内容
    body = ""
    for row in rows:
        body += "  ".join(f"{str(item):<15}" for item in row) + "\n"

    return f"{separator}{header}{separator}{body}{separator}"




# # 示例使用
# sql = """
# SELECT YearMon, Yield FROM IronOre_supply_domestic WHERE YearMon BETWEEN '2021-01' AND '2022-03';
# --查询2022年1月至3月国内铁矿石产量的变化情况。
# """
# result = execute_query(sql)
# print(result)