# 股票 CFI 分类个体本体（Equities CFI Classification Individuals Ontology）结构与公理说明

本文档对应 `EquityCFIClassificationIndividuals.rdf` / `EquityCFIClassificationIndividuals.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `EquityCFIClassificationIndividuals-structure.png`（`EquityCFIClassificationIndividuals-structure.svg` 为可缩放版本）。

![股票 CFI 分类个体本体（Equities CFI Classification Individuals Ontology）本体结构图](EquityCFIClassificationIndividuals-structure.png)

## 1. 本体概述

收录 ISO 10962 金融工具分类（CFI）中股票类别的参考个体（普通股、优先股等类别代码），并含少量配套类定义。

**在体系中的位置**：SEC 权益模块的参考数据层。

**上下游关系**：上游依赖证券分类与股权工具本体；下游为按 CFI 标准标注股票数据提供取值。

**与相近概念的差别**：CFI 代码是六位字母的分类编码（如 ESVUFR），区别于标识证券个体的 ISIN；与其他 CFI 分类（债务、衍生品）是平行分支。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |
| 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。 |

### 2.1 继承关系（Inheritance）

- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） ⊑ 受限股份
- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） ⊑ 受限股份
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 受限股份
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 非受限股份
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 非受限股份
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 增强表决权股
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 非受限股份
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） ⊑ 受限股份
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） ⊑ 受限股份
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 受限股份
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 非受限股份
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 非受限股份
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 无表决权股
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 非受限股份
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） ⊑ 受限股份
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） ⊑ 受限股份
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 受限股份
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 非受限股份
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 非受限股份
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 受限表决权股
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 非受限股份
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） ⊑ 受限股份
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） ⊑ 受限股份
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 受限股份
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 缴足股
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 非受限股份
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 未缴股款股份
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 非受限股份
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） ⊑ 注册证券
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 普通股
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 部分缴足股
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 单一表决权股
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 非受限股份
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 永续优先股
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare） ⊑ 注册证券
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） ⊑ 增强表决权股
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） ⊑ 非累积优先股
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） ⊑ 参与优先股
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 永续优先股
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare） ⊑ 注册证券
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） ⊑ 非累积优先股
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） ⊑ 无表决权股
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） ⊑ 参与优先股
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 永续优先股
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare） ⊑ 注册证券
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） ⊑ 非累积优先股
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） ⊑ 参与优先股
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） ⊑ 受限表决权股
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 永续优先股
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 可交换优先股
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 可调整利率股息优先股
- 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 拍卖利率股息优先股
- 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 累积优先股
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 可展期优先股
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） ⊑ 非参与优先股
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare） ⊑ 注册证券
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） ⊑ 非累积优先股
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） ⊑ 参与优先股
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） ⊑ 固定利率股息优先股
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） ⊑ 单一表决权股
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） ⊑ 注册证券

## 5. 公理约定（Axioms）

- 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）：restriction
- 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）：restriction
- 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare）：restriction
- 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare）：restriction
- 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare）：restriction
- 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare）：restriction
- 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare）：restriction
- 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare）：restriction
- 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare）：restriction
- 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare）：restriction
- 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare）：restriction
- 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare）：restriction
- 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare）：restriction
- 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare）：restriction
- 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare）：restriction
- 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare）：restriction
- 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare）：restriction
- 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare）：restriction
- 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare）：restriction
- 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare）：restriction
- 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare）：restriction
- 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare）：restriction
- 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare）：restriction
- 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare）：restriction
- 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare）：restriction
- 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare）：restriction
- 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare）：restriction
- 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare）：restriction
- 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare）：restriction
- 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare）：restriction
- 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare）：restriction
- 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare）：restriction
- 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare）：restriction
- 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare）：restriction
- 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare）：restriction
- 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare）：restriction
- 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare）：restriction
- 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare）：restriction
- 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare）：restriction
- 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare）：restriction
- 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare）：restriction
- 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare）：restriction
- 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare）：restriction
- 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare）：restriction
- 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare）：restriction
- 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare）：restriction
- 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare）：restriction
- 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare）：restriction
- 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare）：restriction
- 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare）：restriction
- 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare）：restriction
- 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare）：restriction
- 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare）：restriction
- 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare）：restriction
- 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare）：restriction
- 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare）：restriction
- 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare）：restriction
- 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare）：restriction
- 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare）：restriction
- 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare）：restriction
- 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare）：restriction
- 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare）：restriction
- 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare）：restriction
- 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare）：restriction
- 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare）：restriction

## 6. 依赖（owl:imports，9 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Securities/SecuritiesClassification.rdf` | 证券分类本体（Securities Classification Ontology） | 定义证券分类方案：按 CFI 代码、按资产类别等对证券归类。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`EquityCFIClassificationIndividuals.rdf`
- 中文 Turtle：`EquityCFIClassificationIndividuals.ttl`
- 结构图：`EquityCFIClassificationIndividuals-structure.png` / `EquityCFIClassificationIndividuals-structure.svg`