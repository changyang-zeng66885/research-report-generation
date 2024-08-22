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
+ 整理研报中重要的时间节点+信息
+ 将研报数据转化成 json 数据，具体而言应包括以下属性：

  + 研报标题
  + 研报发布时间（xxxx年xx月）
  + 观点内容
  + 观点类型（政策信息，数据走势，市场情绪。。。。）
  + 观点时间（xxxx年xx月）
```json
{
  "title": "研报标题",
  "publish_date": "xxxx年xx月",
  "content": "观点内容",
  "type": "观点类型",
  "view_date": "xxxx年xx月"
}
```
+ 最后将json 数据转化为pandas数据库，存储在sqlite数据库中