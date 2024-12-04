# 人工标注员

推荐阅读 [这篇综述](https://aclanthology.org/2024.cl-3.1/) 的第三章，介绍了许多数据标注质量管理的实践经验。如果你追求的是生产级的质量，并且具备实施条件，那么请继续阅读吧！ 

  ![Best_annotation_practices](https://github.com/huggingface/evaluation-guidebook/blob/main/assets/best_annotation_practices.png?raw=true)

无论项目规模多大，一旦定义了具体的评估任务和打分细则，请注意：

- **选择合适的标注员，如果可能的话提供经济激励**
你可能希望参与任务的标注员具有以下品质：
1) 符合特定的人口统计特征。
	例如：母语是测试目标语言、较高的教育水平、特定领域的专业知识、多样化的地域背景等。 
	 根据评估任务不同，对标注员统计特征需求也不一样。
1) 提供高质量标注。
	有些任务中筛选合适的标注员很重要，比如近期有一种任务是检查回答是否是 LLM 生成的。
  *个人认为，除非你众包标注员有强烈的自我驱动意识，否则一般还是支付合理的费用更好。*

- **设计标注准则** 
请务必深入思考制定标注准则，非常值得花费大量时间去做！我们在制作 [GAIA](https://huggingface.co/gaia-benchmark) 数据集时的耗时最多的地方就是这里。

- **迭代标注** 
很多时候标注员会误解标注指南 (他们的想法可能比你想象的更模棱两可)，所以要做好多轮迭代标注的准备，来不断改进直到达到你的需求。

  - **质量检查** 和 **手动筛选**
你需要仔细检查答案的质量 (检查标注员间的答案一致性)，并筛选出质量最优、相关性最高的答案。

你也可以使用专用工具来构建高质量标注数据集，如 [Argilla](https://argilla.io/)。
### 深入阅读推荐链接：
- ⭐ [五分钟构建自己的标注平台](https://huggingface.co/learn/cookbook/enterprise_cookbook_argilla)，Moritz Laurer 出品的数据标注教程。这篇文章介绍了使用开源工具 (如 Argilla 和 Hugging Face) 的实际经验，可以帮助更好的理解大规模人工标注的注意事项。
- ⭐ [标注实践指南](https://aclanthology.org/2024.cl-3.1/)。这是一篇 2023 年所有关于人工标注论文的综述，内容完整，干货满满，但很容易理解。
- [ScaleAI 出品的另一篇标注实践指南](https://scale.com/guides/data-labeling-annotation-guide)，专注于人工评估。它是对上述文档的更轻量级补充。
- [关于减少人工标注分歧的假设与挑战](https://aclanthology.org/2024.naacl-long.126/)，论文探讨了标注员间分歧来源的原因，以及在实践中的缓解方法。
