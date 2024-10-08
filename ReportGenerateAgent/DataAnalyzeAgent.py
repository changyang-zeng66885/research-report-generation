import json

from openai import OpenAI
import Config.config as config


def dataAnalyzeAgent(reportTitle,yearMon,topic,DataFromDataAgent,EventsFromPreviousReports):
    '''
    分析数据的Agent
    Args:
        reportTitle: 研报标题
        yearMon: 研报分析时间 格式为 YYYYMM
        topic: 分析的主题

    Returns:
        分析结果
    '''
    prompt = f"""
        假设您是一名证券公司，铁矿石组的研究员。您所在的团队需要整理一份《{reportTitle}》的研报，分析的时间范围是：{yearMon}
        您的工作是：根据已提供的信息,对 {topic} 的对指标的变化进行分析。
        
        假设您的团队为您 提供了如下参考信息：
        -------------------------------参考数据-------------------------------
        1. 主要指标变化
           {DataFromDataAgent}
        2. 过去一段时间的重点事件与时间点
           {EventsFromPreviousReports}
        -------------------------------------------------------------------
           
        具体要求有:
        + 字数在150-250字之间
        + 只分析指标变化，不要写其他任何不相关的内容。
        + 必须完全基于上述提供的【参考数据】撰写，不得自行生成数据，也不得引用上面未提及的重点事件与时间点。
        + 不要预测未来的走势
        + 请你**只返回**生成的研报片段，不要返回除了研报片段以外的任何文字（包括任何说明性文字、问候语等），也不要输出"指标分析："之类的文本。
        + 输出结果不要换行
        
        参考示例文本：
        参考示例1：近期铁矿石期货价格过快过高上涨，且价格波动严重背离供需基本面，多次出现异动引发监管部门高度关注，连铁期货价格自2021年11月下旬最低点512.0元/吨上涨至最高点849.5元/吨，涨幅高达65.91%，其中2022年1月单月最高涨幅更是达到21.91%；普氏62%指数自低点87.20美金/吨上涨至最高点153.75美金/吨，涨幅76.32%。2月份期现均出现大幅下挫，连铁主力2205合约最低点655.0元/吨，最大跌幅22.90%，普氏62%指数最低下跌至130.65美金/吨，跌幅15.02%。
        参考示例2：根据国家统计局数据显示，2022年一季度粗钢产量为24338万吨，同比下降10.50%，同比下降量为2855万吨，一季度生铁产量为20090.5万吨，同比下降11.0%，同比下降量为2483.10万吨，日均铁水量223.2万吨，同期钢联口径铁水产量215万吨/日
        参考示例3：四季度主流矿山发运预增，叠加海外经济衰退需求减弱，非主流发运保持弱势，国产受矿难、季节性等因素影响，根据海关总署数据显示，1-8月进口数量为72336.09万吨，同比-3.01%（-2283.1万吨），澳巴进口数量同比增加2.33%（1431.1万吨），非澳巴进口量同比-26.57%（-3714.2万吨）。
        参考示例4： 前三季度，澳洲矿山发运完成进度均相对较好，巴西淡水河谷发运相对落后，截止9月25日，四大矿山发运共计7.94亿吨，同比下降0.73%， 其中淡水河谷完成度为70.07%，澳洲三大矿山完成度接近75%
        
        """

    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0,
        stream=False
    )


    dataAnalyzeText = response.choices[0].message.content

    return dataAnalyzeText

def analyzeAgent(reportTitle,yearMon,topic,refText,DataFromDataAgent,EventsFromPreviousReports):
    prompt = f"""
            假设您是一名证券公司，铁矿石组的研究员。您所在的团队需要整理一份《{reportTitle}》的研报；分析的主题是：{topic}
            您的工作是：根据已提供的信息,分析指标变化所产生的原因（政策、市场等），并推测后续指标的变化。
            分析的时间范围是从开始{yearMon}，往前分析1个月至半年的走势情况。

            假设您的团队为您提供了如下参考信息：
            -------------------------------参考数据-------------------------------
            1. 主要指标变化
               {DataFromDataAgent}
            2. 过去一段时间的重点事件与时间点
               {EventsFromPreviousReports}
            3. {topic}的指标分析文字
               {refText}
            -------------------------------------------------------------------
            
            具体要求有:
            + 字数在150-250字之间
            + 只分析分析制定的内容，不要写其他任何不相关的内容。
            + 必须完全基于上述提供的【参考数据】撰写，不得自行生成数据，也不得引用上面未提及的重点事件与时间点。
            + 请你**只返回**生成的研报片段，不要返回除了研报片段以外的任何文字（包括任何说明性文字、问候语等），也不要输出"指标变化原因推测：", "指标变化预测：" 之类的文本。
            + 输出结果不要换行
            
            指标变化原因推测示例：
            参考示例1：1月份受海外需求复苏以及货币宽松影响铁矿石价格出现非理性上涨，2月份交易远期供需趋紧预期盘面价格大幅走高，3月份受两会期间环保限产以及唐山地区限产减排政策超预期，需求端受政策影响严重下滑，加剧供需关系阶段性宽松格局，价格一度大幅走弱，但3月份原材料焦炭价格大幅下跌叠加需求端逐步恢复使得成材端利润快速扩大，成材高利润和铁矿石货权集中背景下铁矿石现货价格仍保持强势，3月份下旬基差回归逻辑主导盘面，盘面大幅回升修复贴水，一季度期价整体高位宽幅震荡且小幅微跌。
            参考示例2: 2021年上半年，铁矿石价格变动重要时间节点分别在春节前后、3月份中下旬的两会期间津京冀地区环保限产和3月19开始的唐山地区独立环保限产以及"五一假期"后国常会对大宗商品价格上涨的点名。春节前由于市场对成材高价格接受程度较低以及对后市预期悲观，较低的冬储水平抑制了钢厂补库强度，铁矿石盘面表现弱势，春节期间疫情导致工地工人就地过年较多，加快了节后复产节奏，钢厂集中补库带动价格走高持续至两会前夕；3月份上旬两会限产预期和津京冀地区实际限产抑制了价格上行高度，下旬的唐山地区超预期环保限产强烈打压了铁矿石价格，但成材在供需错配情况下利润暴涨刺激了非限产区域钢企的生产积极性，叠加市场现货投机氛围浓厚，现货进口利润一度从倒挂上涨至100元/吨以上，铁矿石期现价格同步出现暴涨至"五一"假期之后；5月12号，国常会再度点名大宗商品价格上涨过快并且约谈部分机构和贸易商，会议要求原材料市场囤积居奇、哄抬价格等非合理市场行为，市场投机情绪快速降温，是铁矿石期货价格大幅下跌的开端。5月份，铁矿石整体供需两旺，但供给端增量小于需求端增量，供需平衡偏紧，环保限产范围尚未进一步扩大且非限产地区高炉高开工使得近月需求持续回升，需求端持续走强是五一假期后的大幅上涨主要基本面驱动之一，再者成材高利润和铁矿石货权集中背景下铁矿石现货价格保持强势，然而，市场过热的投机氛围以及宽松的货币环境是推升行情大幅上涨的主要原因，随着李克强总理对大宗商品价格非理性上涨的定性，铁矿石期现价格向理性回归。
            
            指标变化预测示例：
            示例1：展望5月份，由于当前终端需求偏弱，钢厂利润薄弱，钢厂复产动力略有不足，但5月份全国疫情有望得到有效遏制，叠加经济刺激预期较强、终端需求也处于传统旺季阶段，综合看，5月份铁矿石有望保持稳中有增态势。
            示例2：我们预计2022年上半年粗钢产量存在环比增量空间，对应铁水产量存在较大环比增量预期。但当前钢厂补库进入尾声，叠加冬奥会限产预期，钢厂进一步复产以及补库需求均受到抑制，短期铁矿石需求面临阶段性压力；矿价继续走强驱动略有不足，然而中期市场整体预期铁水仍将有较大增加空间。
            
            """

    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.2,
        stream=False
    )

    dataAnalyzeText = response.choices[0].message.content

    return dataAnalyzeText

def summaryAgent(reportTitle,yearMon,topic,refText,DataFromDataAgent,EventsFromPreviousReports):
    prompt = f"""
                假设您是一名证券公司，铁矿石组的研究员。您所在的团队需要整理一份《{reportTitle}》的研报；分析的主题是：{topic}，分析的时间范围是{yearMon}.
                您的工作是：总结已有的分析，写一段摘要"abstract" （60字以内），并为该段文字你一个小标题"subtitle"（30字以内）。

                假设您的团队为您提供了如下参考信息：
                -------------------------------参考数据-------------------------------
                1. 主要指标变化
                   {DataFromDataAgent}
                2. 过去一段时间的重点事件与时间点
                   {EventsFromPreviousReports}
                3. {topic}的指标分析文字
                    {refText}
                -------------------------------------------------------------------

                具体要求有:
                + 字数限制：总结性的文字不超过60字；小标题不超过30字.
                + 不要写其他任何不相关的内容。
                + 必须完全基于上述提供的【参考数据】撰写，不得自行生成数据，也不得引用上面未提及的重点事件与时间点。
                + 不要返回除了研报片段以外的任何文字（包括任何说明性文字、问候语等）。
                + 小标题subtitle 必须具有概括性。要让读者一看小标题，就能了解文本大致的内容。
                
                返回格式示例：
                {{
                    "subtitle":"价格严重偏离基本面 监管强压下回归理性", 
                    "abstract": "近期铁矿石期货价格过快过高上涨，且价格波动严重背离供需基本面，多次出现异动引发监管部门高度关注。"
                }}
                
                标题示例：
                示例1：价格严重偏离基本面 监管强压下回归理性
                示例2：行情展望：需求端稳中有增 供应端开始回升
                示例3：需求端：粗钢压减抑制需求 边际增加空间受限
                示例4：走势回顾：价格严重偏离基本面 监管强压下回归理性
                
                """

    client = OpenAI(api_key=config.deepseek_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0,
        stream=False
    )

    summaryText = response.choices[0].message.content
    summaryText = summaryText.replace("```", "").replace("json", "")
    summaryJSON = json.loads(summaryText)

    try:
        sultitle,abstract = summaryJSON['subtitle'],summaryJSON['abstract']
    except Exception as e:
        print(f"解析 subtitle 或者 abstract 时出现了错误：{e}")
        sultitle, abstract = "",""

    return sultitle, abstract











