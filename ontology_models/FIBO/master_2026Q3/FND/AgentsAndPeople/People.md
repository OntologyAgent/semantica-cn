# 人员本体（People Ontology）结构与公理说明

本文档对应 `People.rdf` / `People.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `People-structure.png`（`People-structure.svg` 为可缩放版本）。

![人员本体（People Ontology）本体结构图](People-structure.png)

## 1. 本体概述

定义自然人（person）的核心属性：姓名、出生日期、国籍、身份标识、联系方式与家庭/社会关系。

**在体系中的位置**：FND 代理人与人员模块的核心，是雇员、客户、签署人、高管等一切「人」角色的基础。

**上下游关系**：上游依赖 FND 参与方与关系本体；下游被 BE 高管、FBC 客户、LOAN 借款人等引用。

**与相近概念的差别**：自然人≠法律主体——自然人是生物学意义上的人，法律主体是能持有权利义务的主体（含法人）；人≠参与方——人只有进入某个业务关系（签约、任职）才成为参与方。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **成年人（adult）** 继承 **个人（person）**
- **法定成年年龄（age of majority）** 继承 **法定年龄（legal age）**
- **出生证明（birth certificate）** 继承 **身份证件（identity document）**
- **出生证明（birth certificate）** 继承 **证书（Certificate）**
- **出生证明标识方案（birth certificate identification scheme）** 继承 **标识方案（IdentificationScheme）**
- **出生证明标识符（birth certificate identifier）** 继承 **标识符（Identifier）**
- **联系人（contact）** 继承 **参与方角色（party role）**
- **联系人记录（contact record）** 继承 **记录（Record）**
- **出生日期（date of birth）** 继承 **显式日期（ExplicitDate）**
- **死亡日期（date of death）** 继承 **显式日期（ExplicitDate）**
- **死亡证明（death certificate）** 继承 **身份证件（identity document）**
- **死亡证明（death certificate）** 继承 **证书（Certificate）**
- 其余 24 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 成年人（adult） | 在某管辖区达到法定成年年龄的人。 |
| 法定成年年龄（age of majority） | 在某管辖区获得成年人权利与责任的年龄。 |
| 出生证明（birth certificate） | 证明出生情况的原始文件，或该出生登记的认证副本或表示。 |
| 出生证明标识方案（birth certificate identification scheme） | 为出生证明分配标识符的体系。 |
| 出生证明标识符（birth certificate identifier） | 与记录儿童出生的生命统计记录关联的标识符。 |
| 联系人（contact） | 作为指定联络点的参与方所扮演的角色，通常在某个系统或过程中。 |
| 联系人记录（contact record） | 关于处于特定通信或联络角色的参与方的记录。 |
| 出生日期（date of birth） | 个人出生的显式日期（年、月、日）。 |
| 死亡日期（date of death） | 个人死亡的显式日期（年、月、日）。 |
| 死亡证明（death certificate） | 证明死亡情况（如死亡方式与时间）的原始文件，或该死亡登记的认证副本或表示。 |
| 死亡证明标识方案（death certificate identification scheme） | 为死亡证明分配标识符的体系。 |
| 死亡证明标识符（death certificate identifier） | 与记录个人死亡的生命统计记录关联的标识符。 |
| 驾驶证（driver's license） | 声明某人可在公共道路上驾驶机动车辆（如摩托车、汽车、卡车或公共汽车）的官方文件。 |
| 驾驶证标识方案（driver's license identification scheme） | 为驾驶证、操作证或非驾驶身份证件分配标识符的体系。 |
| 驾驶证标识符（driver's license identifier） | 与机动车驾驶执照或非驾驶身份卡关联的标识符。 |
| 解除监护的未成年人（emancipated minor） | 获准在不受父母控制的情况下以自己名义或为自己账户经营业务或从事其他职业的未成年人。 |
| 身份证件（identity document） | 可用于核验个人身份各个方面的任何法律文件。 |
| 无行为能力成年人（incapacitated adult） | 在法律上被认定为不具有法律行为能力的成年人，通常因某种固有的身心障碍所致。 |
| 法定年龄（legal age） | 在某管辖区获得做法律此前禁止之事的能力的年龄。 |
| 法定工作年龄（legal working age） | 在某管辖区获得合法工作能力的年龄。 |
| 达到法定工作年龄的人（legal working age person） | 年龄大于其工作所在管辖区规定的最低法定工作年龄的人。 |
| 具有法律行为能力的成年人（legally capable adult） | 在某管辖区达到法定成年年龄、并获准以自己名义经营业务或从事其他职业的人。 |
| 未成年人（minor） | 低于某一年龄（通常是给定管辖区的法定成年年龄）的人，该年龄在法律上划分童年与成年。 |
| 国家身份号码（national identification number） | 出现在由国家或管辖区签发的身份证件上的号码或文字。 |
| 国家身份号码方案（national identification number scheme） | 为国家身份号码分配标识符的体系。 |
| 护照（passport） | 由国家政府签发的正式身份证件，为国际旅行目的证明持有人的身份与国籍。 |
| 护照号码（passport number） | 与护照关联的国家身份号码。 |
| 护照号码标识方案（passport number identification scheme） | 为护照分配标识符的体系。 |
| 个人（person） | 具有自我意识的个体人类。 |
| 人名（person name） | 某人在某情境中为人所知的指称。 |
| 出生地（place of birth） | 个人出生的物理位置，包括国家、地区和市政区。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 出生证明标识方案（birth certificate identification scheme）

定义：为出生证明分配标识符的体系。

- 父类：**标识方案（IdentificationScheme）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义（defines）** | — | — |

公理：

- **定义（defines）**至少有一个取值，类型是**出生证明标识符（birth certificate identifier）**。

### 2.2 出生证明标识符（birth certificate identifier）

定义：与记录儿童出生的生命统计记录关联的标识符。

- 父类：**标识符（Identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义于（isDefinedIn）** | — | — |
| **标识（identifies）** | — | — |

公理：

- **定义于（isDefinedIn）**恰好有 1 个**出生证明标识方案（birth certificate identification scheme）**。
- **标识（identifies）**恰好有 1 个**出生证明（birth certificate）**。

### 2.3 联系人（contact）

定义：作为指定联络点的参与方所扮演的角色，通常在某个系统或过程中。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的联络点（is point of contact for）** | 是该参与方作为联络点所服务的实体或目的。 | 逆属性：具有联络点（has point of contact）；子属性：具有角色（has role） |
| **由……表示（isSignifiedBy）** | — | — |
| **由……标识（isIdentifiedBy）** | — | — |
| **由…扮演（is played by）** | — | — |

公理：

- **由……标识（isIdentifiedBy）**至少有一个取值，类型是**参与方角色标识符（PartyRoleIdentifier）**。
- **由……表示（isSignifiedBy）**至少有一个取值，类型是**联系人记录（contact record）**。
- **由…扮演（is played by）**至少有一个取值，类型是**参与方（party）**。

### 2.4 联系人记录（contact record）

定义：关于处于特定通信或联络角色的参与方的记录。

- 父类：**记录（Record）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |
| **指代（denotes）** | — | — |

公理：

- **包含（comprises）**恰好有 1 个**参与方角色标识符（PartyRoleIdentifier）**。
- **指代（denotes）**恰好有 1 个**联系人（contact）**。

### 2.5 出生日期（date of birth）

定义：个人出生的显式日期（年、月、日）。

- 父类：**显式日期（ExplicitDate）**

### 2.6 死亡日期（date of death）

定义：个人死亡的显式日期（年、月、日）。

- 父类：**显式日期（ExplicitDate）**

### 2.7 死亡证明标识方案（death certificate identification scheme）

定义：为死亡证明分配标识符的体系。

- 父类：**标识方案（IdentificationScheme）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义（defines）** | — | — |

公理：

- **定义（defines）**至少有一个取值，类型是**死亡证明标识符（death certificate identifier）**。

### 2.8 死亡证明标识符（death certificate identifier）

定义：与记录个人死亡的生命统计记录关联的标识符。

- 父类：**标识符（Identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义于（isDefinedIn）** | — | — |
| **标识（identifies）** | — | — |

公理：

- **定义于（isDefinedIn）**恰好有 1 个**死亡证明标识方案（death certificate identification scheme）**。
- **标识（identifies）**恰好有 1 个**死亡证明（death certificate）**。

### 2.9 驾驶证标识方案（driver's license identification scheme）

定义：为驾驶证、操作证或非驾驶身份证件分配标识符的体系。

- 父类：**标识方案（IdentificationScheme）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义（defines）** | — | — |

公理：

- **定义（defines）**至少有一个取值，类型是**驾驶证标识符（driver's license identifier）**。

### 2.10 驾驶证标识符（driver's license identifier）

定义：与机动车驾驶执照或非驾驶身份卡关联的标识符。

- 父类：**标识符（Identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义于（isDefinedIn）** | — | — |
| **标识（identifies）** | — | — |

公理：

- **定义于（isDefinedIn）**恰好有 1 个**驾驶证标识方案（driver's license identification scheme）**。
- **标识（identifies）**恰好有 1 个**驾驶证（driver's license）**。

### 2.11 身份证件（identity document）

定义：可用于核验个人身份各个方面的任何法律文件。

- 父类：**法律文件（LegalDocument）**
- 直接子类：**出生证明（birth certificate）**、**死亡证明（death certificate）**、**驾驶证（driver's license）**、**护照（passport）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有到期日（hasExpirationDate）** | — | — |
| **具有签发日期（hasDateOfIssuance）** | — | — |
| **标识（identifies）** | — | — |
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **具有到期日（hasExpirationDate）**恰好有 1 个**日期（Date）**。
- **具有签发日期（hasDateOfIssuance）**恰好有 1 个**日期（Date）**。
- **标识（identifies）**至少有一个取值，类型是**个人（person）**。
- **由……标识（isIdentifiedBy）**恰好有 1 个**标识符（Identifier）**。

#### 2.11.1 出生证明（birth certificate）

定义：证明出生情况的原始文件，或该出生登记的认证副本或表示。

- 父类：**身份证件（identity document）**、**证书（Certificate）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **由……标识（isIdentifiedBy）**恰好有 1 个**出生证明标识符（birth certificate identifier）**。

#### 2.11.2 死亡证明（death certificate）

定义：证明死亡情况（如死亡方式与时间）的原始文件，或该死亡登记的认证副本或表示。

- 父类：**身份证件（identity document）**、**证书（Certificate）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **由……标识（isIdentifiedBy）**恰好有 1 个**死亡证明标识符（death certificate identifier）**。

#### 2.11.3 驾驶证（driver's license）

定义：声明某人可在公共道路上驾驶机动车辆（如摩托车、汽车、卡车或公共汽车）的官方文件。

- 父类：**身份证件（identity document）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **由……标识（isIdentifiedBy）**恰好有 1 个**驾驶证标识符（driver's license identifier）**。

#### 2.11.4 护照（passport）

定义：由国家政府签发的正式身份证件，为国际旅行目的证明持有人的身份与国籍。

- 父类：**身份证件（identity document）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |

公理：

- **包含（comprises）**恰好有 1 个**护照号码（passport number）**。

### 2.12 法定年龄（legal age）

定义：在某管辖区获得做法律此前禁止之事的能力的年龄。

- 父类：**存续时间（Age）**
- 直接子类：**法定成年年龄（age of majority）**、**法定工作年龄（legal working age）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于情境（isApplicableIn）** | — | — |

公理：

- **适用于情境（isApplicableIn）**至少有一个取值，类型是**管辖权（Jurisdiction）**。

#### 2.12.1 法定成年年龄（age of majority）

定义：在某管辖区获得成年人权利与责任的年龄。

- 父类：**法定年龄（legal age）**

#### 2.12.2 法定工作年龄（legal working age）

定义：在某管辖区获得合法工作能力的年龄。

- 父类：**法定年龄（legal age）**

### 2.13 国家身份号码（national identification number）

定义：出现在由国家或管辖区签发的身份证件上的号码或文字。

- 父类：**标识符（Identifier）**
- 直接子类：**护照号码（passport number）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义于（isDefinedIn）** | — | — |
| **标识（identifies）** | — | — |

公理：

- **定义于（isDefinedIn）**恰好有 1 个**国家身份号码方案（national identification number scheme）**。
- **标识（identifies）**恰好有 1 个**个人（person）**。

#### 2.13.1 护照号码（passport number）

定义：与护照关联的国家身份号码。

- 父类：**国家身份号码（national identification number）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定义于（isDefinedIn）** | — | — |

公理：

- **定义于（isDefinedIn）**恰好有 1 个**护照号码标识方案（passport number identification scheme）**。

### 2.14 国家身份号码方案（national identification number scheme）

定义：为国家身份号码分配标识符的体系。

- 父类：**标识方案（IdentificationScheme）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**国家身份号码（national identification number）**。

### 2.15 护照号码标识方案（passport number identification scheme）

定义：为护照分配标识符的体系。

- 父类：**标识方案（IdentificationScheme）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**护照号码（passport number）**。

### 2.16 个人（person）

定义：具有自我意识的个体人类。

- 父类：**参与方（party）**
- 直接子类：**成年人（adult）**、**达到法定工作年龄的人（legal working age person）**、**未成年人（minor）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有国籍（has citizenship）** | 将个人关联到其国籍国。 | 值域：国家；子属性：由……分类 |
| **具有出生日期（has date of birth）** | 标识个人出生的日期。 | 值域：出生日期（date of birth）；子属性：具有显式日期 |
| **具有死亡日期（has date of death）** | 标识个人死亡的日期。 | 值域：死亡日期（date of death）；子属性：具有显式日期 |
| **具有性别（has gender）** | 将特定性别值与个人关联。 | 值域：xsd:string |
| **具有出生地（has place of birth）** | 标识个人出生的位置。 | 值域：出生地（place of birth）；子属性：以……为特征 |
| **具有主要居所（has primary residence）** | 标识个人一年中大部分时间居住的住所。 | 值域：常规街道地址；子属性：具有居所（has residence） |
| **具有居所（has residence）** | 标识个人居住的住所。 | 值域：常规街道地址；子属性：具有地址 |
| **具有存续时间（hasAge）** | — | — |
| **具有名称（hasName）** | — | — |

公理：

- **具有出生地（has place of birth）**恰好有 1 个**出生地（place of birth）**。
- **具有出生日期（has date of birth）**恰好有 1 个**出生日期（date of birth）**。
- **具有名称（hasName）**可以有 0 个或多个**人名（person name）**。
- **具有国籍（has citizenship）**可以有 0 个或多个**国家（Country）**。
- **具有存续时间（hasAge）**可以有 0 个或多个**存续时间（Age）**。
- **具有居所（has residence）**可以有 0 个或多个**常规街道地址（ConventionalStreetAddress）**。
- **具有性别（has gender）**存在取值约束。
- **具有死亡日期（has date of death）**可以有 0 个或多个**死亡日期（date of death）**。

#### 2.16.1 成年人（adult）

定义：在某管辖区达到法定成年年龄的人。

- 父类：**个人（person）**
- 直接子类：**无行为能力成年人（incapacitated adult）**、**具有法律行为能力的成年人（legally capable adult）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有法定成年年龄（has age of majority）** | 将某人关联到在某管辖区获得从事特定交易能力或被法律视为成年人所需的年龄。 | 值域：法定成年年龄（age of majority）；子属性：具有存续时间 |

公理：

- **具有法定成年年龄（has age of majority）**可以有 0 个或多个**法定成年年龄（age of majority）**。

##### 2.16.1.1 无行为能力成年人（incapacitated adult）

定义：在法律上被认定为不具有法律行为能力的成年人，通常因某种固有的身心障碍所致。

- 父类：**成年人（adult）**

公理：

- 与**具有法律行为能力的成年人（legally capable adult）**互斥：同一个体不能同时属于两者。

##### 2.16.1.2 具有法律行为能力的成年人（legally capable adult）

定义：在某管辖区达到法定成年年龄、并获准以自己名义经营业务或从事其他职业的人。

- 父类：**成年人（adult）**

#### 2.16.2 达到法定工作年龄的人（legal working age person）

定义：年龄大于其工作所在管辖区规定的最低法定工作年龄的人。

- 父类：**个人（person）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有最低法定工作年龄（has minimum legal working age）** | 将某人关联到其居住管辖区的最低法定工作年龄。 | 值域：法定工作年龄（legal working age）；子属性：具有存续时间 |

公理：

- **具有最低法定工作年龄（has minimum legal working age）**可以有 0 个或多个**法定工作年龄（legal working age）**。

#### 2.16.3 未成年人（minor）

定义：低于某一年龄（通常是给定管辖区的法定成年年龄）的人，该年龄在法律上划分童年与成年。

- 父类：**个人（person）**
- 直接子类：**解除监护的未成年人（emancipated minor）**

##### 2.16.3.1 解除监护的未成年人（emancipated minor）

定义：获准在不受父母控制的情况下以自己名义或为自己账户经营业务或从事其他职业的未成年人。

- 父类：**未成年人（minor）**

### 2.17 人名（person name）

定义：某人在某情境中为人所知的指称。

- 父类：**情境化名称（ContextualName）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有完整法定姓名（has full legal name）** | 标识个人的完整姓名，通常用于正式场合（包括法律或合同性质的场合）。 | 子属性：具有人名（has person name） |
| **具有姓名前缀（has name prefix）** | 标识位于个人姓名之前、提供其附加信息（如头衔、敬称或军衔）的字符或字符序列。 | 子属性：具有文本值 |
| **具有姓名后缀（has name suffix）** | 标识位于个人姓名之后、提供其附加信息（如职位、学位、资格、官职或荣誉）的字符或字符序列。 | 子属性：具有文本值 |
| **具有姓（has surname）** | 标识家庭成员共有的、区别于各成员名字的姓。 | 子属性：具有人名（has person name） |
| **是……的名称（isNameOf）** | — | — |

公理：

- **具有姓名前缀（has name prefix）**存在取值约束。
- **具有姓名后缀（has name suffix）**存在取值约束。
- **具有姓（has surname）**存在取值约束。
- **具有完整法定姓名（has full legal name）**存在取值约束。
- **是……的名称（isNameOf）**可以有 0 个或多个**个人（person）**。

### 2.18 出生地（place of birth）

定义：个人出生的物理位置，包括国家、地区和市政区。

- 父类：**物理位置（PhysicalLocation）**

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有联络点（has point of contact）** | 标识被指定为联络点的参与方。 | 值域：联系人（contact）；子属性：具有角色（has role） |

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有姓氏（has family name）** | 标识家庭成员共有的、区别于各成员名字的姓。 |
| **具有名字（has first name）** | 标识个人的名，即出生时为其选取或其后更改的名字。 |
| **具有名（has given name）** | 标识个人的名，即出生时为其选取或其后更改的名字。 |
| **具有姓（has last name）** | 标识家庭成员共有的、区别于各成员名字的姓。 |
| **具有婚前姓（has maiden name）** | 标识因婚姻而改姓之前的家族姓氏。 |
| **具有中间名或首字母（has middle name or initial）** | 位于个人名与姓之间的一个或多个附加名字或首字母。 |
| **具有人名（has person name）** | 将名称关联到个人。 |

## 4. 依赖（owl:imports，20 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/Arrangements/IdentifiersAndIndices.rdf` | 标识符与索引本体（Identifiers and Indices Ontology） | 定义标识符（identifier）、标识方案与索引（index）的基本结构，是 ISIN、LEI、CUSIP 等编码体系建模的基础。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/Commons/TextDatatype/` | OMG 通用文本数据类型（OMG Commons Text Datatype） | Commons 库中的文本数据类型定义，提供带语言标记的文本等基础数据类型。 |

## 5. 文件

- 官方 RDF/XML：`People.rdf`
- 中文 Turtle：`People.ttl`
- 结构图：`People-structure.png` / `People-structure.svg`