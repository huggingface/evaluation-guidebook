(originally published at : https://huggingface.co/blog/clefourrier/llm-evaluation)

# Let's talk about LLM evaluation

Since my team works on evaluation and leaderboards at Hugging Face, at ICLR 2024 (2 weeks ago) a lot of people wanted to pick my brain about the topic (which was very unexpected, thanks a lot to all who were interested). 

Thanks to all these discussions, I realized that a number of things that I take for granted evaluation wise are 1) not widely spread ideas 2) apparently interesting.

So let's share the conversation more broadly!

## How do we do LLM evaluation?

First, let's align on a couple definitions. There are, to my knowledge, at the moment, 3 main ways to do evaluation: automated benchmarking, using humans as judges, and using models as judges. Each approach has its own reason for existing, uses, and limitations.

### Benchmarks

Automated benchmarking usually works the following way: you'd like to know how well your model performs on something. This something can be a well-defined concrete **task**, such as *How well can my model classify spam from non spam emails?*, or a more abstract and general **capability**, such as *How good is my model at math?*.

From this, you construct an evaluation, usually made of two things:
- a collection of *samples*, given as input to the model to see what comes out as output, sometimes coupled with a reference (called gold) to compare with. Samples are usually designed to try to emulate what you want to test the model on: for example, if you are looking at email classification, you create a dataset of spam and non spam emails, try to include some hard edge cases, etc. For LLMs, the two main tasks are generation evaluation (comparing generated text with a reference after normalization), or multi-choice (compare the relative log-probabilities of possible continuations after a prompt).
- a *metric*, which is a way to compute a score for the model. For example, how accurately can your model classify spam (score of well classified sample = 1, badly classified = 0).

This is more interesting to do on data that was not included in the model training set, because you want to test if it **generalizes** well. You don't want a model which can only classify emails it has already "seen", that would not be very useful! 

Note: A model which can only predict well on its training data (and has not latently learnt more high-level general patterns) is said to be **overfitting**. In less extreme cases, you still want to test if your model is able to generalize to data patterns which were not in the training set's distribution (for example, classify spam emails about 'health' products after having seen only spam emails about fake banks).

This works quite well for very well-defined tasks, where performance is "easy" to assess and measure: when you are literally testing your model on spam classification, you can say "the model classified correctly n% of these samples". For LLMs benchmarks, some issues can arise, such as models [favoring specific choices based on the order in which they have been presented for multi-choice evaluations](https://arxiv.org/abs/2309.03882), and generative evaluations relying on normalisations which can easily [be unfair if not designed well](https://huggingface.co/blog/open-llm-leaderboard-drop), but overall they still provide signal at the task level.

For capabilities however, it's hard to decompose them into well-defined and precise tasks: what does "good at math" mean? good at arithmetic? at logic? able to reason on mathematical concepts?

In this case, people tend to do more "holistic" evaluations, by not decomposing the capability in actual tasks, but assuming that performance on general samples will be a **good proxy** for what we aim to measure. For example, GSM8K is made of actual high school math problems, which require a whole set of capabilities to solve. It also means that both failure and success are very hard to interpret. Some capabilities or topics, such as "is this model good at writing poetry?" or "are the model outputs helpful?" are even harder to evaluate with automatic metrics - and at the same time, models now seem to have more and more **generalist** capabilities, so we need to evaluate their abilities in a broader manner. (For example, there was a debate in the scientific community as to whether LLMs [can draw](https://arxiv.org/abs/2303.12712) unicorns [or not](https://twitter.com/DimitrisPapail/status/1719119242186871275). Most likely not at this point, but clearly an important point to investigate.)

Automatic benchmarks also tend to have another problem: once they are published publicly in plain text, they are very likely to end up (often accidentally) in the training datasets of models. Some benchmarks creators, like the authors of BigBench, have tried to mitigate this by adding a "canary string" (a very specific combination of characters) for people to look for, and remove from training sets, but not everybody is aware of the mechanism nor trying to do this removal. There is also a non negligible quantity of benchmarks, so looking for accidental copies of absolutely all of them in data is costly. Other options include providing benchmarks in an [encrypted form](https://arxiv.org/pdf/2309.16575), or behind a [gating system](https://huggingface.co/datasets/Idavidrein/gpqa). However, when evaluating closed models behind black box APIs, there is no guarantee that the provided data won’t be later used internally for training or fine-tuning. 

The case were an evaluation dataset ends up in the training set is called **contamination**, and a model which was contaminated will have a high benchmark performance that does not generalize well to the underlying task (an extensive description of contamination can be found [here](https://aclanthology.org/2023.findings-emnlp.722/), and here is a fun way to [detect it](https://arxiv.org/abs/2311.06233)). A way to address contamination is to run [**dynamic benchmarks**](https://arxiv.org/abs/2104.14337) (evaluations on datasets which are regularly refreshed to provide scores on systematically unseen new data), but this approach is costly in the long term.

### Human as a judge

A solution to both contamination and more open-ended evaluation is asking humans to evaluate model outputs.

This is usually done by tasking humans with first, prompting models, then, grading a model answer or ranking several outputs according to guidelines. Using humans as judges allows to study more complex tasks, with more flexibility than automated metrics. It also prevents most contamination cases, since the written prompts are (hopefully) new. Lastly, it correlates well with human preference, since this is literally what is evaluated!

Different approaches exist to evaluate models with humans in the loop.

**Vibes-checks** is the name given to manual evaluations done individually by some members of the community, usually on undisclosed prompts, to get an overall "feeling" of how well models perform on many use cases, which range from coding to quality of smut written. (I've also seen the term "canary-testing" used for this, in reference to high signal canary in a coalmine approach). Often shared on Twitter and Reddit, they mostly constitute anecdotal evidence, and tend to be highly sensitive to confirmation bias (in other words, people tend to find what they look for). However, some people have been trying to do more methodical vibe-checks evaluations; for example, the user *Wolfram Ravenwolf* shares his model comparisons findings in a very systematic way through blogs (see [here](https://huggingface.co/blog/wolfram/llm-comparison-test-llama-3) for an example).

Using community feedback to establish massive model rankings is what we call an **arena**. A well known example of this is the [LMSYS chatbot arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard), where community users are asked to chat with models until they find one is better than the other. Votes are then aggregated in an Elo ranking (a ranking of matches) to select which model is "the best". The obvious problem of such an approach is the high subjectivity - it's hard to enforce a consistent grading from many community members using broad guidelines, especially since annotators preferences tend to be [culturally bound](https://arxiv.org/abs/2404.16019v1) (with different people favoring different discussion topics, for example). One can hope that this effect is smoothed over by the sheer scale of the votes, through a "wisdom of the crowd" effect (this effect was found by a statistician named Galton, who observed that individual answers trying to estimate a numerical value, like the weight of a hog, could be modeled as a probability distribution centered around the actual answer).  

The last approach is **systematic annotations**, where you provide extremely specific guidelines to paid selected annotators, in order to remove as much as the subjectivity bias as possible (this is the approach used by [ScaleAI](https://scale.com/guides/data-labeling-annotation-guide#hight-quality-data-annotations), and most data annotation companies). However, it can get extremely expensive fast, as you have to keep on doing evaluations in a continuous and non automatic manner for every new model you want to evaluate, and it can still fall prey to human bias (this [study](https://arxiv.org/abs/2205.00501) showed that people with different identities tend to rate model answer toxicity very differently). 

Recent [work](https://arxiv.org/pdf/2309.16349) has also shown that human evaluators tend to estimate the quality of answers based on first impressions, instead of actual factuality or faithfulness. Crowdsourced annotators are notably very sensitive to tone, and underestimate the number of factual or logical errors in an assertive answer. In other terms, if a model says wrong things in a confident tone, human evaluators are much less likely to notice it, which could skew ratings towards the more assertive models. (Expert annotators are less likely to fall prey to these biases.) This kind of human bias was confirmed in another [paper](https://arxiv.org/pdf/2310.13548) : humans are most likely to prefer answers which appeal to their views or align with their opinions or errors, rather than answers which are factually correct. 

These biases are not unexpected, but they must be taken into account: not all use cases should rely on using human annotators, especially crowdsourced, unexpert ones - any task requiring factuality (such as code writing, evaluation of model knowledge, etc) should include another, more robust, type of evaluation to complete the benchmark.

### Model as a judge

To mitigate the cost of human annotators, some people have looked into using models or derived artifacts (preferably aligned with human preferences) to evaluate models' outputs. This approach is not new, as you can find techniques to measure summarization quality from [model embeddings](https://arxiv.org/abs/1904.09675) in 2019.

Two approach exist for grading: using [generalist, high capability models](https://arxiv.org/abs/2306.05685v4) or using [small specialist models](https://arxiv.org/pdf/2405.01535) trained specifically to discriminate from preference data. The former approach gives results well correlated with human preference, but most strong enough models tend to be closed source, therefore subject to change behind APIs, and uninterpretable.

LLM as judges have several strong limitations: they tend to [favor their own outputs](https://arxiv.org/abs/2404.13076) when scoring answers, are [bad at providing consistent score ranges](https://twitter.com/aparnadhinak/status/1748368364395721128) (though you can improve this with asking the model to explain its reasoning [before providing a score](https://twitter.com/seungonekim/status/1749289437165769177)), and are actually not that consistent [with human rankings](https://arxiv.org/pdf/2308.15812).

My main personal gripe with using models as judges is that they introduce very subtle and un-interpretable bias in the answer selection. I feel that, much like when crossbreeding too much in genetics studies, you end up with dysfunctional animals or plants, by using LLMs to select and train LLMs, we are just as likely to introduce minute changes that will have bigger repercussions a couple generations down the line. I believe this type of bias is less likely to occur in smaller and more specialized models as judges (such as toxicity classifiers), but this remains to be rigorously tested and proven.

## Why do we do LLM evaluation?

Now that we’ve seen how we do evaluation, what is it actually useful for?

I strongly believe that there are 3 main reasons for which people do evaluation, which tend to be conflated together, but are actually **very different**, and each answer a separate question.

### 1) Is my model training well? Is my training method sound? - Non-regression testing

**Non-regression testing** is a concept which comes from the software industry, to make sure small changes have not broken the overall approach.

The idea is the following: when you add a new feature to your software, or fix a problem in the code base, have you broken something else? That's what non-regression tests are for: making sure the expected, high-level behavior of your software is not suddenly broken by a (seemingly unrelated) change.

When you select a setup to train models, you want to test something very similar, and make sure that your changes (choosing different training data, architecture, parameters, etc) have not "broken" the expected performance for a model of these properties.

To give a concrete example, you would expect a 7B base LLM to get between 50 and 65 on (multiple choice) MMLU after training, and on the other hand, know that performance fluctuating between 20 and 30 indicates that no learning occurred.

For "non-regression" evaluation, you need to look at 1) evaluation scores **trajectories** (is the performance better now that when starting training), 2) evaluation scores **ranges** (is the performance within what's expected). You actually... don't care about the precise score themselves!

This evaluation is therefore not here to tell you anything about actual model capabilities, but instead just here to confirm that your training approach is "as sound" as the other training approach, and that your model behaves in similar ways. I believe that even some evaluations simply looking at changes in the perplexity (probabilities) of text could be sufficient for this step, but you usually want benchmarks which have a high "signal to noise" ratio, or in other words, you want to make sure that a big change in the score reflects a big shift in your model.

### 2) Which model is the best? Is my model better than your model? - Leaderboards and rankings

The next role of evaluation is simply to sort models to find and select the best architectures and approaches overall. If you have a leaderboard, take the best model, and it's not working on your use case, it's unlikely the next best model will work. In [their paper](https://arxiv.org/pdf/2404.02112) about lessons learned on benchmarking and dataset design from the ImageNet era, the authors argue that, since scores are susceptible to instability, the only robust way to evaluate models is through rankings, and more specifically by finding broad groups of evaluations which provide consistent and stable rankings.

I believe looking for ranking stability is indeed an extremely interesting approach to model benchmarking, as we have shown that LLMs *scores* on automated benchmarks are extremely susceptible to [minute changes in prompting](https://huggingface.co/blog/evaluation-structured-outputs), and that human evaluations are not more consistent - where *rankings* are actually more stable when using robust evaluation methods. 

If scores, by themselves, are not that relevant, could using the relative ordering of models tell us something of value instead?

In the related ICLR 2024 plenary of evaluation, Moritz Hardt compared adding perturbations to the Open LLM Leaderboard (through minuscule score modification, well within score ranges) and on the Chatbot Arena (through adding a bad contender to the arena to see how it affected the Elo rankings). Neither these benchmarks provide stable and consistent rankings at the moment. We'll be sure to explore this aspect with future versions of the Open LLM Leaderboard!

### 3) Where are we, as a field, in terms of model capabilities? Can my model do X?

"How do you know if models can do X?" is a question which comes up a lot, and I think it is a very valid one.

However, for any complex capability, **we cannot at the moment just say "this model is the best at this", but instead "this model is the best on this task that we hope is a good proxy for this capability, without any guarantee"**. 

We are strongly missing any kind of good definitions and framework on what a capability is for a machine learning model, especially for those surrounding reasoning and mind theory. However, this is not specific to machine learning! In human and animal studies, it is also quite hard to define what constitutes a "capability", and metrics which try to provide precise scores (IQ and EQ for example) are hotly debated and controversial, with reason.

We might want to look at social sciences to think about evaluation of capabilities, as in these fields, people are used to thinking seriously about confounding factors in data gathering and analysis. However, I also believe it likely that 1) we cannot define these broad capabilities at all, since we cannot define them in humans and animals at the moment, 2) frameworks made with the human (or animal) in mind will not transfer well to models, as the underlying behaviors and assumptions are not the same.

## Conclusion

LLM evaluation is nowadays done in the following manner:
Using automatic benchmarks, affected by contamination and lack of “generalness” (the latter not necessarily being a bad thing, as specialized evaluations are interesting)
Using human evaluations, which tends to suffer from lack of reproducibility at a small scale, and psychological biases overall (such as preference for sycophantic answers), though one can hope some of the biases get smoothed over at a high scale
Using models as judges, which has very subtle biases when evaluating, likely to be unnoticed but introduce perturbations downstream.
  
However, all is not lost: evaluation, within its limits, is still able to provide some signal on which new training methods or datasets sound promising or not, both from looking at how performance falls within expected ranges (non-regression testing), and at how models are ranked overall (with stable enough evaluations). We can also hope that combining enough data points across topics and tasks will provide us with enough signal to get an idea of overall model performance, without however assuming anything about more “general” capabilities. 

Contrary to hype, we cannot really evaluate “general model capabilities” at the moment, first and foremost because we have not defined what that means. However, LLM evaluation, as a research field, is very much in its infancy at the moment, and there is a lot to be done, which is very exciting! Inspiration can be grabbed from many fields, from machine learning [interpretability](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html) to sociology, in order to define new metrics and tasks. Interdisciplinary work will likely open very new cool directions for the field!

## Acknowledgements
Many thanks to all the cool people interested in talked about evaluation at the conference, including but not limited to Summer Yue (Scale AI), Moritz Hardt (Max Planck Institute), Luca Soldaini and Ian Magnusson (Allen AI), Ludwig Schmidt (Anthropic), Max Bartolo (Cohere), Maxime Labonne (Liquid AI), François Charton (Meta), Alan Cooney (UK AI Safety Institute) and Max Ryabinin (Together AI).

Many thanks also to Yacine Jernite and Irene Solaiman from Hugging Face for their valuable feedback on this document. 

And last but not least, thanks to the evaluation and leaderboards team at Hugging Face, notably Nathan Habib, for the discussions and work we’ve been doing together!
