OWASP Top Ten Web Application Security Risks | OWASP Foundation

# OWASP 十大 Web 应用安全风险（OWASP Top Ten Web Application Security Risks）

目前发布的最新版本是 OWASP Top Ten 2025。

以前的版本可在 OWASP Top Ten 2021 和 OWASP Top 10 2017（PDF）获取。更早的版本可在 GitHub 仓库（Github repo）中找到。

OWASP（开放式 Web 应用安全项目）Top 10 是面向开发者和 Web 应用安全的一份标准意识文档（awareness document）。它代表了关于 Web 应用所面临的最关键安全风险的广泛共识。

它被全球开发者公认为迈向更安全编码（more secure coding）的第一步。

公司应当采纳本文档，并启动相应流程，确保其 Web 应用尽可能降低这些风险。采用 OWASP Top 10 或许是改变贵组织软件开发文化、使其产出更安全代码的最有效的第一步。

## 2021 项目赞助方（2021 Project Sponsors）

OWASP Top 10:2021 由 Secure Code Warrior 赞助。

## 2017 项目赞助方（2017 Project Sponsors）

OWASP Top 10 - 2017 项目由 Autodesk 赞助，并得到 OWASP NoVA Chapter 的支持。

## 2003-2013 项目赞助方（2003-2013 Project Sponsors）

感谢 Aspect Security 赞助了早期版本。

# OWASP Top 10 2025 数据分析计划（Data Analysis Plan）

## 目标（Goals）

收集迄今与已识别应用漏洞（application vulnerabilities）相关的最全面的数据集，以支持 Top 10 的分析以及其他未来的研究。这些数据应来自多种来源：安全厂商与咨询机构、漏洞赏金（bug bounties），以及公司/组织的贡献。数据将被归一化（normalized），以便在「人类辅助工具（Human assisted Tooling）」与「工具辅助人类（Tooling assisted Humans）」之间进行水平比较。

## 分析基础设施（Analysis Infrastructure）

计划利用 OWASP Azure 云基础设施来收集、分析和存储所贡献的数据。

## 贡献（Contributions）

我们计划同时支持「已知（known）」和「伪匿名（pseudo-anonymous）」两种贡献方式。我们倾向于已知的贡献；这将极大地有助于所提交数据的验证、质量与置信度。如果提交者更希望其数据被匿名存储，甚至走得更远、以匿名方式提交数据，那么该数据将不得不被分类为「未验证（unverified）」而非「已验证（verified）」。

### 已验证数据贡献（Verified Data Contribution）

场景 1：提交者是已知的，并同意被标识为贡献方。场景 2：提交者是已知的，但不希望被公开标识。场景 3：提交者是已知的，但不希望其身份被记录在数据集中。

### 未验证数据贡献（Unverified Data Contribution）

场景 4：提交者是匿名的。（我们是否应该支持？）

在对数据进行分析时，若未验证数据是被分析数据集的一部分，将谨慎地加以区分。

## 贡献流程（Contribution Process）

数据可通过以下几种方式贡献：

将包含数据集的 CSV/Excel 文件通过电子邮件发送至 [email protected]

将 CSV/Excel 文件上传至 https://bit.ly/OWASPTop10Data

模板示例可在 GitHub 中找到：https://github.com/OWASP/Top10/tree/master/2025/Data

## 贡献周期（Contribution Period）

我们计划接收新 Top 10 的数据贡献，直至 2025 年 7 月 31 日，数据时间范围为 2021 年至 2024 年。

## 数据结构（Data Structure）

以下数据元素为必填或选填。提供的信息越多，我们的分析就越准确。最低限度，我们需要：时间段、数据集中被测应用的总数，以及 CWE 列表及包含该 CWE 的应用数量。如果可能的话，请提供额外的元数据，因为这将极大地帮助我们更深入地了解当前测试与漏洞（vulnerabilities）的状况。

### 元数据（Metadata）

贡献者名称（组织或匿名）

贡献者联系邮箱

时间段（2024、2023、2022、2021）

被测应用数量

测试类型（TaH、HaT、Tools）

主要语言（代码）

地理区域（全球、北美、欧盟、亚洲、其他）

主要行业（多种、金融、工业、软件、??）

数据是否包含复测（retests）或同一应用的多次测试（T/F）

### CWE 数据（CWE Data）

一份 CWE 列表，以及包含该 CWE 的应用数量

如果可能，请在数据中提供核心 CWE，而非 CWE 类别。这将有助于分析；作为本分析一部分所进行的任何归一化/聚合（normalization/aggregation）都将被充分记录。

#### 说明（Note）：

如果贡献者拥有两种类型的数据集，一种来自 HaT、一种来自 TaH 来源，那么建议将它们作为两个独立的数据集提交。HaT = 人类辅助工具（Human assisted Tools，更高容量/频率，主要来自工具）TaH = 工具辅助人类（Tool assisted Human，较低容量/频率，主要来自人工测试）

## 调查（Survey）

与 Top Ten 2021 类似，我们计划开展一项调查，以识别出社区认为重要、但可能尚未在数据中反映出来的最多两个 Top 10 类别。我们计划在 2025 年初开展该调查，并将以与上次类似的方式使用 Google 表单（Google forms）。调查中的 CWE 将来自当前的热门发现（trending findings）、数据中处于 Top Ten 之外的 CWE，以及其他潜在来源。

## 流程（Process）

从高层来看，我们计划执行一定程度的归一化；然而，我们会保留所贡献原始数据的一个版本以供未来分析。我们将分析数据集的 CWE 分布，并可能对某些 CWE 进行重新分类，将其合并到更大的桶（buckets）中。我们将仔细记录所采取的所有归一化操作，以便清楚地说明已经完成了什么。

我们计划沿用 2021 年延续下来的模型来计算似然度（likelihood），以确定「发生率（incidence rate）」而非「频率（frequency）」，从而评估给定应用可能包含至少一个某 CWE 实例的可能性。这意味着我们不是在寻找某个应用中的频率率（即发现数量），而是在寻找「含有一个或多个某 CWE 实例的应用数量」。我们可以基于数据集中被测应用的总数、与每个 CWE 被发现的所在应用数量之比来计算发生率。

此外，我们将为排名前 20-30 的 CWE 开发基础 CWSS 评分，并将潜在影响纳入 Top 10 的加权。

同时，我们希望探索从所贡献的数据集中可以挖掘出的其他洞见，看看还能学到什么对安全和开发社区有用的东西。

Watch Star

OWASP® 基金会（OWASP Foundation）通过其社区主导的开源软件项目、遍布全球的数百个分会（chapters）、数以万计的成员，以及主办本地和全球会议，致力于改善软件的安全性。

### 项目信息（Project Information）

• OWASP Top 10:2025

• OWASP Top 10 的制作（Making of OWASP Top 10）

Flagship Project

Documentation

Builder

Defender

• 上一版本（2021）

• 上一版本（2017）

### 下载或社交链接（Downloads or Social Links）

• OWASP Top 10 2017

• 其他语言 → 标签页「Translation Efforts」

### 社交（Social）

Twitter

### 代码仓库（Code Repository）

GitHub 仓库（Github repo）

### 负责人（Leaders）

Andrew van der Stock

Brian Glas

Neil Smithline

Tanya Janca

Torsten Gigler

### 即将举行的 OWASP 全球活动（Upcoming OWASP Global Events）
