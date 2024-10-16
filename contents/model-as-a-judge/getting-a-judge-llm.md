# Getting a Judge-LLM

When using an existing LLM, you can go for [generalist, high capability models](https://arxiv.org/abs/2306.05685v4),  using [small specialist models](https://arxiv.org/pdf/2405.01535) trained specifically to discriminate from preference data, or training your own.

## Using a generalist LLM

With the introduction of more capable LLMs (such as ChatGPT), some researchers started exploring using big models as judges. The best current big model judges tend to be closed source models (like Claude or gpt-o models) though the gap with open source is closing very fast thanks to high quality models such as [Qwen 2.5](https://huggingface.co/collections/Qwen/qwen25-66e81a666513e518adb90d9e), [Command R+](https://huggingface.co/CohereForAI/c4ai-command-r-plus-08-2024) or [Llama 3.1-405-Instruct](meta-llama/Llama-3.1-405B-Instruct). 

Closed source models, despite their performance, present the multiple disadvantages of being:
- under APIs, which mean that models (therefore results) can change with no notice, hurting the reproducibility of evals
- black boxes, which makes them un-interpretable
- possible sources of data leakage/lack of data privacy, as you send your data to a third party through the internet (which tends to be less safe than locally managed data), and you don't know for certain what is done with it (you often need to opt out of it being used in training sets).

However, they also allow anyone to have access to a high quality model without needing to setup things locally or requiring access to hardware. This pros are now also present for most high quality open models, which are accessible through model providers, and solve the first 2 problems above.

You'll find a good cost analysis of model providers [here](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard) if you need help picking one.

## Using a tiny specialized LLM judge model

You can also make the choice to use tiny specialized LLM judges. With often a couple billion parameters, they can run locally on most recent consumer hardware, while being trained from scratch or fine-tuned using instruction data. You often need to follow their specific prompt formats.

Some existing models:
- Flow-Judge-v0.1 ([weights](https://huggingface.co/collections/flowaicom/flow-judge-v01-66e6af5fc3b3a128bde07dec)), 3.8B parameters, a Phi-3.5-mini-instruct fine-tuned on a synthetic preference dataset
- Prometheus ([weights](https://huggingface.co/prometheus-eval/prometheus-13b-v1.0), [paper](https://arxiv.org/abs/2310.08491)), 13B parameters, a model trained from scratch on synthetic preference dataset. A 7B parameter [v2](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0) also exists, a Mistral-7B-Instruct-v0.2 fine-tune on a bigger synthetic preference dataset, with added weight merging
- JudgeLM ([paper](https://arxiv.org/pdf/2310.17631)), 7B to 33B parameters, models trained from scratch on synthetic preference datasets generated with a variety of models.

## Training your own
You can also make the choice to train or fine-tune your own LLM-as-judge.

You first need to gather preference data for your task of interest, which can come
- From existing [human preference datasets](https://www.kaggle.com/competitions/lmsys-chatbot-arena)
- From model generated preference data (which you can generate following the above tiny-model judges papers data sections, or get directly, for example from the Prometheus [preference](https://huggingface.co/datasets/prometheus-eval/Preference-Collection) and [feedback](https://huggingface.co/datasets/prometheus-eval/Feedback-Collection) collections).

Then you need to decide whether to start from a small model to train from scratch, or from an existing model, that you can 
- distill into a new smaller model
- quantize.
- then fine-tune (using peft or adapter weights if the model is big and your training compute low) using the above data
	- apparently [starting from a reward model works better than from an instruct model](https://x.com/dk21/status/1826292289930674590)
