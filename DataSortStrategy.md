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
+ CrudeSteel_Production 粗钢产量
  + YearMon
  + Yield
+ MarketDate	
  + ClosingPrice	
  + SettlementPrice
+ Steel_Company_Profitability 钢铁企业盈利率_中国_周
  + IndexDate (YearMonDate)
  + profitability_rate
+ DCE01,DCE05,DCE07 大连期货交易所铁矿石期货合约价格
  + MarketDate	(~2013-2023.09.24)
  + ClosingPrice	
  + SettlementPrice
+ Demand_of_HotSteel
  + Date	
  + Quantity
+ Demand_of_Rebar
  + Date	
  + Quantity
+ IronOre_comprehensive 铁矿石综合价格
  + QUOTEDATE：报价日期，表示数据记录的日期。
  + SpotDZYangDiPowder：现货市场上某种类型的铁矿石粉末价格。
  + SpotDZPB_Powder：现货市场上另一种铁矿石粉末价格。
  + SpotDZJinBubaPowder：现货市场上金布巴（Jin Buba）铁矿石粉末的价格。
  + SpotDZKaraLaraFinePowder：现货市场上卡拉拉（Kara Lara）优质铁矿石粉末的价格。
  + SpotDZKaraJagasPowder：现货市场上卡拉贾斯（Kara Jagas）铁矿石粉末的价格。
  + SpotDZBaMixBRBF：现货市场上某种混合类型的铁矿石粉末价格。
  + SpotDZUltraSpecialPowder：现货市场上超特殊类型的铁矿石粉末价格。
  + PusiIndex62USD：62%铁矿石的普氏指数，以美元计价，反映国际市场的价格水平。
  + SpotDiscountPort：现货市场上某个港口的折扣信息。
  + BaseDZYangDiPowder：基准的杨迪铁矿石粉末价格。
  + BaseDZUltraSpecialPowder：基准的超特殊类型铁矿石粉末价格。
  + BaseDZPB_Powder：基准的PB类型铁矿石粉末价格。
  + BaseDZJinBubaPowder：基准的金布巴铁矿石粉末价格。
  + SwapJan：1月期货合约的价格
  + SwapMay：5月期货合约的价格或数据。
  + SwapSep：9月期货合约的价格或数据。
  + ImportProfitJan：1月进口铁矿石的利润情况。
  + ImportProfitMay：5月进口铁矿石的利润情况。
  + ImportProfitSep：9月进口铁矿石的利润情况。
  + RebarMineRatioSpot：现货市场上钢筋与铁矿石的比例。
  + RebarMineRatioJan：1月的钢筋与铁矿石的比例。
  + RebarMineRatioMay：5月的钢筋与铁矿石的比例。
  + RebarMineRatioOct：10月的钢筋与铁矿石的比例。
  + date：记录的日期

+ IronOre_supply 铁矿石供应
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
+ IronOre_supply_domestic 国内铁矿石供应
  + YearMon	
  + Yield
+ IronOreInventory_AUS,IronOreInventory_BRA
  + Date	
  + Quantity
+ IronOreInventory_BRA
  + Date	
  + Quantity
+ IronOreInventory_Sprase_port
  + Date	
  + Quantity
+ IronOreInventory_Total
  + Date	
  + Quantity
+ IronOreMarket
  + MarketDate	
  + Price_Jimbuba_61	
  + Price_PBFine_61_5
+ PigIronProduction_Mon
  + YearMon	
  + Yield
+ Public_oponion
  + sentiment_id	
  + title	
  + publication_time	
  + topic_tags	
  + event_tags	
  + risk_tags	
  + importance_level	
  + sentiment_source	
  + website_link	
  + news_data_source	
  + region_code	
  + region_name	
  + company_code	
  + company_name	
  + credit_code
+ PusiIndex
  + IndexDate	
  + PusiIndex62USD
+ Cost_profit_of_independent_electric_arc_furnace 独立电弧炉成本利润 
  + Date	
  + cost_electric 成本_平电	
  + cost_peak_electric 成本_峰电
  + cost_valley_electric 成本_谷电	
  + electric_cost_avg 成本_平均	
  + electric_cost_QOQ 成本_周环比	
  + profit_avg利润_平均	
  + profit_valley_electric 利润_谷电	
  + profit_valley_electric_QOQ 利润_周环比
+ rebarProduction 螺纹钢产量
  + date
  + yield













#### 访问方式

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