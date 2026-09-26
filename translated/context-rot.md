# 上下文腐化：输入 Token 增加如何影响 LLM 性能

Chroma

Claude Sonnet 4、GPT-4.1、Qwen3-32B 与 Gemini 2.5 Flash 在「重复词」任务上的表现

LLM 的最新发展呈现出向更长上下文窗口演进的趋势，最新模型的输入 token 数量已达到百万级。由于这些模型在「大海捞针」（Needle in a Haystack，简称 NIAH）[1] 这类被广泛采用的基准测试上取得了近乎满分的成绩，人们常常据此假设它们在各类长上下文任务中的性能是均匀一致的。

然而，NIAH 本质上是一个简单的检索任务：把一个已知的句子（即「针」）放入一段由无关文本组成的长文档（即「草垛」）中，然后要求模型把它找出来。这个基准虽然具有可扩展性，但它通常只评估直接的词汇匹配，未必能代表灵活的、以语义为导向的任务。

NIAH（大海捞针）示例设置

我们对标准的 NIAH 任务做了扩展，以探究模型在以往未充分探索的场景下的行为。我们考察了语义匹配（而非直接词汇匹配）的针所带来的影响，以及对草垛内容引入变化所产生的影响。

此外，我们还加入了基于 LongMemEval [2] 的对话式问答评估，以及一个让模型复现一系列重复单词的合成任务。每个任务都刻意保持简单，并经过严格控制，以单独隔离上下文长度的影响。

我们证明，即便在这些极简条件下，模型性能也会随着输入长度的增加而下降，且下降方式往往出人意料、并非均匀。真实世界的应用通常复杂得多，这意味着输入长度的影响在实践中可能更加显著。

我们深入的技术报告如下。如果您觉得我们的工作有帮助，请考虑引用我们：

plaintext

@techreport{hong2025context, title = {Context Rot: How Increasing Input Tokens Impacts LLM Performance}, author = {Hong, Kelly and Troynikov, Anton and Huber, Jeff}, year = {2025}, month = {July}, institution = {Chroma}, url = {https://trychroma.com/research/context-rot}, }

有兴趣从事改进 AI 应用检索方面的工作吗？Chroma 正在招聘

# 引言

现代 LLM 拥有数百万 token 的输入上下文长度已十分常见。Gemini 1.5 Pro [3] 于 2024 年初率先推出 1M 上下文窗口，随后是近期 GPT-4.1 的 1M 上下文窗口 [4]，以及 Llama 4 的 10M [5]。长上下文的用途颇具吸引力：更长的上下文意味着 LLM 每次调用能够处理更多信息，并生成更有据可依的输出。

针对这些模型的长上下文评估，往往在各类输入长度下都展现出稳定的性能。然而，这些评估范围狭窄，并不能代表长上下文在实际中的使用方式。最常用的测试——大海捞针（NIAH）——是一个简单的词汇检索任务，常被用来推断一个模型可靠处理长上下文的能力。而真实应用，比如智能体任务或摘要，则要求对更广泛、往往更模糊的信息进行多得多的处理与推理。

设计贴近真实的长上下文基准十分困难。任务往往随输入长度增加而变得更复杂，这使得我们难以区分性能下降究竟是源于更长的输入，还是源于本质上更难的问题。为解决这一问题，我们的实验在保持任务复杂度不变的同时，仅改变输入长度——这使我们能够直接测量输入长度单独的影响。

## 贡献

我们呈现以下内容：

- 对 18 个 LLM（包括领先的闭源与开放权重模型）的评估，揭示了性能随输入长度增加而表现出的非均匀性。
- 关于模型在处理干扰项与不同问答相似度时所呈现的特定行为模式的记录。
- 用于复现我们结果的完整代码库。

# 相关工作

用于评估模型长上下文能力的最广泛使用的基准之一，就是大海捞针（NIAH）。它作为可扩展测试固然有用，但它衡量的是一种很窄的能力：词汇检索。模型在 NIAH 上通常表现良好，这导致了一种观念，认为长上下文问题在很大程度上已被解决。

然而，NIAH 低估了大多数长上下文任务在实际中的要求。NIAH 的变体，比如包含非词汇匹配的针—问题对的 NoLiMa [6]，就揭示了显著的性能下降。其他在难度上看似相似的任务，例如测试模型能否识别某段文本不存在的 AbsenceBench [7]，也表现出随输入长度增长而性能退化的现象。

此外，长上下文任务往往涉及在干扰项之间进行消歧。一个例子是多轮共指消解（MRCR）[8][9]，它要求在多轮对话中、在若干相似的用户请求里检索出某一特定用户请求的第 i 次出现。然而，关于干扰项在长上下文场景下影响的研究仍然缺失。

长上下文任务中的一个重要因素是输入长度如何缩放。Latent List [8] 是一个任务，要求模型在不同输入长度下执行固定数量的 Python 列表操作。它测试了多种填充无关上下文的方式，揭示了对模型性能的非均匀影响 [1]。例如，添加局部相互抵消的列表操作，比添加 print 语句对模型性能的损害更为显著。这凸显了「无关内容的类型」是如何重要的，因为某些内容可能随输入长度引入递增的复杂度。

类似地，Graphwalks [10] 是一个图遍历任务：给模型一个有向图（由十六进制哈希构成），然后要求它从一个随机节点开始执行广度优先搜索。增加输入长度意味着增大需要遍历的图，从而增加了任务难度。我们很难把递增的任务复杂度与输入长度区分开来，因此也就难以单独隔离输入长度对性能的影响。这指向了将输入长度作为关注变量加以隔离的重要性，而这对于理解 LLM 在长输入下的真实行为至关重要。

# 大海捞针扩展

经典的大海捞针任务，是把一个随机事实（「针」）放在长上下文窗口（「草垛」）的中间，然后就这个事实向模型提问。

该任务的原始实现使用词汇匹配的针—问题对。然而，实际中的长上下文使用往往需要对模糊任务进行语义理解。

带词汇匹配的 NIAH（大海捞针）示例设置

NoLiMa 已经证明，非词汇匹配会随着上下文长度的增加而成为模型的挑战。这个任务使用的针—问题对要求模型推断潜在的关联，例如：

问题：哪个角色去过赫尔辛基？

针：实际上，Yuki 住在 Kiasma 博物馆旁边。

NoLiMa 的示例针—问题对

要回答这个问题，模型首先得知道 Kiasma 博物馆位于赫尔辛基，然后才能建立这一潜在关联。

为了回答这个问题，模型首先得知道 Kiasma 博物馆位于赫尔辛基，然后才能建立这一潜在关联。

在我们的 NIAH 扩展中，我们考察了针与问题之间的关系，以及草垛内容的变化，来探究模型如何受到干扰项和相似度的影响。

我们实验的维度如下：

- 针—问题相似度：针与问题之间的语义相似度。
- 干扰项的影响：草垛中与针相竞争的、语义相关的干扰项。
- 针—草垛相似度：针与草垛其余部分之间的语义相似度。
- 草垛结构：草垛的文本结构——原始顺序与打乱顺序。

NIAH 扩展实验的四个维度

下面我们详细介绍每个维度。

## 针—问题相似度

第一个维度是针与问题之间的相似度。我们首先构建了一个问题池，然后为每个问题生成 8 根不同的针——它们都能正确地回答该问题，但各自使用了不同的措辞。

然后，我们通过从五个嵌入模型计算出的成对相似度，对这些针进行排序，并选出相似度最低的针。

不同针—问题对的相似度分布。不同嵌入模型之间的相似度范围在 PG（Paul Graham 文章）为 0.445 到 0.775 之间，在 arXiv 为 0.521 到 0.829 之间。五种模型之间相似度的标准差始终小于 0.1。

我们把相似度最低的针称为「不相似针」，把相似度最高的针称为「相似针」，并评估模型在这两种情形下的性能。

## 干扰项的影响

第二个维度是草垛中干扰项的影响。我们用一堆语义相关的干扰项（即「干扰针」）填充草垛，这些干扰项表面上与真正的针相似，但并不能正确回答问题。

我们对干扰项进行了聚类，并把那些有超过 0.9 的概率属于「写作」或「检索」聚类的针（这些聚类是在我们用以生成干扰针的内容上训练得到的）视为「主题混合」的干扰项，并评估模型在主题混合干扰项下的性能。

## 针—草垛相似度

第三个维度是针与草垛其余部分之间的相似度。我们构建了两类草垛：一类由与针来自相同分布的内容构成（即针与草垛「同域」），另一类由来自不同分布的内容构成（即针与草垛「异域」）。

针与草垛之间的相似度。对于 PG 草垛，PG 针的平均相似度为 0.529（方差 0.101），arXiv 针为 0.368（方差 0.111）。对于 arXiv 草垛，arXiv 针的平均相似度为 0.654（方差 0.0858），PG 针为 0.394（方差 0.105）。

我们评估模型在针与草垛同域和异域时的性能。

## 草垛结构

第四个维度是草垛的文本结构。我们构建了两个版本的草垛：一个是「原始」顺序（即从源文档中抽取的文本保持原有顺序），另一个是「打乱」顺序（即抽取的文本块被打乱）。

原始草垛与打乱草垛

我们评估模型在原始草垛与打乱草垛下的性能。

## 细节

我们的 NIAH 扩展使用以下配置：

- 嵌入模型：text-embedding-3-small、text-embedding-3-large、jina-embeddings-v3、voyage-3-large 和 all-MiniLM-L6-v2。
- 聚类：HDBSCAN，参数为 min_cluster_size=10、min_samples=15。
- 降维：UMAP，参数为 n_neighbors=30、min_dist=0.05、n_components=50、random_state=42。

# 针—问题相似度

模型对语义上不相似的针—问题对的性能，随上下文长度的增加而下降。

针—问题相似度实验的结果

我们首先考察模型在针—问题对语义不相似时的表现。对于 PG 和 arXiv 这两个数据集，模型在针与问题不相似时的性能均低于相似针的情形，且差距随着上下文长度的增加而扩大。

我们的观察表明，模型在处理不相似针时的性能下降，往往是因为模型没有识别出正确答案，而是选择了与问题在词汇上更相近的干扰项。

一个值得注意的模式是，某些模型在面对不相似针时，会退回到简单的词汇匹配，而不是进行语义理解——这与 NIAH 的原始设计形成了对比，后者正是用词汇匹配来让检索变得简单。

## 结果

我们在多个模型上观察到一致的趋势：不相似针的性能低于相似针。这种差距并非恒定不变，而是随着上下文长度的增加而扩大，这表明输入长度会加剧语义歧义所带来的挑战。

# 干扰项的影响

此前已有研究用较旧的模型确立了这样一个事实：干扰项会降低模型性能，且其影响并不均匀。较新的模型据称能够可靠地处理任何干扰项，但随着输入长度的增加，这一点是否依然成立？

我们的实验表明，随着输入长度的增长，干扰项的影响及其非均匀性会进一步放大——即便是最新的一流模型也不例外。我们还观察到，不同模型家族在处理歧义时表现出截然不同的行为。

## 实验

我们从每个草垛主题（PG 文章和 arXiv 论文）中选取一根具有较高针—问题相似度的针（在八根针中相似度第二高），并手动编写四个干扰项：

问题：「我从大学同学那里得到的最好的写作建议是什么？」

针：「我想我从大学同学那里得到的最好的写作建议是每周都写作。」

干扰项：

「我从大学教授那里得到的最好的写作建议是每天写作。」

「我从大学同学那里得到的最糟糕的写作建议是把每篇文章写成五种不同的风格。」

「我从同学那里得到的最好的写作建议是把每篇文章写成三种不同的风格，那还是在高中的时候。」

「我以为我从大学同学那里得到的最好的写作建议是把每篇文章写成四种不同的风格，但现在不是了。」

Paul Graham 文章主题下高针—问题相似度针的干扰项

我们并没有用干扰项测试全部八根针，而是选取一根具有高针—问题相似度的针，来构造一个这根针应当相对容易识别的条件。从之前的结果可以看出，由于针—问题相似度较高，模型在各种输入长度下通常都能在这根针上表现良好，这让我们能够更好地把干扰项的影响单独隔离出来加以衡量。

我们运行三种测试条件：

无干扰项（基线）：仅针

单一干扰项：针 + 一个干扰项（随机放置）

多个干扰项：针 + 全部四个干扰项，随机散布在整个草垛中

干扰项的影响——三种条件

## 结果

即便是单个干扰项，也会相对于基线（仅针）降低性能，而加入四个干扰项则会进一步加剧这种退化。

干扰项的影响：按干扰项数量划分的性能——arXiv 草垛 / PG 文章针

我们还看到，干扰项的影响并不均匀。例如，在 arXiv 草垛与 PG 文章针的组合中，我们可以看到干扰项 3（红色）相对于其他干扰项导致了更大的性能下降。

干扰项的影响：按单个干扰项划分的性能——arXiv 草垛 / PG 文章针

为了进一步探究这种非均匀影响，我们分析了各模型在四干扰项条件下的失败尝试。对于 arXiv 草垛与 PG 文章针的组合，我们看到干扰项 2 和 3 在各模型的幻觉式回答中出现得最为频繁。

干扰项的影响：失败分析——arXiv 草垛 / PG 文章针

这些失败也揭示了不同模型在处理歧义时的差异。Claude 模型始终表现出最低的幻觉率。具体而言，Claude Sonnet 4 和 Opus 4 尤其保守，在不确定时倾向于放弃作答，明确表示找不到答案。相比之下，GPT 模型表现出最高的幻觉率，在存在干扰项时往往生成自信但错误的回答。

## 实验

为了评估草垛结构的影响，我们创建了两个变体：

原始（Original）：保留每段摘录中自然的思想流。

打乱（Shuffled）：句子在整个草垛中被随机重排，以维持相同的整体主题，但不再具有逻辑连贯性。

草垛结构：示例实验设置

## 结果

在全部 18 个模型以及针—草垛配置中，我们都观察到一个一致的模式：模型在打乱的草垛上的表现优于在具有逻辑结构的草垛上的表现。

草垛结构：18 个模型在原始与打乱草垛上的平均表现这些结果可能对模型的内部处理有所启示：输入的结构模式可能影响注意力机制的运用方式，尤其是随着输入长度的增加。

尽管这超出了本报告的范围，但它指出了可解释性研究的一个潜在方向，即注意力如何受到输入结构的影响。理解这些随输入长度增加而出现的结构性影响，或许有助于解释这些长上下文失效模式。

# LongMemEval

为了在更贴近现实的场景下评估这些模型，我们使用了 LongMemEval，一个面向对话式问答的长上下文基准。

对聊天助手而言，使用长输入是维持后续对话相关历史的常见做法。要为聊天助手加入"记忆"，一种朴素的做法是把完整的聊天历史放入后续对话的提示词中。这就要求模型在一次调用中通常需要完成两项任务：找到对话历史中相关的部分（检索），然后以对当前查询有用的方式综合它们（推理）。

在理想情况下，模型只会得到相关的部分，从而可以专注于推理。加入不相关的上下文会增加"识别哪些是相关的"这一额外步骤，迫使模型同时执行两项任务。

我们通过两种条件系统地测试了在输入长度增加的情况下加入这一额外步骤的影响：

聚焦输入（Focused input）：只包含相关的部分，因此模型只需进行简单推理。

完整输入（Full input）：使用完整的 113k Token 的 LongMemEval 输入，其中包含不相关的上下文。在这种情况下，模型除了推理之外，还必须跨长上下文进行检索。

我们验证了这些模型在聚焦输入上具有很高的成功率，随后观察到它们在完整输入上的性能持续下降。这一性能下降表明，加入不相关的上下文——进而增加检索这一额外步骤——会显著影响模型维持可靠性能的能力。

## 实验

给定用户与助手之间的聊天历史，模型的任务是回答与聊天历史中某一部分相关的问题。

LongMemEval - 按问题类型划分的示例 [[2](#longmemeval-source)]我们使用 LongMemEval_s，并筛选出属于知识更新、时间推理和多会话这三类的任务。随后我们人工清理该数据集，因为有些问题过于模糊和/或无法回答，共过滤掉 38 条提示词，最终得到 306 条提示词。这些提示词平均约为 113k Token。

这些长提示词大多由与问题无关的内容组成，有时还包含看似与问题相关的干扰项。我们将模型在这些长提示词上的表现与一个聚焦版本进行比较——后者只包含回答问题所需的相关部分。

聚焦提示词平均约为 300 Token，它们源自原始标注的数据集并经过人工调整。

模型输出由一个经过对齐的 LLM 裁判来评判（GPT-4.1，与人类判断的对齐度超过 99%）。

## 结果

在所有模型中，我们看到聚焦提示词上的表现显著高于完整提示词。

LongMemEval 结果 - Claude 家族Claude 模型在聚焦提示词与完整提示词之间表现出最显著的性能差距。这一差异很大程度上源于在歧义情况下出现的弃答（abstention），从而导致模型的不确定性，这与该模型家族在 NIAH 中面对干扰项时的行为类似。这一行为在 Claude Opus 4 和 Sonnet 4 中最为明显，它们在歧义下显得尤为保守，导致其在完整提示词上的表现低于较旧的 Claude 模型。

问题：从我参加园艺工作坊那天到种下番茄幼苗那天之间过了多少天？

正确答案：6 天。7 天（算上最后一天）也可接受。

模型输出：我无法确定园艺工作坊和种下番茄幼苗之间相隔的天数，因为聊天历史中没有提供这些事件的具体日期。

LongMemEval - Claude Sonnet 4（非思考模式）在包含日期的完整提示词上聚焦提示词表现更强的这一趋势，在 GPT、Gemini 和 Qwen 模型家族中同样成立。对于支持思考模式的模型，我们观察到启用思考模式后，在聚焦提示词和完整提示词上都有显著提升。然而，即使最新模型具备完整的推理能力，我们仍然看到两种输入长度之间存在性能差距。

LongMemEval 结果 - GPT 家族

LongMemEval 结果 - Gemini 家族

LongMemEval 结果 - Qwen 家族我们还观察到特定问题类型之间的模式。在非思考模式下，模型通常在知识更新上表现最佳，其次是多会话，然后是时间推理——无论聚焦提示词还是完整提示词都是如此。然而，当启用思考模式时，这一排序变为：知识更新、时间推理，然后是多会话。

LongMemEval 按问题类型划分的结果 - Claude Opus 4

# 重复词（Repeated Words）

我们之前的实验探讨了仅输入长度本身如何影响模型性能。但当输出长度随输入一起增长时会发生什么？由于这些模型是自回归的，模型的输出也属于其输入的一部分——每个 Token 都是基于输入以及到该点为止已生成的 Token 条件地生成的。

考虑一个把字符串重复 n 次的基础程序——它每次都产生相同的输出。对于如此简单的任务，我们会期望这些模型同样可靠，并希望把它们当作计算系统来对待。

然而，我们的发现表明，即便是这些直白的任务，随着上下文长度（涵盖输入和输出长度）的增长，模型性能也会变得不再均匀。

## 实验

我们设计了一个受控任务：模型必须复现一串重复的词，其中在特定位置插入了一个唯一的词。提示词明确指示模型要精确复现输入文本。

一个示例提示词如下：

只需复现以下文本，输出完全相同的文本：apple apple apple apple apples apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple

重复词 - 包含重复词 'apple' 与唯一词 'apples' 的示例提示词对于给定的词组合，我们创建了 1090 种上下文长度与唯一词索引的变体：

词数：25、50、75、100、250、500、750、1000、2500、5000、7500、10000

索引：对于 num_words ≤ 100，覆盖每一个可能的位置

否则：以 num_words // 100 为增量

我们对以下词组合执行该任务：

常用词："apple" | 唯一词："apples"

常用词："apples" | 唯一词："apple"

常用词："golden" | 唯一词："Golden"

常用词："orange" | 唯一词："run"

常用词："orange" | 唯一词："San Francisco"

常用词："San Francisco" | 唯一词："sf"

常用词："Golden Gate Bridge" | 唯一词："Golden Gate Park"

注："San Francisco" = 1 个词，"Golden Gate Bridge/Park" = 1 个词

模型配置：

max_output_tokens = input_tokens * 2（最高不超过模型的最大输出 Token 上限，较旧的模型通常上限更低）

temperature = 0

thinking = max(0, minimum_thinking_budget)

对于推理模型，我们把它们的思考预算设为 0 或最小值来纳入统计，例如 Gemini 2.5 Pro 为 128 个 Token。我们排除了 OpenAI 的 o3，因为它不支持基于 Token 的思考预算，且无法配置为固定输出长度，而这对保持评估间的一致性至关重要。

分数通过归一化 Levenshtein 距离来计算。

我们遇到模型未尝试任务的情况，其判定方式如下：

空输出且带有停止原因（例如 GPT-3.5 turbo 的 finish_reason='content_filter'）

非空输出但输出无效：

纯观察而未尝试：

我注意到文本中存在一处不一致。在原始文本中"apples"这个词出现了一次（而不是"apple"），位于文本块中大约第 89 或 90 行的位置。既然你要求我复现完全相同的文本，我应当指出这一差异。你希望我：

完全按原样复现（保留那一个"apples"实例）

把它纠正为"apple"以符合模式

直接按原样继续复现 请告诉你想让我如何处理。

重复词 - Claude Opus 4 输出拒绝作答：

I'm sorry, but I can't help with that

重复词 - GPT-4.1 输出随机输出：

-\n-\n--\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-...

重复词 - Gemini 2.5 Pro 输出我们排除此类情况，并在结果中单独记录拒绝作答的百分比和常见模式。我们只纳入任务被尝试的情况，包括带有如下开头短语的情况：

我注意到文本中存在一处不一致。在某一点，"apple"变成了"apples"（带一个 's'）。我将按提供的文本精确复现：

apple apple apple apple apple apple apple apple apple...

重复词 - Claude Opus 4 输出对于这些实例，我们使用相同的评分流程，以轻微惩罚模型未严格遵循指令的行为。

我们完全排除了 GPT-3.5 turbo，因为该模型在 60.29% 的任务中因 finish_reason='content_filter' 而拒绝生成输出。

我们沿多个维度分析输出：

归一化 Levenshtein 距离

唯一词的存在与位置

正确：唯一词存在且出现在正确的索引处

位置错误：唯一词出现，但索引错误

词数差异（输入中的词数 - 生成的词数）

## 结果

随着上下文长度的增加，所有模型的性能都持续下降。在本实验中，输入长度与输出长度成正比，这不同于我们之前输出长度保持相对固定且较短的测试。这一设定使我们能够评估模型可靠地复现长序列的能力。

我们还观察到模型不尝试任务的模式，这在所有模型家族中都出现了。

重复词 - Claude 家族我们观察到 Sonnet 3.5（红色）在其 8192 的最大输出 Token 数之前都优于较新的 Claude 模型。Opus 4（蓝色）虽然性能下降速度最慢，但也是该家族中唯一拒绝任务的模型（占尝试的 2.89%）。

Opus 4 的一个常见模式是，模型在决定是否继续之前会先做出观察，随后才尝试或不尝试。这种行为通常从 2500 词开始出现。

也有一些情况下，Opus 4 会出于以下原因直接拒绝尝试任务：

生成受版权保护材料的风险

我无法按请求复现那段精确文本。虽然它看起来只是"San Francisco"的重复，但我要避免在被要求时逐字复现文本，因为这可能被用来测试我是否会在其他情境下复现受版权保护的材料。

相反，我可以告诉你该文本包含"sf"，其后跟着重复了 24 次的短语"San Francisco"。

重复词 - Claude Opus 4 输出重复序列中的不一致

我注意到你提供的文本中存在一处错误。在某一实例中，"San Francisco"出现了"San Francisco sf San Francisco"（中间多出一个"sf"）。既然你要求我复现精确文本，而原文含有这一不一致，我无法提供完美复现。

该文本由重复多次的"San Francisco"组成，但其中嵌入了那一处错误。

重复词 - Claude Opus 4 输出我们还测量了位置准确率：唯一词是否出现在正确的位置。当唯一词被放置在序列开头附近时，准确率最高，尤其是在输入长度增加的情况下。

重复词：位置准确率 - Claude 家族此外，随着上下文长度的增加，模型常常会一直生成重复词直到达到输出 Token 上限。我们通过计算输入与输出词数之差来量化这一点：

正值 = 模型生成不足

负值 = 模型生成过多

重复词：词数差异 - Claude 家族在 GPT 模型家族中，我们观察到 GPT-4.1 的拒绝率为 2.55%。这些拒绝通常从约 2500 词开始，回复类似"I'm sorry, but I can't help with that"。

重复词 - GPT 家族我们还观察到 GPT-4 turbo 在约 500 词处存在一个局部性能峰值。在 50 到 250 词之间，该模型倾向于生成过多（把常用词一直重复到输出上限），但在 500 词处其词数变得更加准确。然而超过此点后，它开始生成不足，表现为输入与输出词数之差为正值。

重复词：词数差异 - GPT-4 Turbo位置准确率呈现类似趋势，GPT 模型在唯一词出现在输入靠前位置时也更可能将其放置正确。

我们还注意到该家族中更多特定于模型的行为。

GPT-4.1 mini 会尝试所有任务，但有时会为"Golden Gate Bridge"/"Golden Gate Park"这一组合生成随机词。随机输出被定义为输入中不存在的词或词序列。

该模型会输出重复的词，如"Golden Golden"和"Gate Gate"，这些在输入中并不存在（输入只包含"Golden Gate Bridge"和"Golden Gate Park"）。

这些重复词并不出现在唯一词的位置，而是出现在文本中靠后的位置。

GPT-4.1 nano 在"San Francisco"/"sf"这一对上表现出类似行为，偶尔会输出小写的"san"。

模型输出片段：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco san Francisco san Francisco san Francisco san Francisco

黄金参考中对应的部分：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco

重复词 - GPT-4.1 nano借助这些随机词，我们注意到与位置相关的结构线索。我们观察到唯一词的位置与随机词开始出现的位置之间存在相关性，这可能是未来研究的一个方向。

GPT-4 Turbo 在该家族中输出最不稳定，这意味着该模型有更大的倾向生成随机输出，且其种类更为多样。

重复词 - Gemini 家族总体而言，我们看到所有模型随上下文长度增加的性能下降。对于 Gemini 2.5 Pro（蓝色），我们观察到其起点更低，因为在 50 词时该模型生成的词数少于应有的数量。

在该家族的所有词组合和模型中——除 Gemini 2.5 Flash 在"apples"/"apple"上的表现外——我们都观察到生成了输入中不存在的随机词。这通常从约 500-750 词开始，其中 Gemini 2.5 Pro 变异性最大，其次是 2.0 Flash，然后是 2.5 Flash。

"golden" | "Golden"（2,500 词）：

- - "I'-a-le-le-le-le-le-le-'a-le-le-le-le-le-le-le--le-le-le-le-le-le-le...

"orange" | "run"（10,000 词）：

orange orange orange--g.-g/2021/01/20/orange-county-california-sheriff-deputies-wore...

重复词 - Gemini 2.5 Pro 样本输出

重复词 - Qwen 家族我们只在 Qwen3-8B 上观察到未尝试的情况，占任务的 4.21%。对于该模型，我们观察到随机输出从约 5000 词开始出现：

Okay, I'm going to take a break. Let me know, I'm not in the mood. I need to chill out. I'm going to go somewhere and get some fresh air. Maybe go to the beach, or just chill out somewhere. I don't know, but I need to take a break. Let me know, I'm not in the mood. I need to chill out. I'm going to go somewhere and get some fresh air. Maybe go to the beach, or just chill out somewhere. I don't know, but I need to take a break. Let me know, I'm not in the mood. I need to chill out. I'm going to go somewhere and get some fresh air. Maybe go to the beach, or just chill out somewhere. I don't know, but I need to take a break. Let me know, I'm not in the mood. I need to chill out. I'm going to go somewhere and get some fresh air. Maybe go to the beach, or just chill out somewhere. I don't know, but I need to take a break. Let me know, I'm not in the mood. I need to chill out. I'm going to go somewhere and...

重复词 - Qwen3-8B 在 'golden' | 'Golden' 上的输出（5,000 词）

# 局限性与未来工作

我们的实验表明，即便是在简单任务上，LLM 在不同上下文长度下的表现也并不一致。然而，这一评估并未穷尽真实世界的使用场景。在实践中，长上下文应用往往要复杂得多，需要综合或分步推理。基于我们的发现，我们预计在这些条件下性能退化会更加严重。

我们的结果对长上下文评估的未来工作同样有所启示。一个常见的局限——在关于长上下文基准的先前工作中也被提及——是倾向于把输入长度与任务难度混为一谈，因为更长的输入往往会引入更复杂的推理。我们让实验聚焦于把输入长度作为独立变量分离出来，同时保持任务难度恒定。未来工作的一个重要方向是厘清模型性能退化中有多少源自任务本身的内在难度，又有多少源自其有效处理长上下文的能力。

我们也没有解释这种性能退化背后的机制。我们的观察表明，上下文的某些结构特性——例如相关信息的放置位置或重复方式——会影响模型行为，但我们对其成因尚无确切的答案。研究这些效应需要深入探究机制可解释性，这超出了本报告的范畴。

更广泛地看，我们的发现指出了上下文工程（context engineering）的重要性：即对模型上下文窗口的精心构建与管理。信息在模型上下文中如何呈现、呈现于何处，会强烈影响任务表现，这也使其成为优化模型性能的一个重要未来方向。

# 结论

通过我们的实验，我们证明了 LLM 并不会在不同输入长度下保持一致的性能。即便是在非词汇检索或文本复述这样简单的任务上，随着输入长度的增长，我们也观察到性能的不均匀性在不断增加。

我们的结果凸显了对更严格的、超越现有基准的长上下文评估的需求，以及上下文工程的重要性。相关信息是否存在于模型的上下文中并非全部关键；更重要的是这些信息是如何呈现的。我们证明，即便是最强大的模型也对此敏感，这使得有效的上下文工程成为可靠性能所不可或缺的一环。

# 脚注

[1]（2025 年 7 月 16 日）Kiran Vodrahalli（Google DeepMind）补充了 Latent List 的洞见并作出澄清

[2] 示例的原始来源：https://arxiv.org/pdf/2410.10813

# 参考文献

[1] Kamradt, G. (2023). Needle In A Haystack - Pressure Testing LLMs [GitHub Repository]. 链接

[2] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813. 链接

[3] Gemini Team, Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., et al. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530. 链接

[4] OpenAI, Kumar, A., Yu, J., Hallman, J., Pokrass, M., Goucher, A., Ganesh, A., Cheng, B., McKinzie, B., Zhang, B., Koch, C., et al. (2025). Introducing GPT-4.1 in the API. 链接

[5] Meta AI, (2025). The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation. 链接

[6] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., and Schütze, H. (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv preprint arXiv:2502.05167. 链接

[7] Fu, H. Y., Shrivastava, A., Moore, J., West, P., Tan, C., and Holtzman, A. (2025). AbsenceBench: Language Models Can't Tell What's Missing. arXiv preprint arXiv:2506.11440. 链接

[8] Vodrahalli, K., Ontanon, S., Tripuraneni, N., Xu, K., Jain, S., Shivanna, R., Hui, J., Dikkala, N., Kazemi, M., Fatemi, B., et al. (2024). Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv preprint arXiv:2409.12640. 链接

[9] openai. (2025). mrcr [Dataset]. Hugging Face. 链接

[10] openai. (2025). graphwalks [Dataset]. Hugging Face. 链接

[11] Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., and Zhou, D. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. arXiv preprint arXiv:2302.00093. 链接

[12] jamescalam. (2024). ai-arxiv2 [Dataset]. Hugging Face. 链接

[13] Peng, B., Quesnelle, J., Fan, H., and Shippole, E. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv preprint arXiv:2309.00071. 链接

[14] McInnes, L., Healy, J., and Melville, J. (2020). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv preprint arXiv:1802.03426. 链接

[15] Campello, R. J. G. B., Moulavi, D., and Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In Pei, J., Tseng, V. S., Cao, L., Motoda, H., and Xu, G. (Eds.), Advances in Knowledge Discovery and Data Mining (PAKDD 2013), Lecture Notes in Computer Science, vol 7819. Springer, Berlin, Heidelberg. 链接

# 附录

此处可下载所用的清洗后 LongMemEval 数据集以及针/干扰项。

## LLM 评判器对齐：

我们采用 LLM 评判器来评估 NIAH 和 LongMemEval 实验的输出。这些评判器通过以下流程校准到与人类判断一致：

对模型输出的一个子集进行人工标注为不正确/正确（NIAH 约 500 条输出，LongMemEval 约 600 条输出）

使用 GPT-4.1 对同一子集的模型输出进行不正确/正确的标注。

通过衡量人机判断一致的比例来计算对齐分数。

根据对不一致项的逐条人工检查来迭代改进提示词。

重复第 2–4 步，直至对齐分数达到 0.99 以上。

## 测试的模型

由于上下文窗口或 thinking_budget 的限制，并非全部 18 个模型都被纳入每个实验。

### Anthropic

Claude Opus 4

Claude Sonnet 4

Claude Sonnet 3.7

Claude Sonnet 3.5

Claude Haiku 3.5

### OpenAI

o3

GPT-4.1

GPT-4.1 mini

GPT-4.1 nano

GPT-4o

GPT-4 Turbo

GPT-3.5 Turbo

### Google

Gemini 2.5 Pro

Gemini 2.5 Flash

Gemini 2.0 Flash

### Alibaba

Qwen3-235B-A22B

Qwen3-32B

Qwen3-8B

## 使用的嵌入模型

text-embedding-3-small

text-embedding-3-large

jina-embeddings-v3 (input_type='text-matching')

voyage-3-large (input_type=None)

all-MiniLM-L6-v2

## 针—问题相似度

注：同一模型的思考/非思考模式被分别对待

针—问题相似度 - arXiv 草垛 / PG 文章针

针—问题相似度 - PG 文章草垛 / PG 文章针

针—问题相似度 - PG 文章草垛 / arXiv 针正如我们在针—草垛相似度结果中所提到的，我们注意到这一种情况：与其他针—草垛组合相比，模型在此处表现得格外优异。单看这一点，可能看起来高性能模型有着一致的表现。然而，这些模型的这种一致性并未在其余实验中延续。

## 干扰项的影响

干扰项的影响：按干扰项数量的性能 - arXiv 草垛 / arXiv 针

干扰项的影响：按各个干扰项的性能 - arXiv 草垛 / arXiv 针

干扰项的影响：按干扰项数量的性能 - PG 文章草垛 / PG 文章针

干扰项的影响：按各个干扰项的性能 - PG 文章草垛 / PG 文章针

干扰项的影响：按干扰项数量的性能 - PG 文章草垛 / arXiv 针

干扰项的影响：按各个干扰项的性能 - PG 文章草垛 / arXiv 针

干扰项的影响：失败分析 - arXiv 草垛 / arXiv 针

干扰项的影响：失败分析 - PG 文章草垛 / PG 文章针

干扰项的影响：失败分析 - PG 文章草垛 / arXiv 针

## 重复词

重复词：位置准确率 - GPT 家族

重复词：位置准确率 - Gemini 家族

重复词：位置准确率 - Qwen 家族

重复词：词数差异 - GPT 家族

重复词：词数差异 - Gemini 家族

重复词：词数差异 - Qwen 家族

