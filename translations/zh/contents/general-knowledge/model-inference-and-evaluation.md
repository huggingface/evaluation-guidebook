# 模型推理与评估

## 引言
现阶段大型语言模型的工作原理很简单：给定输入文本，模型学习预测合理的后续内容。

这个过程分为两步。
### 分词
输入文本 (推理阶段也叫 *prompt (提示词)*) 首先被拆分为多个 *token*，一个 token 表示文本的一小段 (可以是一个或多个字符，也可以是一个单词)，每个 token 都会被映射为一个数字。模型能够解析的全部 token 的范围叫做该模型的 *vocabulary (词汇表)*。*([Tokenization](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/tokenization.md) 页面有对分词更深入的解释)*.

### 预测

![](https://github.com/huggingface/evaluation-guidebook/blob/main/assets/llm_tk_1.png?raw=true)

给定输入文本，LLM 会在所有词汇表中生成下一个 token 的概率分布。如要持续生成，我们可以选择概率最高的 token (此过程中可以引入一些随机性来获得更有趣的输出) 拼接至 prompt 的末尾作为下一个输入来生成后续 token，然后重复这个操作，依此类推。

## 评估的预测目标
LLM 评估根据预测目标可以大致分为两类：
- 给定一个 prompt 和对应的一个 (或多个) 回答，模型预测该回答的概率是多少？
- 给定一个 prompt，模型生成回答的内容是什么？
### 对数似然评估
对数似然评估的预测目标为：给定 prompt 下的单选或多选回答的条件概率。换句话说就是，输入一句话，模型输出特定续写的可能性有多大？ 
具体步骤为:
- 将每个选项与 prompt 拼接并输入给 LLM，模型根据前面的内容输出每个 token 的 logit 值
- 仅保留最后的 logit 值 (与选项的 token 相关)，应用对数 softmax 来获取对数概率 (范围为 `[-inf, 0]`，而不是 `[0-1]`)
- 然后将所有选项 token 的对数概率相加，获得多选的整体对数概率
- 最后可以根据选项长度进行归一化

![](https://github.com/huggingface/evaluation-guidebook/blob/main/assets/llm_logprob.png?raw=true)

可以使用以下任一方式来计算评估指标：
- 获取模型在多选回答中的首选偏好，如上图。(*不过这种评估方式会使得此类模型得分偏高：不做限制时会生成选项之外回答的模型。如图中的 `Zygote`*)
- 测试模型单选概率是否高于 0.5
- 研究模型校准。一个校准良好的模型会对正确回答预测最高的概率。
  *(要深入了解校准可以阅读 Anthropic 的 [这篇论文](https://arxiv.org/abs/2207.05221)，里面详细介绍了校准的定义、检测方法、以及怎样训练一个校准良好模型。另外要了解校准的一些局限性可以阅读 [这篇论文](https://arxiv.org/abs/2311.14648))。*

### 生成式评估
对于生成式评估的预测目标，我们希望得到给定 prompt 下模型生成的文本。 

我们可以通过自回归的方式获得生成文本：将 prompt 输入模型，将模型预测概率最高的下一个 token 选定为模型的 “首选 token”，然后重复这一过程，直到达到生成结束条件 (最大 token 长度、停止生成的特殊 token 等)。模型生成的所有 tokens 都视为对该 prompt 的回答文本。

![](https://github.com/huggingface/evaluation-guidebook/blob/main/assets/llm_gen.png?raw=true)



然后我们可以将生成文本与参考回答进行比较，并通过计算两者之间的差距进行评分 (可以使用简单指标评判，例如是否精确匹配，或者诸如 BLEU 的复杂指标，甚至可以使用模型进行评估)。

### 深入阅读推荐链接
-  ⭐ [多种评估 MMLU 的方法](https://huggingface.co/blog/open-llm-leaderboard-mmlu)，我所在的 Hugging Face 团队撰写的博客。如果你想更深入了解多选对数似然评估和生成式评估之间的差异，包括这些差异对评分变化的意义，推荐阅读此文。
	- 上述插图来自 Thom Wolf 的博客
- ⭐ [EleutherAI 论文中对上述推理方法背后绝美的数学公式推导](https://arxiv.org/abs/2405.14782v2)，可以直接跳到附录部分查看。
## 约束模型输出
在许多情况下，我们希望模型的输出遵循特定格式，例如在需要与参考回答进行比较时。约束方法有：
### 使用 prompt
最简单的方法是添加一个任务 prompt，其中包括了非常具体的指示，来告诉模型如何回答 (例如：`使用数字形式回答`、`不要使用缩写` (`Provide numerical answers in digits.`,`Use no abbreviation`) 等)。

虽然这种方法并不能保证每次都有效，但对于高能力模型来说效果已经足够好。这也正是我们在 [GAIA](https://huggingface.co/papers/2311.12983) 论文中采用的方法，如果你想获取一些任务 prompt 的书写灵感，可以在 [leaderboard](https://huggingface.co/spaces/gaia-benchmark/leaderboard) 页面的 Submission 标签中找到我们设计的任务 prompt。
### Few-shot 和上下文学习
另一种约束模型输出的方法是 “上下文学习 (in context learning)”。通过在 prompt 中提供示例 (称为 `few-shot prompting`)，使得模型隐性地遵循重复的 prompt 模式，进而输出回答文本。

这种方法直到 2023 年底整体效果都还不错！然而随着指令微调 (instruction-tuning) 方法的广泛使用，以及在模型预训练的后期阶段 (继续预训练) 加入了更多的指令数据，似乎使得新模型倾向于遵循特定的输出格式 (在 [这篇论文](https://arxiv.org/abs/2407.07890) 中称为 `在测试集上训练`，或者叫 `过拟合 prompt 格式`)。另外对于稍旧的模型，特别是上下文窗口较小的模型，这种方法也有点受限，因为某些 few-shot 示例可能无法被拟合到上下文窗口里。
### 结构化文本生成
结构化文本生成的方法通过预定义语法或正则表达式来约束模型输出。例如，`outlines` 库通过有限状态机 (FSM) 实现了这个方法，非常巧妙。(实际还有其他实现方法，比如使用交错生成来约束 JSON 格式输出。但 FSM 是我个人最喜欢的方法)

如想了解结构化生成方法的原理，可以阅读我们写的这篇 [博客](https://huggingface.co/blog/evaluation-structured-outputs)：结构化生成降低了评估中的 prompt 方差，使得评估结果和排名更加稳定。你还可以查看 `outlines` 库的概览 [博客](https://blog.dottxt.co/)，了解更多与结构化生成相关的有趣实现和观察结果。 

不过，一些最新 [研究](https://arxiv.org/pdf/2408.02442) 表明，结构化生成在某些任务 (例如因果推断) 中可能会降低模型性能，因为它使得先验分布偏离了预期的概率分布。

### 深入阅读推荐链接
-  ⭐ [理解结构化生成的有限状态机工作原理](https://blog.dottxt.co/coalescence.html)，由 Outlines 出品的博客，提供了非常清晰的可视化指南。
- [outlines 方法的论文](https://arxiv.org/abs/2307.09702)，对上述博客更加学术的解释
- [Guidance-AI 的官方 repo 实现的交错生成方法](https://github.com/guidance-ai/guidance?tab=readme-ov-file#guidance-acceleration)，是另一种约束模型遵循特定格式输出的方法。
