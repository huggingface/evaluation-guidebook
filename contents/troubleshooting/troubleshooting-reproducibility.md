# Troubleshooting reproducibility

Let's say you have read a recent tech report about a cool new model, and you want to reproduce their results on your machine... but you're not managing to?
Let's explore why.

## Different code base
To reproduce evaluation scores to the decimal point, you first need to make sure you're using exactly the same code base as the paper you want to reproduce. 

Usually, this means either using the evaluation default code as provided by the authors, or a standard implementation in a reference library like Eleuther's AI `lm_eval` or HuggingFace's `lighteval`. However, if the code source for evaluation is not provided, then, I'm sorry for you but it's unlikely that you'll be able to reproduce the results precisely. 

If you want to easily understand what kind of discrepancies happen when using different implementations, you can explore [this blog](https://huggingface.co/blog/open-llm-leaderboard-mmlu) (⭐) we wrote with the eval team at HuggingFace. It studies the differences we observed between 3 common implementations of the MMLU evaluation (in `lm_eval`, `helm`, and in the original author implementation), and how they change model scores. 

*Note: This is precisely for this reason that a Hugging Face team decided to launch the [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard), to get unified and homogeneous comparisons of models scores in order to compare them to internal experiments.*

### Other subtle ways in which the implementation can be different
We've observed that the following were easy things to mess up, even when using the same code base:
- **Different random seeds.** 
	- Normally, inference is less affected by random seeds than training. However, they can still affect some CUDA operations (see the PyTorch page on [reproducibility](https://pytorch.org/docs/stable/notes/randomness.html)) and change predictions if you're using a non greedy generation strategy. They can also affect the prompt if you're using few-shots, and some pre or post-processing functions. 
	  -> A tiny change can result in a couple of points of difference.
- **Actually different metrics**. 
  Metrics can be different in practice even if they share the same name. Some examples:
	- If the original implementation is a *log likelihood* `exact match` (computing the log probabilities of different possible answers), and you're using a *generative* `exact match` (only comparing the main greedy generation with the reference), you won't get the same scores.
	- We also saw, in evaluation code bases, a number of tasks which were defined as `exact match`, but were actually `prefix exact match` (comparing only the beginning of the generation with the reference), or `suffix exact match` (the opposite), or `quasi exact match` (exact match with a normalization). 
	 -> You therefore can't rely only on the metric name to determine what is happening, and need to look at the code.
- **Different normalization**.
	- To go back to our above `exact match` comparison example, in `lm_eval` v1, a number of tasks were simply named generative `exact match`: you would assume from this that the prediction is *compared as such* to a reference. 
	  Looking at the code, the prediction would instead go through a normalization step (removing punctuation, homogenizing numbers, etc) before being compared to the reference. This will obviously change results quite a lot. 
	  (The `lm_eval` v2 now includes the normalization name in most metric names.)
	 -> This is one of the easiest things to mess up, especially for tasks which require a lot of normalization/answer post processing, like math evaluations (where you want to extract the answer from a generated explanation).

## Different prompt
3 main things can come into play for prompt variation.
### Prompt itself
The format you are using for the prompt can and will change scores wildly. 

For example, for multichoice question answers, some common formats include very simple variations when presenting the choices, such as:
```
Question: <text of the question>
Choices:
```
```markdown
| A. <Choice A> | (A) <Choice A> | <Choice A> | 
| B. <Choice B> | (B) <Choice B> | <Choice B> | 
| C. <Choice C> | (C) <Choice C> | <Choice C> | 
| D. <Choice D> | (D) <Choice D> | <Choice D> | 
```
```
Answer: 
```
and predicting either `A`/`B`/`C`/`D` or `<Choice A/B/C/D>`.

These prompts are **semantically equivalent**, as they contain the exact same content - but they can still result in a difference of *several points for the same model*. We did some experiments on this [here](https://x.com/clefourrier/status/1777319187913875893/photo/1) (you'll see up to a 7 points difference for the same model) and a [paper observed similar results](https://arxiv.org/abs/2310.11324).

Some tasks are also prefixed with a task prompt (eg: `The following questions are about <topic>`) - its presence or absence will also affect the scores.

This [great paper](https://arxiv.org/abs/2407.07890)⭐ also highlights a side effect of this: a number of models are now trained to overfit benchmark prompts and answer formats, to the cost of adaptation to other prompts at evaluation time.

This is something we observed on the Open LLM Leaderboard 2 for the Llama3.1 models. They were predicting the correct answers to our MATH-Hard evaluations, but were getting low scores, being unable to fit to the template provided in few-shot because they overfit the GSM8K prompt and answer format (another math eval).
### System prompt and chat template
Chat models usually have been through instruction/preference training or fine-tuning. During this stage, they have learned to follow specific templates when inferring. For example, templates can require starting rounds of dialogue with a general prompt (called the `system prompt`) prefixed by specific tokens (usually `System: `). Said prompt is here to provide high-level instructions for the model, such as the contents of a persona, or general answering style instructions. Rounds of dialogue can also require adding prefix key words to text, such as `User` for queries and `Assistant` for answers.

When using few shot, you also need to select if you want examples to be provided multi-turn (mimicking user/assistant turns) or all at once (in a single user prompt).

Not following the chat template expected by the model at inference will kill its performance, as it will drive its output outside of the probability space it's been converging on.

### Few-shots samples
Two things are easy to mess up with few-shot samples (see `general-knowledge/Model inference` if you're unsure what it is).

Obviously, you need to use the **same number of few-shot samples** as your task of reference. 

However, you also need to use the **exact same samples** as the model you are comparing to, as using different samples will change results (which is not too surprising, if we assume some samples are better at expressing the task than others). More surprising maybe: you not only need to use the exact same samples, but also present them in the **exact same order**. Varying the order on the same samples led us to observe up to 3 points of difference on some subsets of MMLU (you can see [some results here](https://huggingface.co/blog/evaluation-structured-outputs) , it's the third colorgrid).

This is also a place where paying attention to the random seeds is important.

## Different generation parameters
For generative evaluations, parameters to pay attention to are:
- making sure you are using the **same end of sentence token**
- making sure you are allowing your model to **generate the same number of tokens** for the evaluation
- making sure, if using sampling, that you are using the **same seed/temperature parameters**

## Different model loading
Some sources of differences that we have observed are:
- using **different hardware**.
  Pytorch does not ensure reproducibility of non deterministic operations across hardware
- using **different libraries**.
  For example, if you use `transformers` vs `vllm` as your backend for inference, matrix computations are not managed exactly in the same way)
- using **different batch sizes**. 
  It's been documented in several evaluation libraries and model backends that using different batch sizes will change inference results - if you want fully reproducible evaluations, you should fix the batch size, though it might not always be possible for memory issues
- using **different loading precision** for your model weights.
  Using a lower precision can reduce memory and inference costs, but it will also change the numerical results, since you are using different versions of the weights.
