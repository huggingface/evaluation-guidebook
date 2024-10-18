# What about Reward Models?

## What is a Reward Model?

Reward models learn to predict a score from human annotations for given prompt/completion pairs. The end goal is for them to do predictions aligned with human preference. 
Once trained, these models can then be used to improve other models, by acting as a a reward function which is a proxy for human judgment.

### Pairwise score

The most common type of reward model is the Bradley-Terry model, which outputs a single score, following:

$$p(\text{completion b is better than completion a}) = \text{sigmoid}(\text{score}_b - \text{score}_a)$$

This model is trained using only pairwise comparisons of completions, which are easier to collect than scores, but can only compare several completions for one prompt, and not completions across prompts.

Other models have expanded on this approach to predict a more nuanced probability that a completion is better than the other one ([example](https://huggingface.co/RLHFlow/pair-preference-model-LLaMA3-8B)). 

This allows them to (theoretically) judge subtle differences between completions, at the cost of not being able to easily save and compare many different scores across prompts for the same test set. In addition, context length and memory limits can become an issue when comparing too long completions.

### Absolute score

Some reward models such as [SteerLM](https://arxiv.org/abs/2311.09528) output absolute scores, which can be used to evaluate completions directly without the need for pairwise comparisions. These models can be easier to use for evaluation, but are also harder to collect data for, as absolute scores tend to be less stable than pairwise scores in human preferences. 

More recently, models have been proposed that output both absolute and relative scores, such as [HelpSteer2-Preference](https://arxiv.org/abs/2410.01257) and [ArmoRM](https://arxiv.org/abs/2406.12845).


## How do I use a Reward Model for Evaluation?

Given a dataset of prompts, we can generate completions from a language model and ask a reward model to score them.

For models that give absolute scores, the resulting scores can be averaged to get a reasonable summary score.

However, in the more common case of relative scores, the average reward can be biased by outliers (a few very good or very bad completions) as different prompts may have inherently different reward scales (some prompts are way harder or easier than others).

Instead, we can use 
- win rates: take a reference set of completions and calculate the percentage of completions from the model that are ranked higher than the reference completions. It is slightly more granular. 
- win probabilities: the mean probability of the completions being better than the reference completions, which can give a more fine-grained and smoothly changing signal.

## Pros and Cons of Reward Models

Reward models are typically:
- **Very fast**: Getting a score is as simple as running a forward pass of a relatively small model once (since we only get a score, and not long text, contrary to judge-LLMs)
- **Deterministic**: The same scores will be reproduced through the same forward pass
- **Unlikely to suffer from positional bias**: As most models take only one completion, they can not be influenced by the order. For pairwise models, positional bias is often also minimal, as long as the training data was balanced with respect to containing both first and second answers as being the best.
- **Require no prompt engineering**: since the model will simply output a score from one or two completions depending on preference data it's been trained on.

On the other hand they:
- **Require specific fine-tuning**: This can be a relatively costly step, and elthough they inherit many capabilities from a base model, they may still perform poorly on tasks that are out of the training distribution.
- **Loose efficiency when used both in reinforcement learning and evaluation** (or when using direct alignment algorithms on datasets that are similar to the training data of the reward model), as the language model may overfit to the reward model's preferences.

## Tips and Tricks for using Reward Models for Evaluation

- A good place to find high performing models is the [RewardBench Leaderboard](https://huggingface.co/spaces/allenai/reward-bench).
- You can look at how reward models have been used in the [Nemotron](https://arxiv.org/abs/2406.11704) paper. 
- For reward models that rate single prompts and completions, you can cache the scores of many reference models and easily see how a new model performs.
- Tracking of win rates or probabilities over training, e.g. as in [this](https://arxiv.org/abs/2410.11677v1) recent paper, can allow you to detect model degradation and select optimal checkpoints.
