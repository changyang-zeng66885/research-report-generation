import sqlite3
import matplotlib.pyplot as plt
import Config.config as config
import pandas as pd

# 设置支持中文的字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号


def executeAndDrawByQuery(sql_query, desc):

    if sql_query.count("Public_oponion") or sql_query.count("Events"):
        print("Events 和 Public_oponion 不支持画图！")
        return ""
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

    # 绘制折线图
    desc = desc.replace("查询","").replace("的结果","")
    output_image_path = config.saveReportDir+"/assets/" + desc + ".png"
    plot_data(column_names, rows, output_image_path,title=desc)

    return "assets/"+desc+".png" # 这个返回的是markdown文件的相对地址（config.saveReportDir）


def plot_data(column_names, rows, output_image_path, title=""):
    # 转换数据为 DataFrame
    df = pd.DataFrame(rows, columns=column_names)

    # 自动识别日期/时间列
    date_col = pd.to_datetime(df[column_names[0]], errors='coerce')
    df[column_names[0]] = date_col

    # 选择日期列作为 x 轴，其他列作为 y 轴
    x = df[column_names[0]]
    y_data = df[column_names[1:]]

    # 增加图形宽度
    plt.figure(figsize=(12, 6))

    for col in y_data.columns:
        plt.plot(x, y_data[col], label=col)

    plt.xlabel(column_names[0])
    plt.ylabel("Values")
    plt.title(title)
    plt.legend()
    plt.grid()

    # 设置 x 轴标签纵向排列
    plt.xticks(rotation=45, fontsize=10)

    # # 省略部分日期，只显示每个月的1日
    # plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # plt.gca().xaxis.set_major_formatter(
    #     plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%Y-%m-%d') if pd.to_datetime(x).day == 1 else ''))

    # 自动调整 x 轴标签以防重叠
    plt.tight_layout()

    # 保存图像
    plt.savefig(output_image_path)
    plt.close()

# 使用示例
if __name__ == "__main__":
    sql_query = "SELECT YearMon, Yield FROM IronOre_supply_domestic WHERE YearMon BETWEEN '2022-09' AND '2023-03' ORDER BY YearMon;"
    desc = "demo-IronOre_supply_domestic"
    executeAndDrawByQuery(sql_query, desc)