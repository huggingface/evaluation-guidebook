# 设计你自己的评估 prompt

## 通用 prompt 设计建议
我总结的互联网上通用 prompt 的通用设计原则如下：
- 任务描述清晰：
	- `Your task is to do X (你的任务是 X)`. 
	- `You will be provided with Y (你拿到的信息是 Y)`.
- 评估标准精细，评分细则详尽 (如有必要)：
	- `You should evaluate property Z on a scale of 1 - 5, where 1 means ... (根据属性 Z 的表现进行评分，评分范围为 1 - 5，其中 1 分表示 ...)`
	- `You should evaluate if property Z is present in the sample Y. Property Z is present if ... (请指出样本 Y 中是否具备属性 Z，如果具备，那么 ...)`
- 加入一些 “推理” 评估步骤
	- `To judge this task, you must first make sure to read sample Y carefully to identify ..., then ... (评估此任务之前，请先仔细阅读样本 Y，识别出 ...，然后再 ...)`
- 输出格式明确 (添加特定字段可以提升一致性)
	- `Your answer should be provided in JSON, with the following format {"Score": Your score, "Reasoning": The reasoning which led you to this score} (以 JSON 格式回答，格式为 {"Score": 评分, "Reasoning": 评分推理过程})`

Prompt 书写灵感可以参考 [MixEval](https://github.com/huggingface/lighteval/blob/main/src/lighteval/tasks/extended/mix_eval/judge_prompts.pyy) 或 [MTBench](https://github.com/huggingface/lighteval/blob/main/src/lighteval/tasks/extended/mt_bench/judge_prompt_templates.py) 的 prompt 模板。

其他要点：
- 成对比较比对输出评分[更能反映人类的偏好](https://arxiv.org/abs/2403.16950)，且通常更稳健
- 如果任务确实需要对输出评分为具体的值，建议使用整数，并详细解释 [每个分值的代表含义](https://x.com/seungonekim/status/1749289437165769177)，或添加说明 prompt `如 provide 1 point for this characteristic of the answer, 1 additional point if ... (回答具备某项特性得 1 分，如果 ... 再加 1 分)` 等
- 尽量每评估一项能力就使用专门评分 prompt，会得到更好而鲁棒的结果

## 提升评估准确性
可以通过以下方式或技术来提升评估准确性 (有可能会增加成本)：
- **Few-shot 示例**：提供少量示例可以帮助模型理解和推理，但也会增加上下文长度。
- **引用参考**：提供参考内容可以提高模型输出的准确性。
- ***思维链 (CoT)**：要求模型 **在评分之前** 给出推理过程，可以 [提高准确性](https://arxiv.org/abs/2212.08073) (参考这篇 [帖子](https://x.com/seungonekim/status/1749289437165769177))。
- **多轮分析**：可以更好地 [检测事实性错误](https://arxiv.org/abs/2305.13281)
- **陪审团机制**：汇总多个评价模型的结果 [比单一模型的结果更好](https://arxiv.org/abs/2404.18796)。 
	- 使用多个小模型替代一个大模型可以大幅降低成本。
	- 也可以使用一个模型的多个温度参数来进行多次实验。
- 社区意外发现，prompt 引入奖励机制 (`例如：回答正确将得到一只小猫`) 可以提高回答正确性。这个方法的效果视场景而异，你可以根据需求灵活调整。

注：如要减少模型偏见，可以参考社会学中的问卷设计，然后根据使用场景来书写 prompt。如想使用模型来替代人工评估，可以设计类似的评价指标：如计算标注员一致性，使用正确的问卷方法来减少偏见等。

不过在实际应用中，大多数人并不需要完全可复现且高质量无偏的评估，快速且略显粗糙的 prompt 就能满足需求。(只要知悉使用后果，这种情况也是能接受的)。
