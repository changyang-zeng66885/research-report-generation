# 数据表一览：铁矿石

> 数据结构说明：
> + <表名>  数据表含义的必要说明
>   + <字段名1> 字段1的必要说明
>   + <字段名2> 字段2的必要说明

## 走势回顾相关
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

## 供给分析相关
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
+ Supply_IronOre 铁矿石供给发运量(单位：万吨)（记录日期范围：2020.10.16-2023.11.20）
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
## 新闻动态观点数据
+ Events 重要的事件节点（记录日期:2021年1月1日-2022年8月31日）
  + id 事件id (自增属性)
  + event_id 事件id(唯一标识)
  + event_start_date　事件或信息的开始时间节点.如：2021年4月13日。例如，如果一件事情发生于2024年1月-11月，则该项为 2024年1月1日
  + event_end_date　　　事件或信息的结束时间节点。如：2021年4月15日。例如，如果一件事情发生于2024年1月-11月，则该项为 2024年11月30日 
  + topic 该事件的内容概括 
  + content 该事件的内容 
  + type 　该事件的类型；取值范围为：[价格走势、政策信息、供给端动态、需求端动态、供需关系]
  + type_region 　该事件的范围；取值范围为:[国内信息，国外信息]
  // 请注意，如果要查询某一段事件的重要事件节点（例如t1-t2事件段内的重要事件）， 可以这样查:SELECT * FROM Events WHERE event_start_date >= t1 OR event_start_date <= t2 ;
  // 例如: 查询 2022年1月-3月，国内供给端的主要新闻
  // 返回的SQL： SELECT * FROM Events WHERE  event_start_date >= '2022-01-01' OR event_end_date <= '2022-03-31';
  

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

## 其他数据
+ PusiIndex 普氏铁矿石62%指数（记录日期范围：2013.1.2-2023.11.14）
  + IndexDate	
  + PusiIndex62USD


+ Steel_Company_Profitability 钢铁企业盈利率_中国_周(记录日期范围：2019.1.4-2023.11.10)
  + IndexDate 
  + profitability_rate

## 数据库说明
+ 数据库使用的是SQLite
+ 本数据库不支持 YEAR() 函数，可以使用 strftime 函数