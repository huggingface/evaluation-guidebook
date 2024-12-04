# 分词

## 为什么以及如何对文本进行分词？
LLM 本质上是庞大的数学函数，模型只能处理数字，无法直接处理文本。

所以我们需要把文本转化为数字。具体地，如给定一句文本，须先将它以某种方式切分成多个小段，再将每个小段映射为一个数字。这个过程就叫 *分词 (tokenization)*。

在英文中，以前大家的做法是将文本句子中的每个字符与字母表索引对应起来 (例如 `a` -> 1, `b` -> 2 等)，这称为 *基于字符的分词* (按字符切分)。另一种做法是，将每个单词与词典索引对应起来 (例如 `a` -> 1, `aardvark` -> 2, `ab` -> 3 等)，这称为 *基于单词的分词* (英文或其他带有空格的语言可以按空格切分，不含空格的语言就会稍微复杂一些，例如中文)。

然而这些方法都存在很强的局限性：它们丢失了输入文本中的部分信息，尤其是单词形态中反映出的语义联系 (例如，`dis similar`、`similar`、`similar ity`、`similar ly` 等)。实际上我们希望模型能够保留并学到这些信息，以便把有语义联系的单词关联起来。
(此外，如果输入文本突然出现一个全新的单词，就没法将它映射到已有数字中，那么模型就处理不了这个词😔)

很自然地，有人提出了将单词切分为子词，并为这些子词分配数字索引 (例如 `dis`、`similar`、`ity`、`ly`)！

最开始这个过程是根据形态句法规则 ("morpho-syntax"，即构词法的语法规则，如词缀、词形等) 实现的。现在使用更多的是字节对编码 (BPE, byte pair encoding)，这是一种智能统计方法，可以根据参考文本中的词频自动计算和切分子词。

小结：分词是一种将切分的文本小段 (可以是一个或多个字符，也可以是一个单词) 映射为数字 (类似于索引) 的方法。对输入文本 (推理阶段也叫 *prompt*) 进行切分和映射的工具叫 *分词器 (tokenizer)*，文本被切分的小段叫 *token*，分词器或模型能够解析的全部 token 范围叫 *词汇表 (vocabulary)*。
#### 深入理解分词：
建议深入阅读前两个链接。
- ⭐ [HuggingFace 🤗 NLP 课程中对不同分词方法的解释](https://huggingface.co/learn/nlp-course/en/chapter2/4)
- ⭐ [HuggingFace 🤗 transformers 库说明文档中的分词基本概念及代码用法](https://huggingface.co/docs/transformers/en/tokenizer_summary)
- [Jurafsky 制作的分词课程](https://web.stanford.edu/~jurafsky/slp3/2.pdf)。这个课程更偏学术，可以直接跳到 2.5 和 2.6 章 (其余章节也很有趣，但范围太广有些超纲) 阅读。

#### 深入理解字节对编码
- ⭐ [HuggingFace 🤗 NLP 课程中对 BPE 的解释](https://huggingface.co/learn/nlp-course/en/chapter6/5)
- [首次提出 BPE 的论文](https://aclanthology.org/P16-1162/)


## 分词中要注意的问题
### 选择合适的词汇表大小
词汇表的大小决定了模型需要学习的单位 token (例如子词) 的数量。 

如果词汇表 **太大**，可能会包含一些非常罕见的词，不做切分直接映射为一个完整的词 token (例如：`aardvark`)，这会导致两个问题：

一方面，如果这些几乎从未出现过的罕见词加入训练数据中，模型可能很难学习它与其他语义概念的联系，导致难以推断其含义。

另一方面，如果这些罕见词仅出现在特定的上下文中，模型可能会将它关联到某些非常具体的词。例如在论坛数据上训练时，分词器将某个用户名完整映射为一个 token 并加入词汇表，那么模型可能会将此 token 关联到该用户发布的特定内容上去。

如果词汇表 **太小**，同样会带来两个问题：表达能力太弱、推理成本增加。

回到之前对 `similar` 的派生词进行分词的例子。如果使用类 BPE 方法 (大词汇表) 将会把 `similarly` 切分为两个 tokens (`similar` 和 `ly`)。而如果使用基于字符的分词方法 (词汇表非常小，只包含字母表)，那么这个单词就会被切分为 9 个 tokens (`s`, `i`, `m`, `i`, `l`, `a`, `r`, `l`, `y`)。

第一种方法将 `similarly` 切分为了具有独立语义的 token，而第二种方法由于词汇表太小，导致切分时丢失了一些语义表征。另外在推理生成一个单词时，token 表征长度的不同还导致了推理成本的差距，较小的词汇表生成的成本更高 (9 个 tokens 的生成成本比 2 个 tokens 增加了 4 倍以上!)。

目前大部分人采用启发式方法，根据模型大小和涵盖的语言数量来推断词汇表大小。在选择适合自己模型的词汇表大小时，也可以参考同等量级模型的词汇表大小来确定。
#### 深度理解罕见 token
- [SolidGoldMagikarp 在 Less Wrong 上的帖子](https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation)
	- 很有趣的文章，介绍了大家如何在 OpenAI 的词汇表中找到极其罕见的 token。这真的很酷！因为是在未访问模型内部信息的情况下完成的 (例如没人知道 OpenAI 的训练数据内容)。 
- [Cohere 的论文：Fishing for Magikarp](https://arxiv.org/abs/2405.05417)
	- 检测模型 token 的工作。

### 管理多语言环境
(建议：在阅读本部分前先了解 BPE 的相关内容)
选择分词器时，词汇表是根据参考文本构建的，也就是说分词器是认识参考文本中的词汇和字符的，而一般情况下文本主要为英语和拉丁语。

如果你想要模型学习一门新语言，而且很幸运，该语言使用的字母表和词根等与原语言相同，那么理论上模型学到的原语言的语义表征可以迁移到新语言中。

然而，如果你希望分词器能够对其他语言的文本进行正确的分词 (尤其是字母表不同的语言)，那么最好在构建分词器时就包含这些语言的数据。大部分情况下，新语言 (如泰语或缅甸语) 数据的加入会使得与原语言 (如英语) 的比例不平衡，原语言的占比通常高的多。由于当前常用的高效分词方法 (如 BPE) 是基于词频来创建复杂的词汇表，而英语使用频率最高，其单词会被切分为较长的 token。相比之下，不太常见语言的单词则会被切分为字符级别的 token。

这种现象导致了多语言分词中的不平衡现象：不常见 (低频、或 *低资源*) 的语言反而需要更多的 tokens 数才能生成与英语相同长度的文本。

#### 深入理解多语言分词
- ⭐ [Yennie Jun 对跨语言分词问题的精美分析与演示](https://www.artfish.ai/p/all-languages-are-not-created-tokenized)
	- 非常清晰明了！也建议亲自试用一下 HuggingFace 上的在线多语言分词 [space](https://huggingface.co/spaces/yenniejun/tokenizers-languages)。
- ⭐ [Aleksandar Petrov 制作的关于分词不平衡的 demo](https://aleksandarpetrov.github.io/tokenization-fairness/)
	- 推荐阅读 `Compare tokenization of sentences` 部分，来对不同语言推理的成本差异有一个大致的感觉。

### 数字分词问题
构建分词器时，还需要决定如何处理数字：是仅对 0 到 9 进行索引，并假设其他所有数字都可以由这些基础数字组合；还是要单独存储一定量级的 (例如一百万以内的) 所有数字？目前的知名模型采取了多种方法处理数字分词问题，但哪种方法更有利于数学推理仍然没有确定的答案。或许会出现诸如层级分词的新方法更适合处理这个问题。
#### 深入理解数字分词
- ⭐ [Yennie Jun 制作的可视化 demo，展示了 Anthropic、Meta、OpenAI 以及 Mistral 模型如何对数字分词](https://www.artfish.ai/p/how-would-you-tokenize-or-break-down) 
- [Beren Millidge 总结的多年来数字分词问题的演变](https://www.beren.io/2024-05-11-Integer-tokenization-is-now-much-less-insane/)
