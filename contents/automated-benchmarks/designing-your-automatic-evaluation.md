# Designing your automatic evaluation

## Choosing a dataset
For your evaluation, you can either select an existing dataset (see [Some evaluation datasets](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/some-evaluation-datasets.md) for examples) or design your own. Through this process, it's very important to keep in mind that **your evaluation result will only be as good as your evaluation dataset**.

### Selecting an existing dataset
You must imperatively look at its components.
#### Creation process
- **Who created the actual samples?** 
Imo, expert created dataset > paid annotator dataset ~ crowdsourced dataset > MTurked dataset.
You also want to look for a data card, where you'll find annotator demographics - this can be important to understand the dataset language diversity.

- **Were they all examined by other annotators or by the authors?** 
You want to know: 
	- if the inter-annotator score on samples is high (= are annotators in agreement?)
	- and/or if the full dataset has been examined by the authors.
This is especially important for datasets with the help of underpaid annotators who usually are not native speakers of your target language (think AWS Mechanical Turk), as you might otherwise find typos/grammatical errors/nonsensical answers.

- **Were the annotators provided with clear data creation guidelines?**
In other words, is your dataset consistent?

#### Samples 
Take 50 random samples and manually inspect them:
- *For quality*:
	- are the prompts clear and unambiguous? 
	- are the answers correct? (*Eg: TriviaQA contains several gold answers (aliases field) per question, sometimes conflicting.*)
	- is information missing? (*Eg: MMLU misses reference schematics in a number of questions.*)
- *For relevance to your task*:
	- are these questions the kind of questions you want to evaluate an LLM on?
	- are these examples relevant to your use case?

You also want to know how many samples are present there (to make sure results are statistically significant - 100 samples is usually a minimum for automatic benchmarks).
### Designing your own
You can go 3 ways when designing your own dataset. 
#### Aggregating existing data
You can aggregate existing data from different sources, evaluating a relevant capability for your task. A number of evaluation datasets are for example constructed from aggregating human evaluation datasets (such as MATH, LSAT, etc). In this case, follow the steps above.
#### Using human annotators
There's a whole section on using human annotators in `Human evaluation`, see [Using human annotators](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/using-human-annotators.md).
#### Using synthetic data
- **Using LLMs**
On this, you can check the very cool [Cosmopedia](https://huggingface.co/blog/cosmopedia) blog by cool HF colleagues! It's mostly studying how to create a synthetic training dataset, but similar techniques can be used for evaluation. 
Make sure to manually check/filter/inspect your dataset afterwards (following the above steps).

- **Using rule-based techniques**
If your task allows, this is a very good way to get a virtually infinite supply of samples and avoid contamination! 
For some examples, you can look at [NPHardEval](https://arxiv.org/abs/2312.14890), [DyVal](https://arxiv.org/abs/2309.17167), [MuSR](https://arxiv.org/abs/2310.16049), [BabiQA](https://arxiv.org/abs/1502.05698), etc.

## Choosing an inference method
You'll need to choose what kind of inference method you need.

Using log-probabilities (MCQA, multi-choice question answer) is very good for multiple choice question answers (usually to test model knowledge, or ability to disambiguate). 
- Pros: 
	- Makes sure that all models have access to the correct answer
	- Provides a proxy for model "confidence" (and calibration)
	- Fast to evaluate, especially when we ask the model to predict only one token (A/B/C/D the indices of the choices, or Yes/No, etc).
	- Allow to get signal on small models' task performance 
- Cons: 
	- Slightly over-scores small models which would have generated something outside of the range of available choices if given free rein.
	- Some models [favor specific choices based on the order in which they have been presented](https://arxiv.org/abs/2309.03882), which could lead to unrepresentative evaluations

Using generations (QA, question answering) is very good for any task where you want to test fluency, reasoning, or the ability of your model to actually answer questions.
- Pros:
	- Should actually correlates with LLM ability to generate fluent text, will most of the time be what people are actually interested in
- Cons:
	- Can be harder to score (see the `metrics` section below)
	- Usually slightly more expensive than log likelihood evaluations, especially if they include sampling

## Choosing a prompt
The prompt is going to define:
- how much information is given to your model about the task
- how this information is presented to your model.

A prompt for a general MCQA or QA is usually made of some of the following:
- a task prompt (optional): introduces your task.
- a context: provides additional context for your question.
	- *Eg: For a summarization or information extraction task, you could provide a content source*
- a question: the actual core of your prompt.
- in case of a multi choice evaluation, you can add options
- connector words (`Question`, `Context`, `Choice`, ...)

When defining your prompt, you need to be aware that:
- even small changes in semantically equivalent prompts can make the results vary by quite a lot (see Section `Different prompt` in [Troubleshooting reproducibility](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/troubleshooting/troubleshooting-reproducibility.md)), and prompt formats might advantage or disadvantage specific models
	- How to mitigate this: 
		- A costly way is to re-run the evaluation several times with prompt variations
		- A less costly way is to run your evaluation once using a range of prompt formats allocated to different samples of equivalent difficulty
- you can provide examples to your model to help it follow the expected format (using few-shot examples), and adding connector words helps this overall
- but models now tend to overfit specific prompt formats. 
	- [This paper](https://arxiv.org/abs/2407.07890) is great on the topic, showing notably how some models can be over-evaluated because they have overfitted the test set **format**
	- On the Open LLM Leaderboard 2, we've notably observed that Llama 3.2 and Qwen 2.5 are no longer following the format of the prompt provided in a few-shot setup for this reason.
- for a number of metrics, you want a very constrained generation or output. 
  *You can learn more about this in the `Constraining model outputs` section of the [Model inference and evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/model-inference-and-evaluation.md) page.*

## Choosing a metric
If you are looking at **log-probabilities**, your metrics are going to be easy: you'll want to look at accuracy (how often the most likely choice is the best choice). It's important to normalize it by length (either character, token, or pmi). You could also look at perplexity, recall, or f1 score.

For **generative** evaluations, your range of metrics is going to be wider. 
You'll need to 
1. decide if you compare generations as they are, or first normalize them with something. 
	- Normalizations can easily [be unfair if not designed well](https://huggingface.co/blog/open-llm-leaderboard-drop), but overall they still provide signal at the task level.
	- They are very important for specific tasks, such as math evaluations, where you might want to extract your result from formatted outputs.
	- They will also be important if you want to evaluate with added mechanisms for accuracy, such as Chain of Thought, as you'll need to remove the reasoning trace from the actual result
2. decide how you compare the generation with the reference. 
   You could use anything ranging from match-based metrics (exact match, prefix match, etc) to summarization and translation metrics (ROUGE, BLEU, character n gram comparisons). For a list of existing metrics, you can look [here](https://github.com/huggingface/lighteval/wiki/Metric-List), I'll add a section later on which metric to use when.

More generally, when picking your metric, you need to keep in mind what your task is really about. For some domains (ex: medical, chatbots with public interaction), you don't want to measure the average performance, but need a way to evaluate the **worst performance** you'll get (on medical quality of output, on toxicity, etc). (*To go further, take a look at this [blog](https://ehudreiter.com/2024/07/10/challenges-in-evaluating-llms/)*)

## Smart new tasks: what about functional testing?
In the field of code, you want to evaluate generated programs not only on their semantics, but on their actual function. A good way to do so is therefore to check if code generated to follow a prompt passes correctly a suite of unit-tests designed to fit the task.

This functionality approach is extremely promising, as it 
- allows to generate test cases more easily (in many cases, you can generate rule-based test cases)
- therefore reducing overfitting
- tests models on specific active capabilities

It's however an approach which requires creativity to be translated to text! 

A good example of this is IFEval, an evaluation benchmark which tests if models can follow instructions. It works by creating a number of formatting instructions (*Add this number of bullet points. Capitalize only one sentence.* etc), and strictly testing if the format is followed. More work is clearly needed to extend this idea to other features of text to analyze!
