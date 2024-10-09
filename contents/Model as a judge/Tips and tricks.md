## Mitigating well known biases of LLM as judges: 
- **Lack of internal consistency**: a judge might give you different judgments if you prompt it several times (if the temperature is not 0)
	- You can mitigate this by doing self-consistency prompting of your judge, prompting it multiple times and keeping the majority output
- **Self-preference**: they tend to [favor their own outputs](https://arxiv.org/abs/2404.13076) when scoring answers
	- You can mitigate this by using a jury
- **Blindness to input perturbation**: models are bad at identifying [perturbated input](https://arxiv.org/abs/2406.13439)and tangentially [bad at providing consistent score ranges](https://twitter.com/aparnadhinak/status/1748368364395721128) (extended experiments on this [here](https://github.com/LeonEricsson/llmjudge/blob/main/README.md)). For example, if asked to rank text quality on text where noise has been added on a consistent scale, the grades predicted do not reflect this scale. 
	- You can mitigate this by 
		- asking the model to explain its reasoning [before providing a score](https://twitter.com/seungonekim/status/1749289437165769177)
		- providing a coherent grading scale in the prompt.
- **Position-bias**: they tend to [favor specific answer positions](https://arxiv.org/abs/2306.05685). For example, when presented with pairwise comparisons, Claude and GPT3.5 tend to quite systematically prefer the first choice, or the second choice
	- You can mitigate this by 
		- switching answer positions randomly
		- computing the log-probabilities of all possible choices to get a normalized answer
- **Verbosity-bias** (or length-bias): they tend to like more verbose answers
	- You can mitigate this by [accounting for the answer difference in length](https://arxiv.org/abs/2404.04475)
- **Debatable consistency [with human answers](https://arxiv.org/pdf/2308.15812):**
	- However, it's also [debatable if non-expert humans are a good baseline for absolutely all evaluations](https://arxiv.org/abs/2202.06935). For some specific domains (medical, legal, mathematics, etc), relying on non-expert human annotators is as bad a baseline as using an LLM directly.
- **Format bias**: they tend to fail to evaluate accurately if the prompt format [is too far away](https://arxiv.org/pdf/2310.17631) from what it's been trained with. For example, a model trained to do pairwise comparison with an added reference answer will fail if said answer is not provided, and failures will also occur the other way around.
	- You can mitigate this by paying attention to the training prompt format (if the model was instruction tuned) and ensuring you follow it.

## Picking correct tasks for an LLM judge
LLM evaluators:
- are **bad at identifying hallucinations** in general, particularly what are called partial hallucinations (which look close to the ground truth but are actually slightly different) (see [this](https://arxiv.org/abs/2305.11747) and [this](https://arxiv.org/abs/2303.08896))
- have a low to OK-ish correlation with human annotators on [summarization](https://arxiv.org/abs/2304.02554) ([here too](https://arxiv.org/abs/2303.16634)), [faithfulness](https://arxiv.org/abs/2307.16877), and are not consistently correlated with human judgement more broadly against [a scope of tasks](https://arxiv.org/abs/2406.18403)
