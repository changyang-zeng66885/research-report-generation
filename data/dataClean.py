import pandas as pd
import sqlite3
from datetime import datetime

# 创建 SQLite 数据库连接
conn = sqlite3.connect('data/ironDB.db')

# 读取 Excel 文件
excel_file = 'data/alldata/IRON_DATA.xlsx'
xls = pd.ExcelFile(excel_file)

# 遍历所有 Sheet
for sheet_name in xls.sheet_names:
    # 读取当前 Sheet
    print(f"Processing sheet: `{sheet_name}`")
    df = pd.read_excel(xls, sheet_name=sheet_name)


    df.insert(0, 'id', range(1, len(df) + 1))

    # 将数据写入 SQLite 数据库
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)

# 关闭数据库连接
conn.close()