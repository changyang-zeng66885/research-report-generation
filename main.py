import  ReportGenerateAgent.reportAgentNew as reportAgent
import Config.config as config


if __name__ == "__main__":

    # 在这里设置需要生成研报的日期
    yearMonList = ["2022年9月","2022年11月","2022年12月","2023年5月","2023年6月","2023年8月","2023年9月"]
    for yearMon in yearMonList:
        reportTitle = f'{yearMon}月报：走势回顾与供给分析：铁矿石'
        fullTrendReviewText = reportAgent.generateTrendReview(reportTitle, yearMon)
        print("*"*50)
        print(f"完整的研报：{reportTitle}")
        print(fullTrendReviewText)
        with open(f'{config.saveReportDir}/{reportTitle}.md', 'w',encoding='utf-8') as file:
            file.write(fullTrendReviewText)
