# Basics

## What is a judge model evaluation?
Judge models are simply **neural network used to evaluate the output of other neural networks**. In most cases, they evaluate text generations. 

Judge models range from small specialized classifiers (think "spam filter", but for toxicity for example) to LLMs, either large and generalist or small and specialized. In the latter case, when using an LLM as a judge, you give it a prompt to explain how to score models (ex: `Score the fluency from 0 to 5, 0 being completely un-understandable, ...`). 

Model as judges allow to score text on complex and nuanced properties. 
For example, an exact match between a prediction and reference can allow you to test if a model predicted the correct fact or number, but assessing more open-ended empirical capabilities (like fluency, poetry quality, or faithfulness to an input) requires more complex evaluators. 

That's where models as judges come into play. 

They are used on 3 main tasks:
- *Scoring a model generation*, on a provided scale, to assess a property of the text (fluency, toxicity, coherence, persuasiveness, etc).
- *Pairwise scoring*: comparing a pair model outputs to pick the best text with respect to a given property
- *Computing the similarity* between a model output and a reference 

*Note: In this document, I'll focus on the LLMs + prompt approach for now, but you should definitely check out how classifier judges work, as I think it can be fairly robust and well adapted to a number of use cases, and the recently introduced and promising reward model as judge approach (introduced in [this tech report](https://research.nvidia.com/publication/2024-06_nemotron-4-340b), and on which we have a small page [here](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/What%20about%20Reward%20Models.md))*

## Pros and cons of using judge-LLMs
Judge LLMs have been used for the following points:
- **Objectivity** when compared to humans: They automate empirical judgments in an objective and reproducible manner
- **Scale and reproducibility**: They are more scalable than human annotators, which allows to reproduce scoring on large amounts of data.
- **Cost**: They are cheap to instantiate, as they don't require to train a new model, and can just rely on good prompting and an existing high quality LLM. They are also cheaper than paying actual human annotators.
- **Alignment with human judgments**: They are somehow correlated with human judgments.

There are also downside to all of these:
- LLM as judges seem objective, but they have many **hidden biases** that can be harder to detect than the ones in humans, since we're not as actively looking for them (see [model-as-a-judge/Tips and tricks]). Besides, there are ways to reduce human bias by designing survey questions in specific and statistically robust ways (which has been studied in sociology for about a century), where LLM-prompting is not as robust yet. Using LLMs to evaluate LLMs has been compared to creating an echo-chamber effect, by reinforcing biases subtly.
- They are indeed scalable, but contribute to creating massive amounts of data which themselves need to be examined to ensure their quality (for example, you can improve the quality of LLM-judges by asking them to generate a thinking trace, or reasoning around their data, which makes even more new artificial data to analyse)
- They are indeed cheap to instantiate, but paying actual expert human annotators is likely to give you qualitatively better results for your specific use cases.

## How to start?
- If you want to give it a go, I suggest first reading this [very good guide](https://huggingface.co/learn/cookbook/en/llm_judge) (⭐) by Aymeric Roucher on how to setup your first LLM as judge!
- You can also try the [distilabel](https://distilabel.argilla.io/latest/) library, which has specific tasks to use LLMs as a judge. They have a nice [tutorial](https://distilabel.argilla.io/latest/sections/pipeline_samples/papers/ultrafeedback/) applying the methodology of the [Ultrafeedback paper](https://arxiv.org/abs/2310.01377).