# 股票 CFI 分类个体本体（Equities CFI Classification Individuals Ontology）结构与公理说明

本文档对应 `EquityCFIClassificationIndividuals.rdf` / `EquityCFIClassificationIndividuals.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `EquityCFIClassificationIndividuals-structure.png`（`EquityCFIClassificationIndividuals-structure.svg` 为可缩放版本）。

![股票 CFI 分类个体本体（Equities CFI Classification Individuals Ontology）本体结构图](EquityCFIClassificationIndividuals-structure.png)

## 1. 本体概述

收录 ISO 10962 金融工具分类（CFI）中股票类别的参考个体（普通股、优先股等类别代码），并含少量配套类定义。

**在体系中的位置**：SEC 权益模块的参考数据层。

**上下游关系**：上游依赖证券分类与股权工具本体；下游为按 CFI 标准标注股票数据提供取值。

**与相近概念的差别**：CFI 代码是六位字母的分类编码（如 ESVUFR），区别于标识证券个体的 ISIN；与其他 CFI 分类（债务、衍生品）是平行分支。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）** 继承 **普通股（CommonShare）**
- **增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）** 继承 **增强表决权股（EnhancedVotingShare）**
- **增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）** 继承 **缴足股（FullyPaidShare）**
- **增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）** 继承 **受限股份（RestrictedShare）**
- **增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）** 继承 **注册证券（RegisteredSecurity）**
- **增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）** 继承 **普通股（CommonShare）**
- **增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）** 继承 **增强表决权股（EnhancedVotingShare）**
- **增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）** 继承 **未缴股款股份（NilPaidShare）**
- **增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）** 继承 **受限股份（RestrictedShare）**
- **增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）** 继承 **注册证券（RegisteredSecurity）**
- **增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare）** 继承 **普通股（CommonShare）**
- **增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare）** 继承 **增强表决权股（EnhancedVotingShare）**
- 其余 1104 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is restricted from a sales / transfer perspective, is fully paid and is registered |
| 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is restricted from a sales / transfer perspective, is nil paid and is registered |
| 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is restricted from a sales / transfer perspective, is partially paid and is registered |
| 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is not restricted from a sales / transfer perspective, is fully paid and is registered |
| 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is not restricted from a sales / transfer perspective, is nil paid and is registered |
| 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有多于一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers multiple votes per share, is not restricted from a sales / transfer perspective, is partially paid and is registered |
| 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is restricted from a sales / transfer perspective, is fully paid and is registered |
| 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is restricted from a sales / transfer perspective, is nil paid and is registered |
| 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is restricted from a sales / transfer perspective, is partially paid and is registered |
| 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is unrestricted from a sales perspective, is fully paid and is registered |
| 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is unrestricted from a sales perspective, is nil paid and is registered |
| 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股不享有表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly 0 votes per share, is unrestricted from a sales perspective, is partially paid and is registered |
| 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is restricted from a sales / transfer perspective, is fully paid and is registered |
| 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is restricted from a sales / transfer perspective, is nil paid and is registered |
| 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is restricted from a sales / transfer perspective, is partially paid and is registered |
| 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is unrestricted from a sales / transfer perspective, is fully paid and is registered |
| 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is unrestricted from a sales / transfer perspective, is nil paid and is registered |
| 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有不足一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers less than one vote per share, is unrestricted from a sales / transfer perspective, is partially paid and is registered |
| 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is restricted from a sales / transfer perspective, is fully paid and is registered |
| 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is restricted from a sales / transfer perspective, is nil paid and is registered |
| 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is restricted from a sales / transfer perspective, is partially paid and is registered |
| 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is unrestricted from a sales perspective, is fully paid and is registered |
| 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is unrestricted from a sales perspective, is nil paid and is registered |
| 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare） | 普通股：每股享有一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>common share that confers exactly one vote per share, is unrestricted from a sales perspective, is partially paid and is registered |
| 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic stated income, and is registered |
| 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, and is registered |
| 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic stated income, and is registered |
| 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, has no fixed maturity date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有多于一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers multiple votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic stated income, and is registered |
| 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare） | 优先股：每股不享有表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, and is registered |
| 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic stated income, and is registered |
| 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare） | 优先股：每股不享有表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, has no fixed maturity date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare） | 优先股：每股不享有表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers zero votes per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income, and is registered |
| 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, and is registered |
| 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic stated income, and is registered |
| 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, has no fixed maturity date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有不足一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers less than one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income, and is registered |
| 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income, and is registered |
| 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder with an extendable redemption date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic stated income, and is registered |
| 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare） | 优先股：每股享有一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, has no fixed maturity date, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one per share, may be exchanged for securities of another issuer, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is set periodically, and is registered |
| 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic income whose dividend rate is adjusted through an auction, and is registered |
| 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, dividends not paid in any year accumulate, and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and dividends not paid in any year accumulate, and is registered |
| 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income, and is registered |
| 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, whose issuer and/or shareholders have the option to extend the maturity date, that provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |
| 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income, and is registered |
| 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides the same dividends as common/ordinary shareholders, and is registered |
| 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare） | 优先股：每股享有一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。<br>preferred share that confers exactly one vote per share, may be redeemed at the option of the issuer and/or of the shareholder, provides a periodic stated income and participates with common shareholders in further dividend and capital distributions, and is registered |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 增强表决权、转让受限、缴足普通股（CommonEnhancedVotingRestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**缴足股（FullyPaidShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESETFR。

### 2.2 增强表决权、转让受限、未缴普通股（CommonEnhancedVotingRestrictedNilPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**未缴股款股份（NilPaidShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESETOR。

### 2.3 增强表决权、转让受限、部分缴足普通股（CommonEnhancedVotingRestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**部分缴足股（PartiallyPaidShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESETPR。

### 2.4 增强表决权、转让不受限、缴足普通股（CommonEnhancedVotingUnrestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**缴足股（FullyPaidShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESEUFR。

### 2.5 增强表决权、转让不受限、未缴普通股（CommonEnhancedVotingUnrestrictedNilPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**未缴股款股份（NilPaidShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESEUOR。

### 2.6 增强表决权、转让不受限、部分缴足普通股（CommonEnhancedVotingUnrestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有多于一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**增强表决权股（EnhancedVotingShare）**、**部分缴足股（PartiallyPaidShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESEUPR。

### 2.7 无表决权、转让受限、缴足普通股（CommonNonVotingRestrictedFullyPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**无表决权股（NonVotingShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNTFR。

### 2.8 无表决权、转让受限、未缴普通股（CommonNonVotingRestrictedNilPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**无表决权股（NonVotingShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNTOR。

### 2.9 无表决权、转让受限、部分缴足普通股（CommonNonVotingRestrictedPartlyPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**无表决权股（NonVotingShare）**、**部分缴足股（PartiallyPaidShare）**、**受限股份（RestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNTPR。

### 2.10 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**无表决权股（NonVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNUFR。

### 2.11 无表决权、转让不受限、未缴普通股（CommonNonVotingUnrestrictedNilPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**无表决权股（NonVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNUOR。

### 2.12 无表决权、转让不受限、部分缴足普通股（CommonNonVotingUnrestrictedPartlyPaidRegisteredShare）

定义：普通股：每股不享有表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**无表决权股（NonVotingShare）**、**部分缴足股（PartiallyPaidShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESNUPR。

### 2.13 受限表决权、转让受限、缴足普通股（CommonRestrictedVotingRestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**受限股份（RestrictedShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRTFR。

### 2.14 受限表决权、转让受限、未缴普通股（CommonRestrictedVotingRestrictedNilPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**受限股份（RestrictedShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRTOR。

### 2.15 受限表决权、转让受限、部分缴足普通股（CommonRestrictedVotingRestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**部分缴足股（PartiallyPaidShare）**、**受限股份（RestrictedShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRTPR。

### 2.16 受限表决权、转让不受限、缴足普通股（CommonRestrictedVotingUnrestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**受限表决权股（RestrictedVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRUFR。

### 2.17 受限表决权、转让不受限、未缴普通股（CommonRestrictedVotingUnrestrictedNilPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**受限表决权股（RestrictedVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRUOR。

### 2.18 受限表决权、转让不受限、部分缴足普通股（CommonRestrictedVotingUnrestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有不足一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**部分缴足股（PartiallyPaidShare）**、**受限表决权股（RestrictedVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESRUPR。

### 2.19 单一表决权、转让受限、缴足普通股（CommonVotingRestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**受限股份（RestrictedShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVTFR。

### 2.20 单一表决权、转让受限、未缴普通股（CommonVotingRestrictedNilPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**受限股份（RestrictedShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVTOR。

### 2.21 单一表决权、转让受限、部分缴足普通股（CommonVotingRestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**部分缴足股（PartiallyPaidShare）**、**受限股份（RestrictedShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVTPR。

### 2.22 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让不受限；股款已缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**缴足股（FullyPaidShare）**、**单一表决权股（SingleVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVUFR。

### 2.23 单一表决权、转让不受限、未缴普通股（CommonVotingUnrestrictedNilPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让不受限；股款未缴，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**未缴股款股份（NilPaidShare）**、**单一表决权股（SingleVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVUOR。

### 2.24 单一表决权、转让不受限、部分缴足普通股（CommonVotingUnrestrictedPartlyPaidRegisteredShare）

定义：普通股：每股享有一票表决权；出售/转让不受限；股款部分缴足，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**普通股（CommonShare）**、**部分缴足股（PartiallyPaidShare）**、**单一表决权股（SingleVotingShare）**、**非受限股份（UnrestrictedShare）**、**注册证券（RegisteredSecurity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**的取值固定为 ESVUPR。

### 2.25 增强表决权、可交换、可调整收益优先股（PreferredEnhancedVotingExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.26 增强表决权、可交换、拍卖利率收益优先股（PreferredEnhancedVotingExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.27 增强表决权、可交换、累积参与优先股（PreferredEnhancedVotingExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.28 增强表决权、可交换、累积优先股（PreferredEnhancedVotingExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.29 增强表决权、可交换、固定收益优先股（PreferredEnhancedVotingExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.30 增强表决权、可交换、普通收益优先股（PreferredEnhancedVotingExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**注册证券（RegisteredSecurity）**

### 2.31 增强表决权、可交换、参与优先股（PreferredEnhancedVotingExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.32 增强表决权、可展期、可调整收益优先股（PreferredEnhancedVotingExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.33 增强表决权、可展期、拍卖利率收益优先股（PreferredEnhancedVotingExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.34 增强表决权、可展期、累积参与优先股（PreferredEnhancedVotingExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.35 增强表决权、可展期、累积优先股（PreferredEnhancedVotingExtendableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.36 增强表决权、可展期、固定收益优先股（PreferredEnhancedVotingExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.37 增强表决权、可展期、普通收益优先股（PreferredEnhancedVotingExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.38 增强表决权、可展期、参与优先股（PreferredEnhancedVotingExtendableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.39 增强表决权、永续、可调整收益优先股（PreferredEnhancedVotingPerpetualAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.40 增强表决权、永续、拍卖利率收益优先股（PreferredEnhancedVotingPerpetualAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.41 增强表决权、永续、累积参与优先股（PreferredEnhancedVotingPerpetualCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.42 增强表决权、永续、累积优先股（PreferredEnhancedVotingPerpetualCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.43 增强表决权、永续、固定收益优先股（PreferredEnhancedVotingPerpetualFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.44 增强表决权、永续、普通收益优先股（PreferredEnhancedVotingPerpetualNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**非累积优先股（NonCumulativePreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**注册证券（RegisteredSecurity）**

### 2.45 增强表决权、永续、参与优先股（PreferredEnhancedVotingPerpetualParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.46 增强表决权、可赎回、可调整收益优先股（PreferredEnhancedVotingRedeemableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.47 增强表决权、可赎回、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.48 增强表决权、可赎回、累积参与优先股（PreferredEnhancedVotingRedeemableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.49 增强表决权、可赎回、累积优先股（PreferredEnhancedVotingRedeemableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.50 增强表决权、可赎回、可交换、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.51 增强表决权、可赎回、可交换、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.52 增强表决权、可赎回、可交换、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.53 增强表决权、可赎回、可交换、累积优先股（PreferredEnhancedVotingRedeemableExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.54 增强表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.55 增强表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.56 增强表决权、可赎回、可交换、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.57 增强表决权、可赎回、可交换、可展期、累积优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.58 增强表决权、可赎回、可交换、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.59 增强表决权、可赎回、可交换、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.60 增强表决权、可赎回、可交换、可展期、参与优先股（PreferredEnhancedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.61 增强表决权、可赎回、可交换、固定收益优先股（PreferredEnhancedVotingRedeemableExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.62 增强表决权、可赎回、可交换、普通收益优先股（PreferredEnhancedVotingRedeemableExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.63 增强表决权、可赎回、可交换、参与优先股（PreferredEnhancedVotingRedeemableExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.64 增强表决权、可赎回、可展期、可调整收益优先股（PreferredEnhancedVotingRedeemableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.65 增强表决权、可赎回、可展期、拍卖利率收益优先股（PreferredEnhancedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.66 增强表决权、可赎回、可展期、累积参与优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.67 增强表决权、可赎回、可展期、累积优先股（PreferredEnhancedVotingRedeemableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.68 增强表决权、可赎回、可展期、固定收益优先股（PreferredEnhancedVotingRedeemableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.69 增强表决权、可赎回、可展期、普通收益优先股（PreferredEnhancedVotingRedeemableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.70 增强表决权、可赎回、可展期、参与优先股（PreferredEnhancedVotingRedeemableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.71 增强表决权、可赎回、固定收益优先股（PreferredEnhancedVotingRedeemableFixedIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.72 增强表决权、可赎回、普通收益优先股（PreferredEnhancedVotingRedeemableNormalIncomeRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.73 增强表决权、可赎回、参与优先股（PreferredEnhancedVotingRedeemableParticipatingRegisteredShare）

定义：优先股：每股享有多于一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**增强表决权股（EnhancedVotingShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.74 无表决权、可交换、可调整收益优先股（PreferredNonVotingExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.75 无表决权、可交换、拍卖利率收益优先股（PreferredNonVotingExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.76 无表决权、可交换、累积参与优先股（PreferredNonVotingExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.77 无表决权、可交换、累积优先股（PreferredNonVotingExchangeableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.78 无表决权、可交换、固定收益优先股（PreferredNonVotingExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.79 无表决权、可交换、普通收益优先股（PreferredNonVotingExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.80 无表决权、可交换、参与优先股（PreferredNonVotingExchangeableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.81 无表决权、可展期、可调整收益优先股（PreferredNonVotingExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.82 无表决权、可展期、拍卖利率收益优先股（PreferredNonVotingExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.83 无表决权、可展期、累积参与优先股（PreferredNonVotingExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.84 无表决权、可展期、累积优先股（PreferredNonVotingExtendableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.85 无表决权、可展期、固定收益优先股（PreferredNonVotingExtendableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.86 无表决权、可展期、普通收益优先股（PreferredNonVotingExtendableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.87 无表决权、可展期、参与优先股（PreferredNonVotingExtendableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.88 无表决权、永续、可调整收益优先股（PreferredNonVotingPerpetualAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**无表决权股（NonVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.89 无表决权、永续、拍卖利率收益优先股（PreferredNonVotingPerpetualAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**无表决权股（NonVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.90 无表决权、永续、累积参与优先股（PreferredNonVotingPerpetualCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.91 无表决权、永续、累积优先股（PreferredNonVotingPerpetualCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.92 无表决权、永续、固定收益优先股（PreferredNonVotingPerpetualFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.93 无表决权、永续、普通收益优先股（PreferredNonVotingPerpetualNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**永续优先股（PerpetualPreferredShare）**、**注册证券（RegisteredSecurity）**

### 2.94 无表决权、永续、参与优先股（PreferredNonVotingPerpetualParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

### 2.95 无表决权、可赎回、可调整收益优先股（PreferredNonVotingRedeemableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.96 无表决权、可赎回、拍卖利率收益优先股（PreferredNonVotingRedeemableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.97 无表决权、可赎回、累积参与优先股（PreferredNonVotingRedeemableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.98 无表决权、可赎回、累积优先股（PreferredNonVotingRedeemableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.99 无表决权、可赎回、可交换、可调整收益优先股（PreferredNonVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.100 无表决权、可赎回、可交换、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.101 无表决权、可赎回、可交换、累积参与优先股（PreferredNonVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.102 无表决权、可赎回、可交换、累积优先股（PreferredNonVotingRedeemableExchangeableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.103 无表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.104 无表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.105 无表决权、可赎回、可交换、可展期、累积参与优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.106 无表决权、可赎回、可交换、可展期、累积优先股（PreferredNonVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.107 无表决权、可赎回、可交换、可展期、固定收益优先股（PreferredNonVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.108 无表决权、可赎回、可交换、可展期、普通收益优先股（PreferredNonVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.109 无表决权、可赎回、可交换、可展期、参与优先股（PreferredNonVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.110 无表决权、可赎回、可交换、固定收益优先股（PreferredNonVotingRedeemableExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.111 无表决权、可赎回、可交换、普通收益优先股（PreferredNonVotingRedeemableExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.112 无表决权、可赎回、可交换、参与优先股（PreferredNonVotingRedeemableExchangeableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.113 无表决权、可赎回、可展期、可调整收益优先股（PreferredNonVotingRedeemableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.114 无表决权、可赎回、可展期、拍卖利率收益优先股（PreferredNonVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.115 无表决权、可赎回、可展期、累积参与优先股（PreferredNonVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.116 无表决权、可赎回、可展期、累积优先股（PreferredNonVotingRedeemableExtendableCumulativeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.117 无表决权、可赎回、可展期、固定收益优先股（PreferredNonVotingRedeemableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.118 无表决权、可赎回、可展期、普通收益优先股（PreferredNonVotingRedeemableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.119 无表决权、可赎回、可展期、参与优先股（PreferredNonVotingRedeemableExtendableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.120 无表决权、可赎回、固定收益优先股（PreferredNonVotingRedeemableFixedIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**无表决权股（NonVotingShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.121 无表决权、可赎回、普通收益优先股（PreferredNonVotingRedeemableNormalIncomeRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**无表决权股（NonVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.122 无表决权、可赎回、参与优先股（PreferredNonVotingRedeemableParticipatingRegisteredShare）

定义：优先股：每股不享有表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**无表决权股（NonVotingShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.123 受限表决权、可交换、可调整收益优先股（PreferredRestrictedVotingExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.124 受限表决权、可交换、拍卖利率收益优先股（PreferredRestrictedVotingExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.125 受限表决权、可交换、累积参与优先股（PreferredRestrictedVotingExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.126 受限表决权、可交换、累积优先股（PreferredRestrictedVotingExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.127 受限表决权、可交换、固定收益优先股（PreferredRestrictedVotingExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.128 受限表决权、可交换、普通收益优先股（PreferredRestrictedVotingExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.129 受限表决权、可交换、参与优先股（PreferredRestrictedVotingExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.130 受限表决权、可展期、可调整收益优先股（PreferredRestrictedVotingExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.131 受限表决权、可展期、拍卖利率收益优先股（PreferredRestrictedVotingExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.132 受限表决权、可展期、累积参与优先股（PreferredRestrictedVotingExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.133 受限表决权、可展期、累积优先股（PreferredRestrictedVotingExtendableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.134 受限表决权、可展期、固定收益优先股（PreferredRestrictedVotingExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.135 受限表决权、可展期、普通收益优先股（PreferredRestrictedVotingExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.136 受限表决权、可展期、参与优先股（PreferredRestrictedVotingExtendableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.137 受限表决权、永续、可调整收益优先股（PreferredRestrictedVotingPerpetualAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**永续优先股（PerpetualPreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.138 受限表决权、永续、拍卖利率收益优先股（PreferredRestrictedVotingPerpetualAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**永续优先股（PerpetualPreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.139 受限表决权、永续、累积参与优先股（PreferredRestrictedVotingPerpetualCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.140 受限表决权、永续、累积优先股（PreferredRestrictedVotingPerpetualCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.141 受限表决权、永续、固定收益优先股（PreferredRestrictedVotingPerpetualFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.142 受限表决权、永续、普通收益优先股（PreferredRestrictedVotingPerpetualNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.143 受限表决权、永续、参与优先股（PreferredRestrictedVotingPerpetualParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.144 受限表决权、可赎回、可调整收益优先股（PreferredRestrictedVotingRedeemableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.145 受限表决权、可赎回、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.146 受限表决权、可赎回、累积参与优先股（PreferredRestrictedVotingRedeemableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.147 受限表决权、可赎回、累积优先股（PreferredRestrictedVotingRedeemableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.148 受限表决权、可赎回、可交换、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.149 受限表决权、可赎回、可交换、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.150 受限表决权、可赎回、可交换、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.151 受限表决权、可赎回、可交换、累积优先股（PreferredRestrictedVotingRedeemableExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.152 受限表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.153 受限表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.154 受限表决权、可赎回、可交换、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.155 受限表决权、可赎回、可交换、可展期、累积优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.156 受限表决权、可赎回、可交换、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.157 受限表决权、可赎回、可交换、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.158 受限表决权、可赎回、可交换、可展期、参与优先股（PreferredRestrictedVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.159 受限表决权、可赎回、可交换、固定收益优先股（PreferredRestrictedVotingRedeemableExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.160 受限表决权、可赎回、可交换、普通收益优先股（PreferredRestrictedVotingRedeemableExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.161 受限表决权、可赎回、可交换、参与优先股（PreferredRestrictedVotingRedeemableExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.162 受限表决权、可赎回、可展期、可调整收益优先股（PreferredRestrictedVotingRedeemableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.163 受限表决权、可赎回、可展期、拍卖利率收益优先股（PreferredRestrictedVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.164 受限表决权、可赎回、可展期、累积参与优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.165 受限表决权、可赎回、可展期、累积优先股（PreferredRestrictedVotingRedeemableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.166 受限表决权、可赎回、可展期、固定收益优先股（PreferredRestrictedVotingRedeemableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.167 受限表决权、可赎回、可展期、普通收益优先股（PreferredRestrictedVotingRedeemableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.168 受限表决权、可赎回、可展期、参与优先股（PreferredRestrictedVotingRedeemableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.169 受限表决权、可赎回、固定收益优先股（PreferredRestrictedVotingRedeemableFixedIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.170 受限表决权、可赎回、普通收益优先股（PreferredRestrictedVotingRedeemableNormalIncomeRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.171 受限表决权、可赎回、参与优先股（PreferredRestrictedVotingRedeemableParticipatingRegisteredShare）

定义：优先股：每股享有不足一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**受限表决权股（RestrictedVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.172 单一表决权、可交换、可调整收益优先股（PreferredVotingExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.173 单一表决权、可交换、拍卖利率收益优先股（PreferredVotingExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.174 单一表决权、可交换、累积参与优先股（PreferredVotingExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.175 单一表决权、可交换、累积优先股（PreferredVotingExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.176 单一表决权、可交换、固定收益优先股（PreferredVotingExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.177 单一表决权、可交换、普通收益优先股（PreferredVotingExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.178 单一表决权、可交换、参与优先股（PreferredVotingExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.179 单一表决权、可展期、可调整收益优先股（PreferredVotingExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.180 单一表决权、可展期、拍卖利率收益优先股（PreferredVotingExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.181 单一表决权、可展期、累积参与优先股（PreferredVotingExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.182 单一表决权、可展期、累积优先股（PreferredVotingExtendableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.183 单一表决权、可展期、固定收益优先股（PreferredVotingExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.184 单一表决权、可展期、普通收益优先股（PreferredVotingExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.185 单一表决权、可展期、参与优先股（PreferredVotingExtendableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.186 单一表决权、永续、可调整收益优先股（PreferredVotingPerpetualAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**永续优先股（PerpetualPreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.187 单一表决权、永续、拍卖利率收益优先股（PreferredVotingPerpetualAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**永续优先股（PerpetualPreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.188 单一表决权、永续、累积参与优先股（PreferredVotingPerpetualCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.189 单一表决权、永续、累积优先股（PreferredVotingPerpetualCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.190 单一表决权、永续、固定收益优先股（PreferredVotingPerpetualFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.191 单一表决权、永续、普通收益优先股（PreferredVotingPerpetualNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.192 单一表决权、永续、参与优先股（PreferredVotingPerpetualParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；无固定到期日；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**永续优先股（PerpetualPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

### 2.193 单一表决权、可赎回、可调整收益优先股（PreferredVotingRedeemableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.194 单一表决权、可赎回、拍卖利率收益优先股（PreferredVotingRedeemableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.195 单一表决权、可赎回、累积参与优先股（PreferredVotingRedeemableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.196 单一表决权、可赎回、累积优先股（PreferredVotingRedeemableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.197 单一表决权、可赎回、可交换、可调整收益优先股（PreferredVotingRedeemableExchangeableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.198 单一表决权、可赎回、可交换、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.199 单一表决权、可赎回、可交换、累积参与优先股（PreferredVotingRedeemableExchangeableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.200 单一表决权、可赎回、可交换、累积优先股（PreferredVotingRedeemableExchangeableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.201 单一表决权、可赎回、可交换、可展期、可调整收益优先股（PreferredVotingRedeemableExchangeableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.202 单一表决权、可赎回、可交换、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExchangeableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.203 单一表决权、可赎回、可交换、可展期、累积参与优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.204 单一表决权、可赎回、可交换、可展期、累积优先股（PreferredVotingRedeemableExchangeableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.205 单一表决权、可赎回、可交换、可展期、固定收益优先股（PreferredVotingRedeemableExchangeableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.206 单一表决权、可赎回、可交换、可展期、普通收益优先股（PreferredVotingRedeemableExchangeableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.207 单一表决权、可赎回、可交换、可展期、参与优先股（PreferredVotingRedeemableExchangeableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.208 单一表决权、可赎回、可交换、固定收益优先股（PreferredVotingRedeemableExchangeableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.209 单一表决权、可赎回、可交换、普通收益优先股（PreferredVotingRedeemableExchangeableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.210 单一表决权、可赎回、可交换、参与优先股（PreferredVotingRedeemableExchangeableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；可交换为另一发行人的证券；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可交换优先股（ExchangeablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.211 单一表决权、可赎回、可展期、可调整收益优先股（PreferredVotingRedeemableExtendableAdjustableIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率按基准定期调整，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**可调整利率股息优先股（PreferredShareWithAdjustableRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.212 单一表决权、可赎回、可展期、拍卖利率收益优先股（PreferredVotingRedeemableExtendableAuctionRateIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；股息率通过拍卖定期重置，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**拍卖利率股息优先股（PreferredShareWithAuctionRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.213 单一表决权、可赎回、可展期、累积参与优先股（PreferredVotingRedeemableExtendableCumulativeParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延，并可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.214 单一表决权、可赎回、可展期、累积优先股（PreferredVotingRedeemableExtendableCumulativeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；未付股息累积递延至日后支付，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**累积优先股（CumulativePreferredShare）**、**可展期优先股（ExtendablePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.215 单一表决权、可赎回、可展期、固定收益优先股（PreferredVotingRedeemableExtendableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.216 单一表决权、可赎回、可展期、普通收益优先股（PreferredVotingRedeemableExtendableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.217 单一表决权、可赎回、可展期、参与优先股（PreferredVotingRedeemableExtendableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；到期日可由发行人和/或股东选择延长；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**可展期优先股（ExtendablePreferredShare）**、**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.218 单一表决权、可赎回、固定收益优先股（PreferredVotingRedeemableFixedIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；按约定利率提供定期固定收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**非参与优先股（NonParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.219 单一表决权、可赎回、普通收益优先股（PreferredVotingRedeemableNormalIncomeRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；提供与普通股股东相同的股息，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

### 2.220 单一表决权、可赎回、参与优先股（PreferredVotingRedeemableParticipatingRegisteredShare）

定义：优先股：每股享有一票表决权；发行人或股东可选择赎回；除约定股息外可与普通股股东分享额外收益，记名股份。属 ISO 10962（CFI）股票分类中的组合类别个体。

- 父类：**非累积优先股（NonCumulativePreferredShare）**、**参与优先股（ParticipatingPreferredShare）**、**固定利率股息优先股（PreferredShareWithFixedRateDividend）**、**单一表决权股（SingleVotingShare）**、**注册证券（RegisteredSecurity）**

公理：

- 该属性存在取值约束。

## 3. 依赖（owl:imports，9 个）

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

## 4. 文件

- 官方 RDF/XML：`EquityCFIClassificationIndividuals.rdf`
- 中文 Turtle：`EquityCFIClassificationIndividuals.ttl`
- 结构图：`EquityCFIClassificationIndividuals-structure.png` / `EquityCFIClassificationIndividuals-structure.svg`