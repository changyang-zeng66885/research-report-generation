# 研报生成系统架构设计
我正在设计一个研报生成的机器人，大致思路是：将相关的数据（例如价格走势）和往期参考研报存放在数据库中。当需要生成研报时，由Data Agent生成SQL 查询语句，将查询结果返回给Researcher Agent 撰写研报，最后由Editor Agent进行润色。

## 数据处理



在数据查询阶段，结构化的数据（如价格，供应量）等数据很容易存储在数据库中。难点是非结构化的数据（如研报文本）。在研报生成过程中，我需要通过研报收集：

某时间 重要的政策信息（例如涉及铁矿石行业的政策变动、环保政策、贸易政策等）
市场情绪数据：市场对大宗商品价格的预期、市场情绪波动等。
其他可以利用的数据，例如对以往走势的分析。虽然这部分的数据可以通过SQL查询，但是我还是希望能够利用到这些数据.

### 结构化数据
+ 总体设想：将数据整理并存储在Sqlite中。DataAgent通过写SQL查询所需的数据

#### 数据表一览

##### 走势回顾相关
+ PlattsIronOreIndex 普氏铁矿石价格指数（记录日期范围：2013.1.2-2023.11.14）
  + date	
  + yield
+ IronOrePrice_RizhaoPort 日照港铁矿石价格（记录日期范围：2020.1.2-2023.11.21）
  + date
  + price_aus_Jimblebar_61 日照港:澳大利亚:金布巴粉61% 车板价
  + price_aus_PB_61_5  日照港:澳大利亚:PB粉矿61.5% 车板价
+ DCE01,DCE05,DCE07 (三张表)大连期货交易所铁矿石期货合约价格(记录日期范围：2013年-2023.09.24) 
  + MarketDate	
  + ClosingPrice	
  + SettlementPrice
  
+ IronOre_comprehensive 铁矿石综合（记录日期范围：2022.03.24-2023.11.14）
  > 数据说明：包括铁矿石粉末价格现货市场价格/基准价格/期货合约价格/进口铁矿石利润情况/钢筋与铁矿石的比例等数据
  + QUOTEDATE：报价日期
  + SpotDZYangDiPowder 现货市场上杨迪矿石粉（产于澳大利亚，必和必拓公司经营）价格。
  + SpotDZPB_Powder 现货市场PB铁矿石粉末价格。
  + SpotDZJinBubaPowder 现货市场上金布巴（Jin Buba）铁矿石粉末的价格。
  + SpotDZKaraLaraFinePowder 现货市场上卡拉拉（Kara Lara）优质铁矿石粉末的价格。
  + SpotDZKaraJagasPowder 现货市场上卡拉贾斯（Kara Jagas）铁矿石粉末的价格。
  + SpotDZBaMixBRBF 现货市场巴西淡水河谷混矿价格
  + SpotDZUltraSpecialPowder 现货市场上超特殊类型的铁矿石粉末价格。
  
  + PusiIndex62USD 62%铁矿石的普氏指数，以美元计价，反映国际市场的价格水平。
  + BaseDZYangDiPowder 基准的杨迪铁矿石粉末价格。
  + BaseDZUltraSpecialPowder 基准的超特殊类型铁矿石粉末价格。
  + BaseDZPB_Powder     基准的PB铁矿石粉末价格。
  + BaseDZJinBubaPowder 基准的金布巴铁矿石粉末价格。
  
  + SwapJan             1月期货合约的价格
  + SwapMay             5月期货合约的价格或数据。
  + SwapSep             9月期货合约的价格或数据。
  + ImportProfitJan     1月铁矿石的利润情况。
  + ImportProfitMay     5月铁矿石的利润情况。
  + ImportProfitSep     9月铁矿石的利润情况。
  + RebarMineRatioSpot  现货市场上钢筋与铁矿石的比例。
  + RebarMineRatioJan   1月的钢筋与铁矿石的比例。
  + RebarMineRatioMay   5月的钢筋与铁矿石的比例。
  + RebarMineRatioOct   10月的钢筋与铁矿石的比例。

##### 供给分析相关
+ RawOreYield 原矿产量(万吨)(记录日期范围：2012.1-2023.10)
  + yearMon
  + yield
+ CrudeSteel_Production 中国粗钢产量（万吨）(记录日期范围：2021.01-2023.10)
  + YearMon 
  + Yield
+ PigIronProduction 生铁产量（万吨）（记录日期范围：2016.1-2023.10）
  + YearMon	
  + Yield
+ IronOre_supply 铁矿石供应量(记录日期范围：2020.10.16-2023.11.20)
  + Shipment_Volume_Date	
  + Global_Shipment_Volume	
  + Aus_Bra_Shipment_Volume	
  + Aus_Shipment_Volume	
  + FMG_Shipment_Volume	
  + BHP_Shipment_Volume	
  + Rio_Tinto_Shipment_Volume	
  + Vale_Shipment_Volume	
  + Bra_Shipment_Volume	
  + Aus_to_China_Shipment_Volume
  + FMG_to_China_Shipment_Volume
  + BHP_to_China_Shipment_Volume
  + Rio_Tinto_to_China_Shipment_Volume
  + Non_Mainstream_Shipment_Volume
+ IronOre_supply_domestic 国内铁矿石供应总量(记录范围：2012.1-2023.11)
  + YearMon	
  + Yield
+ IronOreInventory_AUS 铁矿石库存：澳大利亚(记录日期范围：2014.1.3-2023.12.12 每隔一周记录一次) 
  + Date	
  + Quantity
+ IronOreInventory_BRA 铁矿石库存：巴西(记录日期范围：2014.1.3-2023.12.7 每隔一周记录一次)
  + Date	
  + Quantity
+ IronOreInventory_Sprase_port (记录日期范围：2014.1.3-2023.12.13 每隔一周记录一次)
  + Date	
  + Quantity
+ IronOreInventory_Total 铁矿石库存：全球(记录日期范围：2014.1.3-2023.12.9 每隔一周记录一次)
  + Date	
  + Quantity
+ Sypply_IronOre 铁矿石供给发运量(单位：万吨)（记录日期范围：2020.10.16-2023.11.20）
  + date 日期
  + global_shipments_week: 全球发货量
  + australia_brazil_shipments_week: 澳洲和巴西铁矿石发货量
  + australia_production_shipments_week: 澳大利亚铁矿石产量
  + fmg_shipments_week: FMG发货量
  + bhp_shipments_week: 必和必拓发货量
  + rio_tinto_shipments_week: 力拓发货量
  + vale_shipments_week: 淡水河谷发货量
  + brazil_production_shipments_week: 巴西铁矿石产量
  + australia_to_china_total_shipments_week: 澳大利亚发货量合计到中国
  + fmg_to_china_shipments_week: FMG发货到中国
  + bhp_to_china_shipments_week: 必和必拓发货到中国
  + rio_tinto_to_china_shipments_week: 力拓发货到中国
  + non_mainstream_shipments_week: 非主流发货量
  + fmg_to_china_ratio: FMG发货到中国比例
  + bhp_to_china_ratio: 必和必拓发货到中国比例
  + rio_tinto_to_china_ratio: 力拓发货到中国比例
  + total_shipments_week: 合计发货量

+ Visual_requirements_for_rebar 螺纹钢表观需求(记录日期范围：2021.1.8-2023.11.18)
  + date
  + yield
+ Visual_requirements_for_HotStell 热卷表观需求(记录日期范围：2021.1.8-2023.11.18)
  + date
  + yield

##### 其他数据

+ Public_oponion 公众看法（记录日期范围：2023.1.1-2024.1.5）
  + sentiment_id	新闻编号
  + title	新闻名称
  + publication_time	发布事件
  + topic_tags	话题标签，由于此属性空值较多，可以忽略
  + event_tags	事件标签，
  >**event_tags	事件标签,包括**: 经营展望	机构解读	其它新闻	人事动态	土地出让	投资合作	财报业绩	股价上涨	人事风险	股价下跌	债券发行	商票逾期	常规兑付	企业拿地	地方化债政策	地方投融资政策	审批进程	公积金贷款	其它变更	增持减持	澄清辟谣	区域动态	其它招投标	监管处罚	收并购	银行授信	诉讼纠纷	上市退市	资产出售	地方国企改革	非标融资	境内债招投标	关联公司	监管问询关注	持有人会议	回售转售	经营负面	评级动态	股权变动	美元债动态	信披违规	购房补贴	资产划转	担保相关	债券条款变更	商票逾期澄清	境外债招投标	保障性住房	宏观经济	债券赎回	其它地方政策	债市速览	债价下跌	员工动态	破产重整/清算	各地保交楼方案	取消/推迟发行	首付比例	房贷利率调整	资产抵(质)押	财务异常	非标舆情	政府补贴	资产减值	纳入被执行人	中央政策	中标结果	债务重组	债券违约	债价上涨	停牌复牌	提前兑付	中债隐含评级	评级上调	其它债务违约	置换及展期	资产重组	限购	债券回购	资产冻结	评级下调	银行借款	实控人变动	限售	预售资金监管	资产处置	预售条件	价格跟踪	违约后续	市场解读	发行计划	行业动态	权益融资	产业政策	事件跟踪	一级发行	交易日报	城投专题	经济数据&政策	市场行情	新债跟踪	审批驳回	债券增发	回购及要约	发行人名称变更	中介机构变更	限贷	审批终止	回售到期分布
  + risk_tags	 风险标签，包括风险，正面，中性
  + importance_level	普通，重要
  + sentiment_source	新闻来源（网站名称）
  + website_link	新闻链接
  + news_data_source	新闻来源，但是不清楚标签值的含义
  + region_code	地区编号
  + region_name	地区名称
  + company_code	公司编号
  + company_name	公司名称
  + credit_code 公司信用代号

+ PusiIndex 普氏铁矿石62%指数（记录日期范围：2013.1.2-2023.11.14）
  + IndexDate	
  + PusiIndex62USD
+ Steel_Company_Profitability 钢铁企业盈利率_中国_周(记录日期范围：2019.1.4-2023.11.10)
  + IndexDate 
  + profitability_rate

#### 测试结果
DataAgent运行结果：
```python
user_query = "2022年1月-6月，铁矿石价格的变化，数据尽量涵盖多的方面。"
```

```json
[
  {
    "sql": "SELECT date, price_aus_Jimblebar_61, price_aus_PB_61_5 FROM IronOrePrice_RizhaoPort WHERE date BETWEEN '2022-01-01' AND '2022-06-30'",
    "desc": "查询2022年1月至6月日照港铁矿石价格，包括澳大利亚金布巴粉61%和PB粉矿61.5%的车板价。"
  },
  {
    "sql": "SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE01 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30' UNION ALL SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE05 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30' UNION ALL SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE07 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30'",
    "desc": "查询2022年1月至6月大连期货交易所铁矿石期货合约价格，包括DCE01、DCE05和DCE07合约的收盘价和结算价。"
  },
  {
    "sql": "SELECT QUOTEDATE, SpotDZYangDiPowder, SpotDZPB_Powder, SpotDZJinBubaPowder, SpotDZKaraLaraFinePowder, SpotDZKaraJagasPowder, SpotDZBaMixBRBF, SpotDZUltraSpecialPowder, PusiIndex62USD, BaseDZYangDiPowder, BaseDZUltraSpecialPowder, BaseDZPB_Powder, BaseDZJinBubaPowder, SwapJan, SwapMay, SwapSep, ImportProfitJan, ImportProfitMay, ImportProfitSep, RebarMineRatioSpot, RebarMineRatioJan, RebarMineRatioMay, RebarMineRatioOct FROM IronOre_comprehensive WHERE QUOTEDATE BETWEEN '2022-01-01' AND '2022-06-30'",
    "desc": "查询2022年1月至6月铁矿石综合数据，包括现货市场价格、基准价格、期货合约价格、进口铁矿石利润情况、钢筋与铁矿石的比例等。"
  },
  {
    "sql": "SELECT date, yield FROM PlattsIronOreIndex WHERE date BETWEEN '2022-01-01' AND '2022-06-30'",
    "desc": "查询2022年1月至6月普氏铁矿石价格指数。"
  }
]
```

供需分析数据：
```sql
--Prompt：2022年1月-6月，铁矿石价格的变化，数据尽量涵盖多的方面。

SELECT date, price_aus_Jimblebar_61, price_aus_PB_61_5 FROM IronOrePrice_RizhaoPort WHERE date BETWEEN '2022-01-01' AND '2022-06-30';
--查询2022年1月至6月日照港铁矿石价格，包括澳大利亚金布巴粉61%和PB粉矿61.5%的车板价。


SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE01 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30' UNION ALL SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE05 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30' UNION ALL SELECT MarketDate, ClosingPrice, SettlementPrice FROM DCE07 WHERE MarketDate BETWEEN '2022-01-01' AND '2022-06-30';
--查询2022年1月至6月大连期货交易所铁矿石期货合约价格，包括DCE01、DCE05和DCE07合约的收盘价和结算价。


SELECT QUOTEDATE, SpotDZYangDiPowder, SpotDZPB_Powder, SpotDZJinBubaPowder, SpotDZKaraLaraFinePowder, SpotDZKaraJagasPowder, SpotDZBaMixBRBF, SpotDZUltraSpecialPowder, PusiIndex62USD, BaseDZYangDiPowder, BaseDZUltraSpecialPowder, BaseDZPB_Powder, BaseDZJinBubaPowder, SwapJan, SwapMay, SwapSep, ImportProfitJan, ImportProfitMay, ImportProfitSep, RebarMineRatioSpot, RebarMineRatioJan, RebarMineRatioMay, RebarMineRatioOct FROM IronOre_comprehensive WHERE QUOTEDATE BETWEEN '2022-01-01' AND '2022-06-30';
--查询2022年1月至6月铁矿石综合数据，包括现货市场价格、基准价格、期货合约价格、进口铁矿石利润情况、钢筋与铁矿石的比例等。


SELECT date, yield FROM PlattsIronOreIndex WHERE date BETWEEN '2022-01-01' AND '2022-06-30';
--查询2022年1月至6月普氏铁矿石价格指数。
```

以上SQL均能正常执行

### 非结构化数据
#### 总体设想

Prompt：
你是一台从提供的研报文本中提取信息的AI系统。你的任务是整理研报中重要的事件+时间节点，并将信息转化成树状JSON列表，其中包含完整且未经修改的信息块。以下是详细要求和示例:
1. **完整切片**，一字不漏。
2. **不需要解释或任何多余的输出**。
3. 输出尽可能完整，要求如下:
(1)**标准JSON**:输出的格式必须是标准的JSON，不需要包含任何解释性或额外的文本。结构化:构建树状JSON结构，叶节点为“内容”
(2)如果文本中含有明显的结构标志(如标题、子标题)，利用这些标志帮助结构化JSON输出。确保每个“内容”字段内的文本是自包含的，能够独立传达完整的信息。提高准确性和避免遗漏，确保每个知识片段都被正确分类和标记。格式参考:

```json
{
  "report_title":"",//研报名称，例如：2022年2月报-铁矿石
  "events": // 研报中重要的事件+时间节点
  [
    {
      "event_date": "xxxx年xx月xx日", // 事件或信息的时间节点，例如：2021年，2021年4月 2021年4月13日
      "topic":"",// 该事件的内容概括（即content属性的内容概要，要求不多于50字）
      "content": "", // 该事件的内容
      "type": "",// 该事件的类型，例如：价格走势、政策信息、供给端动态、需求端动态、供需关系
      "type_region":""// 该事件的范围：例如:国内信息，国外信息
    }
  ]
}
```

输出结果示例：
```json
{
  "report_title": "2022年2月报-铁矿石",
  "events": [
    {
      "event_date": "2022年1月1日",
      "topic": "铁矿石价格走势回顾",
      "content": "2022年1月份铁矿石延续2021年11月中旬以来的反弹走势，钢厂复产从预期逐步走向现实，一方面粗钢压减政策进入空窗期，2021年全年粗钢控制政策完成度较高，且2021下半年粗钢环比减量过于显著导致2022年上半年存在较大环比增量空间，另一方面是长流程钢厂利润保持相对合理空间，钢厂增产原动力较强，叠加宏观政策表现积极提振商品估值水平，其中逆周期、跨周期经济调节力度加强，且货币政策释放宽松信号。",
      "type": "价格走势",
      "type_region": "国内信息"
    },
    {
      "event_date": "2022年1月1日",
      "topic": "铁矿石供需关系变化",
      "content": "短期随着铁矿石需求边际回升以及供应端边际走弱，铁矿石供需关系由宽松走向平衡偏紧，支撑铁矿石价格走强，但当前钢厂补库进入尾声，叠加冬奥会限产预期，钢厂进一步复产以及补库需求均受到抑制，短期铁矿石需求面临阶段性压力；供应方面巴西降水影响减弱后澳巴发运有所回升，到港量短期相对坚挺但由于前期发运减少导致将出现一定回落。",
      "type": "供需关系",
      "type_region": "国内信息"
    },
    {
      "event_date": "2021年1月1日",
      "topic": "国内铁矿石供应情况",
      "content": "2021年，国内供应整体走低，其中主流矿山、非主流矿山均出现一定程度下降，其中非主流矿山下降更为显著，国内矿供应前高后低但整体大幅增加，一是海外疫情失控情况下欧洲、印度、日韩等国需求增加，铁矿石向国外分流，二是粗钢压减政策下国内铁矿石需求迅速衰减，铁矿石阶段性显著过剩，进口需求大幅减弱，三是非主流矿、国产矿等高价资源在矿价迅速下降过程中供应也跟随下滑。海关总署数据显示，我国2021年1～12月我国累计进口铁矿砂及其精矿112562.5万吨，同比下降4630.2万吨，同比降幅3.95%。",
      "type": "供给端动态",
      "type_region": "国内信息"
    },
    {
      "event_date": "2021年1月1日",
      "topic": "非主流矿供应情况",
      "content": "2021年非主流矿供应价格弹性较主流矿山更大，一方面原因在于非主流矿不具备成本优势，而且非主流矿多为低品质矿，折扣较高，矿价下跌首先波及高价资源，另一方面除中国外其他国家铁水产量恢复以及经济复苏带来的本地需求增加，非主流矿出口至中国的量显著下滑，2021年1-11月份印度进口量累计为3323.16万吨，同比下降14.47%，南非累计进口量为3799.86万吨，同比下降12.26%，南非进口量相对平稳，非主流供给弹性更大，应予以更多关注。",
      "type": "供给端动态",
      "type_region": "国外信息"
    },
    {
      "event_date": "2021年1月1日",
      "topic": "国产矿季节性走弱",
      "content": "2021年国内铁矿石原矿量为98052.80万吨，增幅9.4%，同比升8425.0万吨，按照品位66%（原矿品位25%*回收率85%）理论折算精矿2021年精矿产量为3.16亿吨，同比增加2712万吨。2021年原矿产量呈现前高后低趋势，上半年国内需求不断释放叠加铁矿石价格不断走高，矿山企业生产积极性高，但随着矿价在5月中旬达到最高值后震荡下行，7月下旬开始加速下跌，原矿产量反应相对滞后一个月左右，原矿产量在6月份创出2018年以来最高值单月产量8786.90万吨之后开始持续下滑，截止到11月份原矿产量仅为7839.60万吨，较高点降幅为10.8%。",
      "type": "供给端动态",
      "type_region": "国内信息"
    },
    {
      "event_date": "2021年1月1日",
      "topic": "主流矿山供应情况",
      "content": "2021年主流矿山供应增量来自巴西淡水河谷，主要是其产能恢复以及生产效率提高，澳洲矿山由于自身产能增量限制以及突发恶劣天气、疫情影响、检修增加等因素对于供应增量贡献较低，展望2022年，澳洲方面增量仍相对悲观，增量仍将来自淡水河谷产能持续恢复和发运水平的主动提高。",
      "type": "供给端动态",
      "type_region": "国外信息"
    },
    {
      "event_date": "2022年2月1日",
      "topic": "2月份到港量下降",
      "content": "2022年2月份属于传统发运淡季，结合澳洲存在飓风等不确定性因素影响，叠加铁矿石到港量将环比持续回落，主流矿山供给端对现货价格的支撑力度将增强。",
      "type": "供给端动态",
      "type_region": "国外信息"
    },
    {
      "event_date": "2021年1月1日",
      "topic": "国内需求边际回升",
      "content": "2021年上半年由于新增产能投放、产能利用率提升、唐山以外地区环保限产宽松、钢厂盈利能力平稳以及终端需求强劲等因素共同作用下生铁产量不断释放，但下半年粗钢压减政策严格执行叠加钢厂低利润水平下主动限产，铁水产量出现断崖式下跌并且持续维持低位水平，根据国家统计局数据，2021年1～12月我国生铁累计产量86856.80万吨，同比降幅4.3%，同比下降3902.66万吨。国家统计局数据显示，2021年1-12月粗钢累计产量103279.0万吨，同比下降3.00%，同比下降3194.20万吨。从上述比较可以得到2021年由生铁贡献粗钢全部减量，假设2022年粗钢产量继续下降1500万吨左右，则我们预计2022年国内铁矿石需求下降2400万吨，根据上述假设，我们预估2022年全国铁水年均日均铁水下降6.6万吨/日至231万吨/日。",
      "type": "需求端动态",
      "type_region": "国内信息"
    },
    {
      "event_date": "2022年2月1日",
      "topic": "2月份行情展望",
      "content": "短期随着铁矿石需求边际回升以及供应端边际走弱，铁矿石供需关系由宽松走向平衡偏紧，支撑铁矿石价格走强，但当前钢厂补库进入尾声，叠加冬奥会限产预期，钢厂进一步复产以及补库需求均受到抑制，短期铁矿石需求面临阶段性压力，到港量由于前期发运减少导致将出现一定回落。随着需求阶段性压力出现，矿价继续走强驱动略有不足，然而中期市场整体预期铁水仍将有较大增加空间。",
      "type": "价格走势",
      "type_region": "国内信息"
    }
  ]
}
```
+ 最后将json 数据转化为pandas数据库，存储在sqlite数据库中

