# 评估你的评估结果

在生产中或大规模使用 LLM 评估模型之前，你需要先评估它在目标任务的表现效果如何，确保它的评分跟期望的任务表现一致。

注：*如果评估模型的输出结果是二元分类，那么评估会相对简单，因为可使用的解释性分类指标有很多 (如准确率、召回率和精确率)。但如果输出是在某个范围内的分数，评估起来就会困难一些，因为模型输出和参考答案的相关性指标很难与分数映射的非常准确。*

在选定 LLM 评估模型以及设计 prompt 之后，还需要：

## 1. 选择基线
你需要将选定模型的评估结果与基线对比。基线可以是很多种类型，如：人工标注结果、标准答案、其他表现良好评估模型的结果、其他 prompt 对应模型的输出，等等。

测试用例的数量不需要非常多 (50 个足以)，但必须极具代表性 (例如边缘用例)、区分性、并且质量足够高。

## 2. 选择评估指标
评估指标是用来比较评估结果和参考标准之间的差距的。 

通常来说，如果比较对象是模型的二元分类或成对比较属性，评估指标计算起来就非常容易，因为一般使用召回率 (二元分类)、准确率 (成对比较)、和精确率作为评估指标，这些指标容易理解、且具有可解释性。

如果比较对象是模型得分与人类评分，则计算指标就会困难一些。如要深入理解可以阅读 [这篇博客](https://eugeneyan.com/writing/llm-evaluators/#key-considerations-before-adopting-an-llm-evaluator)。

总的来说，如果你不清楚如何选择合适的评估指标或者评估模型，可以参考 [这篇博客](https://eugeneyan.com/writing/llm-evaluators/) 中的 [图表](https://eugeneyan.com/assets/llm-eval-tree.jpg) ⭐。

## 3. 评估你的评估结果
这一步你只需用评估模型和测试 prompt 来评估在样本上的表现，拿到评估结果之后使用上一步选定的评估指标计算分数即可。

你需要确定一个阈值来决定结果归属，阈值大小取决于你的任务难度。例如成对比较任务的准确率指标可以设为 80% 到 95%，再比如评分排名任务的相关性指标，文献中经常使用 0.8 的皮尔逊相关系数，不过也有一些论文认为 0.3 足以表明与人工评估的相关性良好。所以标准不是死的，根据任务灵活调整吧 (^^") ！



