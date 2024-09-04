import DataAnalyzeAgent
import dataAgent.dataAgent as dataAgent

def generateTrendReview(reportTitle,yearMon):
    '''
    生成走势回顾
    Args:
        reportTitle: 要生成的研报标题，如 202x年t月月报:供给分析:铁矿石
        yearMon: 研报日期 如 202x年t月
    Returns:
        生成的完整的走势回顾
    '''

    print(f"开始生成研报.. 标题: {reportTitle},时间范围:{yearMon}")

    fullTrendReviewText = f"# {reportTitle}" # 完整的走势回顾文字

    topics=[
        "走势回顾情况：普氏62%指数价格，日照港Pb粉等现货价格，合约价格、DCE01、DCE05、DCE07变化",
        "国际铁矿石供给情况:铁矿砂及精粉进口量、到港量变化(可以分主流矿和非主流矿)",
        "国际铁矿石供给情况:四大矿山(巴西的淡水河谷、澳大利亚的力拓、必和必拓和福蒂斯丘)年度年产量变动情况",
        "国内铁矿石供给情况:国产铁矿石原矿产量",
        "国内铁矿石供给情况:矿山产能利用率"
    ] # 研报片段的分析主题


    for topic in topics:
        print(f"正在生成主题: {topic} ...")

        data_query = f" 主题为:{topic}；时间范围：{yearMon}以来，往前推3-6个月左右的的相关数据"
        dataFromDataAgent,imageSavePaths = dataAgent.askDataAgent(data_query)
        events_query = f" 主题为:{topic}；时间范围为：{yearMon},往前推3=6个月左右,发生的重要的事件数据"
        eventsFromPreviousReports = dataAgent.askDataAgent(events_query)

        # 分析指标走势数据
        dataAnalyzeText = DataAnalyzeAgent.dataAnalyzeAgent(reportTitle,yearMon,topic,dataFromDataAgent,eventsFromPreviousReports)

        # 分析指标走势发生变化的原因
        dataChangeReasonText = DataAnalyzeAgent.analyzeAgent(reportTitle,yearMon,topic,dataAnalyzeText,dataFromDataAgent,eventsFromPreviousReports)

        # 生成总结文字与小标题
        sultitle, abstract = DataAnalyzeAgent.summaryAgent(reportTitle,yearMon,topic,dataAnalyzeText+"\n"+dataChangeReasonText,dataFromDataAgent,eventsFromPreviousReports)

        text = f"""
## **{sultitle}**
自{yearMon}以来，{abstract} 指标走势方面，{dataAnalyzeText} {dataChangeReasonText}
        """

        for imageSavePath in imageSavePaths:
            text+= imageSavePath+"\n"


        fullTrendReviewText+= text
        print("*"*20+"【研报正文】"+"*"*20)
        print(f"{text}")
        print("*" * 45)


    return fullTrendReviewText

if __name__ == "__main__":
    # 2022年9月、11月、12月；2023年3月、5月、6月、8月、9月

    # yearMonList = ["2022年9月","2022年12月","2023年5月","2023年6月","2023年8月","2023年9月"]
    yearMonList = ["2023年3月"]
    for yearMon in yearMonList:
        reportTitle = f'{yearMon}月报：走势回顾与供给分析：铁矿石'
        fullTrendReviewText = generateTrendReview(reportTitle, yearMon)
        print("*"*50)
        print(f"完整的研报：{reportTitle}")
        print(fullTrendReviewText)
        with open(f'reportResult/{reportTitle}.md', 'w',encoding='utf-8') as file:
            file.write(fullTrendReviewText)



