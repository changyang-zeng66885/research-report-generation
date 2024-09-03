from openai import OpenAI
import Config.config as config
import dataAgent.dataAgent as dataAgent

def generateReportText(reportTitle,yearMon,timeRange,topic,direction,DataFromDataAgent,EventsFromPreviousReports,refText = ""):
    '''
    根据指令写研报的片段
    Args:
        reportTitle: 研报的标题，如 202x年t月月报:供给分析:铁矿石
        yearMon: 研报时间，如 202x年t月
        timeRange: 研报的时间范围 如 "过去一年中","近三个月以来"
        topic:该片段的的主题，如："国内铁矿石供给情况:国产铁矿石原矿产量",
        direction: 写作该研报的指令 如： "简要说明分析的时间范围。例如：自xxxx年yy月以来/近三个月以来",
        DataFromDataAgent: 由DataAgent提供的数据
        EventsFromPreviousReports: 由研报Agent提供的既往重点信息
        refText: 参考文本，一般是之前写的研报

    Returns:
        生成的研报片段

    '''

    prompt = f"""
    假设您是一名证券公司，铁矿石组的研究员。您所在的团队需要整理一份《{reportTitle}》的研报，您负责撰写的部分为: {direction}，时间范围是：{yearMon}，{timeRange}
    假设您的团队为您 提供了如下参考信息
    1. 参考数据
       { DataFromDataAgent }
    2. 过去一段时间的重点事件与时间点
       { EventsFromPreviousReports }
    3. 您的同事之前写的【参考文字】（如果该部分为空，您可以忽略这一部分）
        {refText}
    您现在需要根据已知的信息,撰写一段 { topic } 的研报片段。请注意：您只需要做:{direction}。
    
    具体要求有:
    + 字数在200-500字之间
    + 只写 {direction} 这一部分的研报片段，不要写其他任何不相关的内容。
    + 请您必须完全基于上述提供的【1. 参考数据】和【2. 过去一段时间的重点事件与时间点】撰写，不得自行生成数据，也不得引用上面未提及的重点事件与时间点。
    + 请你**只返回**生成的研报片段，不要返回除了研报片段以外的任何文字（包括任何说明性文字、问候语等）。
    + 不要出现 例如 ”您的同事之前写的【参考文字】“之类的文字，您只需要给出分析观点即可。
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

def generateTrendReview(reportTitle,yearMon):
    '''
    生成走势回顾
    Args:
        reportTitle: 要生成的研报标题，如 202x年t月月报:供给分析:铁矿石
        yearMon: 研报日期 如 202x年t月
    Returns:
        生成的完整的走势回顾
    '''

    fullTrendReviewText = "" # 完整的走势回顾文字

    topics=[
        "国际铁矿石供给情况:铁矿砂及精粉进口量、到港量变化(可以分主流矿和非主流矿)"
        "国际铁矿石供给情况:近3年内，四大矿山(巴西的淡水河谷、澳大利亚的力拓、必和必拓和福蒂斯丘)年度年产量变动情况",
        "国内铁矿石供给情况:国产铁矿石原矿产量",
        "国内铁矿石供给情况:矿山产能利用率"
    ] # 研报片段的分析主题
    directions=[
        "说明该时间范围中，1. 指标总体趋势概况 2. 分析指标在数值上的变化情况。必须涵盖：具体数值，同比上升/下降x万吨、同比上升/下降y%",
        "根据 您的同事之前写的【参考文字】 的内容， 分析上述指标变化可能的原因（政策、市场等因素）",
        "根据 您的同事之前写的【参考文字】 的内容，合理预测后续的指标变化，并为投资者提供建议"
    ] # 以什么角度分析该主题
    # timeRanges = ["过去一年", "近三个月"]
    timeRanges = ["过去三个月"]
    print(f"开始生成研报.. 标题: {reportTitle},时间范围:{yearMon}")
    for topic in topics:
        print(f"正在生成主题: {topic} ...")
        fullTrendReviewText += f"\n {topic} \n"
        refText = "" # 参考文本
        for direction in directions:
            print(f"正在分析:{direction} ...")
            for timeRange in timeRanges:
                print(f"正在分析时间范围为 {timeRange} 的情况....")
                fullTrendReviewText += timeRange+","
                data_query = f" 主题为:{topic}; 时间范围：{yearMon}以来，{timeRange}的数据; 查询的数据将用于:{direction}"
                DataFromDataAgent = dataAgent.askDataAgent(data_query)
                event_query = f" 主题为:{topic};时间范围为： {yearMon},{timeRange} 的 重要的事件节点数据"
                EventsFromPreviousReports = dataAgent.askDataAgent(event_query)
                text = generateReportText(reportTitle,yearMon,timeRange,topic,direction,DataFromDataAgent,EventsFromPreviousReports,refText)
                fullTrendReviewText+= text
                refText += text
                fullTrendReviewText += " \n"
                print("*"*20+"【研报正文】"+"*"*20)
                print(f"{text}")
                print("*" * 45)


    return fullTrendReviewText

if __name__ == "__main__":
    reportTitle = '2022年9月月报:供给分析:铁矿石'
    yearMon = "2022年9月"
    fullTrendReviewText = generateTrendReview(reportTitle, yearMon)
    print("*"*50)
    print(f"完整的研报：{reportTitle}")




    print(fullTrendReviewText)






