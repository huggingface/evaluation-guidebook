# Basics

## What is human evaluation?
Human evaluation is simply asking humans to evaluate models. 
In this document, we'll look at post-hoc evaluation: your model has been trained, you have a given task in mind, and humans are providing scores.

### Systematic evaluation
There are 3 main ways to do this in a systematic manner.

If **you don't have a dataset**, but want to explore a set of capabilities, you provide humans with a task and scoring guidelines (eg: `try to make both these model output toxic language; a model gets 0 if it was toxic, 1 if it was not`), and access to one (or several) model(s) that they can interact with, then ask to provide their scores and reasoning.

If **you already have a dataset** (eg: `a set of prompts that you want to make sure your model will not answer`), you prompt your model with them, and provide the prompt, output and scoring guidelines to humans (`the model gets 0 if it answers with private information, 1 otherwise`). 

Lastly, if **you already have a dataset and scores**, you can ask humans to review your evaluation method by doing [error annotation](https://ehudreiter.com/2022/06/01/error-annotations-to-evaluate/) (*it can also be used as a scoring system in the above category*). It's a very important step of testing new evaluation system, but it technically falls under evaluating an evaluation, so it's slightly out of scope here.

Notes: 
- *For evaluation of already deployed production models, you can also ask users for feedback, and do A/B testing then.*
- *[AI audits](https://arxiv.org/pdf/2401.14462) (external systematic evaluation of models) are usually human based, but out of scope for this document.

### Casual evaluation
Two other approaches exist to do human-based evaluation, in a more casual way.

**Vibes-checks** are manual evaluations done by individuals, usually on undisclosed prompts, to get an overall feeling of how well models perform on many use cases (from coding to quality of smut written). Often shared on Twitter and Reddit, results mostly constitute anecdotal evidence, and tend to be highly sensitive to confirmation bias (in other words, people tend to find what they look for). However, they can be [good starting point for your own use cases](https://olshansky.substack.com/p/vibe-checks-are-all-you-need).

**Arenas** are crowdsourced human evaluation to rank models. 
A well known example of this is the [LMSYS chatbot arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard), where community users are asked to chat with models until they find one is better than the other. Votes are then aggregated in an Elo ranking (a ranking of matches) to select which model is "the best". 
## Pros and cons of human evaluation

Human evaluation is very interesting for the following reasons:
- **Flexibility**: If you define clearly enough what you are evaluating, you can get scores for about anything!
- **Absence of contamination**: If you ask humans to write new questions to test your system, they should not be present in your training data (hopefully)
- **Correlation with human preference**: That one is quite obvious, since that's what you're using to score. 
  *Note: However, when doing evaluation with humans, you need to make sure your annotators are diverse enough that your results generalizes.*

However, it also present a number of limitations:
- **First impressions bias**: Human evaluators tend to estimate the quality of answers [based on first impressions](https://arxiv.org/pdf/2309.16349), instead of actual factuality or faithfulness. 
- **Tone bias**: Crowdsourced annotators are notably very sensitive to tone, and underestimate the number of factual or logical errors in an assertive answer. In other terms, if a model says wrong things in a confident tone, human evaluators are much less likely to notice it, which could skew ratings towards the more assertive models. (Expert annotators are less likely to fall prey to these biases.) 
- **Self-preference bias**: Humans are [most likely to prefer answers which appeal to their views or align with their opinions or errors](https://arxiv.org/pdf/2310.13548), rather than answers which are factually correct.
- **Identity bias**: People with different identities tend to have different values, and rate model answers very differently (for example on [toxicity](https://arxiv.org/abs/2205.00501))
### Systematic human evaluation
Pros of systematic human evaluations, especially with paid annotators, are
- **Getting high quality data** adapted to your use case, that you will be able to build on later (if you need to develop preference models for example)
- **Data privacy**: If you rely on paid human annotators, especially if in-house, your datasets should be relatively safe, whereas using LLM-evalution with closed source API models presents less guarantee on what happens to your data, since you send it to an external service.
- **Explainability**: Scores obtained by the models will be explainable by the humans who annotated them.

Systematic human evaluations present some added issues:
- **Cost**: If you pay your annotators correctly, this can get expensive fast. It's also likely you'll need rounds of iterative evaluation so that you can refine your guidelines, which adds to the cost.
- **Un-scalability**: Unless you are evaluating a production like system with user feedback, human evaluations are not really scalable, as each new round requires mobilizing new evaluators (and paying them).
- **Lack of reproducibility**: Unless you keep the exact same annotators continuously and your guidelines are perfectly unambiguous, it's likely some evaluations are going to be hard to reproduce precisely.

### Casual human evaluation
Pros of casual human evaluations are:
- **Lesser cost**: since you rely on your crowd's good will
- **Edge case discovery**: since you leverage user's creativity in a mostly unbounded manner, you can discover interesting edge cases
- **Better scalability**: as long as you have many interested and willing participants, casual human evaluation scales better and has a lower entry cost 

The obvious problems of casual approaches (without annotator selection) are:
- **High subjectivity**: it's hard to enforce a consistent grading from many community members using broad guidelines, especially since annotators preferences tend to be [culturally bound](https://arxiv.org/abs/2404.16019v1). One can hope that these effect is smoothed over by the sheer scale of the votes, through a "wisdom of the crowd" effect (see Galton's wikipedia page).
- **Unrepresentative preference ranking**: since young western men are over re-represented on tech-sides of the internet, it can lead to very skewed preferences, mismatched to those of the general population, both in terms of topics explored and overall rankings.
- **Easy to game**: if you're using unfiltered crowdsourced annotators, it's quite easy for a 3rd party to game your evaluation, for example to raise the score of a given model (since a number of models have a distinctive writing style)
