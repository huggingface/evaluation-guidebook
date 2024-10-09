## General prompt design tips
Some general guidelines I've come across online when designing the prompt itself are:
- Provide a clear description of the task at hand:
	- `Your task is to do X`. 
	- `You will be provided with Y`.
- Provide clear instructions on the evaluation criteria, including a detailed scoring system if needed:
	- `You should evaluate property Z on a scale of 1 - 5, where 1 means ...`
	- `You should evaluate if property Z is present in the sample Y. Property Z is present if ...`
- Provide some additional "reasoning" evaluation steps:
	- `To judge this task, you must first make sure to read sample Y carefully to identify ..., then ...`
- Specify the desired output format (adding fields will help consistency)
	- `Your answer should be provided in JSON, with the following format {"Score": Your score, "Reasoning": The reasoning which led you to this score}`

You can and should take inspiration from [MixEval](https://github.com/huggingface/lighteval/main/src/lighteval/tasks/extended/mix_eval/judge_prompts.py) or [MTBench](https://github.com/huggingface/lighteval/main/src/lighteval/tasks/extended/mt_bench/judge_prompt_templates.py) prompt templates. - broken link

Other tidbits:
- Pairwise comparison [correlates better with human preference](https://arxiv.org/abs/2403.16950) than scoring, and is more robust generally.
- If you really want a score, use an integer scale make sure you provide a detailed explanation for what [each score represents](https://x.com/seungonekim/status/1749289437165769177), or an additive prompt (`provide 1 point for this characteristic of the answer, 1 additional point if ...` etc)
- Using one prompt per capability to score tends to give better and more robust results

## Improving judgment accuracy
You can also improve accuracy using the following, possibly more costly, techniques:
- **Few shot examples**: like in many other tasks, if you provide examples it can help its reasoning. However, this adds to your context length.
- **Reference**: you can also enhance your prompt with a reference if present, which increases accuracy 
- **CoT**: [improves accuracy](https://arxiv.org/abs/2212.08073), if you ask the model to output its chain of thought **before** the score (also observed [here](https://x.com/seungonekim/status/1749289437165769177))
- **Multiturn analysis**: can improve [factual error detection](https://arxiv.org/abs/2305.13281)
- Using **a jury** (many judges, where you pick an aggregate of the answers): [gives better results](https://arxiv.org/abs/2404.18796) than using a single model. 
	- It can be made considerably less costly by leveraging many smaller models instead of one big expensive model. 
	- You can also experiment with using one model with variations on temperature
- Surprisingly, the community has found that adding stakes to the prompts (`answer correctly and you'll get a kitten`) can increase correctness. Ymmv on this one. -

Note on prompting: Depending on the stakes of your use case, to remove as much bias as possible, you would want to look at work done in sociology on how to design good surveys. If you treat your evaluator as a replacement for a human annotator, then you need to look at similar metrics: computing inter-annotator agreement, using correct survey design methodology to mitigate bias, etc.

However, most people don't really want a reproducible and high quality unbiased eval, and will be happy with quick and dirty evaluation through OK-ish prompts. (Which is an OK situation to be in! Just depends on the consequences attached).
