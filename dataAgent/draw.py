import sqlite3
import matplotlib.pyplot as plt

# 设置支持中文的字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号


def executeAndDrawByQuery(sql_query, desc):

    if sql_query.count("Public_oponion") or sql_query.count("Events"):
        print("Events 和 Public_oponion 不支持画图！")
        return ""
    conn = sqlite3.connect('D:/24大语言模型工程师实训营/dataAgent/ironDB.db')
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
    output_image_path = "../ReportGenerateAgent/reportResult/assets/"+desc+".png"
    plot_data(column_names, rows, output_image_path,title=desc)

    return "/assets/"+desc+".png" # 这个返回的是markdown文件的相对地址

def plot_data(column_names, rows, output_image_path,title=""):
    # 假设第一列是 x 轴，剩余列是 y 轴
    x = [row[0] for row in rows]
    y_data = [list(row[1:]) for row in rows]

    # 增加图形宽度
    plt.figure(figsize=(12, 6))

    for i in range(len(column_names) - 1):
        plt.plot(x, [row[i] for row in y_data], label=column_names[i + 1])

    plt.xlabel(column_names[0])
    plt.ylabel("Values")
    plt.title(title)
    plt.legend()
    plt.grid()

    # 设置 x 轴标签纵向排列
    plt.xticks(rotation=45, fontsize=10)

    # 自动调整 x 轴标签以防重叠
    plt.tight_layout()


    # 保存图像
    plt.savefig(output_image_path)
    plt.close()

# 使用示例
if __name__ == "__main__":
    sql_query = "SELECT Shipment_Volume_Date AS date, Global_Shipment_Volume AS global_shipment, Aus_Bra_Shipment_Volume AS aus_brazil_shipment, Non_Mainstream_Shipment_Volume AS non_mainstream_shipment FROM IronOre_supply WHERE Shipment_Volume_Date BETWEEN '2021-09-01' AND '2022-09-30';"
    desc = "查询2021年9月至2022年9月期间,国际铁矿石供给情况，包括全球发货量、澳洲和巴西发货量以及非主流矿发货量的结果"
    executeAndDrawByQuery(sql_query, desc)