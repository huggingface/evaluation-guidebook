# 选择 LLM 评估模型

使用现有的 LLM 评估模型时，你可以选择：[通用性强、能力高的大模型](https://arxiv.org/abs/2306.05685v4)、[专业性强、特定数据偏好的小模型](https://arxiv.org/abs/2405.01535)、或自行训练模型。

## 使用大型专家 LLM

随着更强大的 LLMs (如 ChatGPT) 的不断推出，研究者们开始探索使用 LLM 作为评估模型。目前在评估任务上表现最好的仍然是闭源模型 (如 Claude 或 gpt-o)，不过得益于高质量开源模型 (如 [Qwen 2.5](https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e)，[Command R+](https://huggingface.co/CohereForAI/c4ai-command-r-plus-08-2024)，以及 [Llama 3.1-405-Instruct](meta-llama/Llama-3.1-405B-Instruct)) 快速发展，开源与闭源模型之间的差距正在迅速缩小。

尽管闭源模型效果很好，也存在一些局限性：
- 只能使用 API 方式调用。这意味着 API 背后的模型以及输出结果可能随着版本更替 (有时候甚至不发公告说明) 而改变，进而影响评估结果的可重复性。
- 黑箱性质。可解释性较差。
- 数据隐私泄露风险。使用 API 时需要将数据发送给第三方 (比本地数据管理安全性差得多)，你无法确定数据会被怎样处理 (一般需要筛选一下训练集中的数据)。

闭源模型的优点也很明显，无需本地配置或硬件支持，任何人都可以轻松地访问高质量模型。不过这些优点开源模型也具备，大多数高质量开源模型提供商本身就提供了 API 访问，同时还缓解了上述两个局限性。

如果你需要选择模型提供商，可以参考 [这篇博客](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard)，了解一下成本分析的内容。

## 使用小型专家 LLM

你也可以选择使用小型专业 LLM 评估模型，它们的参数量通常只有几 B，可以在大多数现代消费级硬件上部署和运行，甚至可以自行从头训练或指令微调。直接使用也很简单，只需要遵循模型特定的 prompt 格式就行。

可选的模型有：
- Flow-Judge-v0.1 ([权重链接](https://huggingface.co/collections/flowaicom/flow-judge-v01-66e6af5fc3b3a128bde07dec))：3.8B 参数，基于 Phi-3.5-mini-instruct，在合成偏好数据集上微调
- Prometheus ([权重链接](https://huggingface.co/prometheus-eval/prometheus-13b-v1.0)，[论文链接](https://arxiv.org/abs/2310.08491))：13B 参数，在合成偏好数据集上从头训练。还有一个 7B [v2](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0) 版本：基于 Mistral-7B-Instruct-v0.2，在更大的合成偏好数据集上微调，且加入了权重融合
- JudgeLM ([论文链接](https://arxiv.org/abs/2310.17631))：7B 到 33B 参数，在多个模型生成的合成偏好数据集上从头训练。

## 自行训练 LLM
你也可以选择训练或微调自己的 LLM 评估模型。

首先要为任务目标收集偏好数据。可选的数据有：
- 现有的 [人类偏好数据集](https://www.kaggle.com/competitions/lmsys-chatbot-arena)
- 模型生成的偏好数据 (可以参考上述小型评估模型论文中的数据部分，也可以直接点击链接获取，如 Prometheus [偏好数据集](https://huggingface.co/datasets/prometheus-eval/Preference-Collection) 和 [反馈数据集](https://huggingface.co/datasets/prometheus-eval/Feedback-Collection))。

然后需要决定模型训练方式，是从头训练还是微调现有模型。步骤包括：
- 蒸馏大模型为小模型
- 量化
- 使用上一步的数据微调 (如果模型较大且计算资源有限，可以使用 peft 或 adapter 权重的方式)
	- 有帖子指出 [从奖励模型开始微调比指令模型的效果更好](https://x.com/dk21/status/1826292289930674590)
