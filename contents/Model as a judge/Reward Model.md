# Reward Model Based Evaluation

## What is a Reward Model?

Reward models are a type of model that outputs a reward score for a given prompt and completion.
They are often used in the context of Reinforcement Learning (RL), where the goal is to maximize the reward signal.

The most common type of Reward Model is the so-called Bradley-Terry model, which outputs a single score with the following interpretation:

$$p(\text{completion b is better than completion a}) = \text{sigmoid}(\text{score}_b - \text{score}_a)$$

This model has the advantage of requiring only pairwise comparisons, which are easier to collect.
However, as these models are trained only on comparisons, it is important to keep in mind that scores across different prompts should not be compared,
 as they can be arbitrarily offset.

Some reward models such as [SteerLM](https://arxiv.org/abs/2311.09528) output one or more absolute scores, which can be used to evaluate the model directly without the need for paired completions.
These models can be easier to use for evaluation, but are also harder to collect data for. 
More recently models have been proposed that output both absolute and relative scores, such as [HelpSteer2-Preference](https://arxiv.org/abs/2410.01257) and [ArmoRM](https://arxiv.org/abs/2406.12845).

Another type of reward model is a pair-wise model, which output a single score for a pair of completions ([example](https://huggingface.co/RLHFlow/pair-preference-model-LLaMA3-8B)).
These models have the advantage of being able to judge subtle differences between completions (at least in theory), 
 but at the cost of not being able to easily save and compare many different scores for the same test set.
In addition, context length and memory limits can become an issue when comparing two long completions.

## How do I use a Reward Model for Evaluation?

Given a dataset of prompts, we can generate completions from a language model and ask a Reward Model to score these.

For models that give absolute scores, the resulting scores can be averaged to get a reasonable summary score.

However, in the more common case of relative scores, 
 although the average reward can be a valid metric to look at,
  it can often be biased by a few very good or very bad completions,
   as different prompts may have different reward scales due to them being easier or harder to evaluate.

Instead, we can take a reference set of completions and calculate the percentage of completions from the model that are ranked higher than the reference completions.
Another useful metric is the mean probability of the completions being better than the reference completions, which can give a more fine-grained and smoothly changing signal.

## Pros and Cons of Reward Models

Reward models are typically very fast, as getting a score is as simple as running a forward pass of the model.
The scores they give are also deterministic, have no position bias, and no prompt engineering is needed to generate scores.

On the other hand they need to be fine-tuned separately, and although they inherit many capabilities from a base model, they may still perform poorly on tasks that are out of the training distribution.
In addition, the usefulness of reward model-based evaluation decreases when the same model is also used in reinforcement learning, 
 or when using direct alignment algorithms on datasets that are similar to the training data of the reward model, as the language model may overfit to the reward model's preferences.

## Tips and Tricks for using Reward Models for Evaluation

* A good place to find high performing models is the [RewardBench Leaderboard](https://huggingface.co/spaces/allenai/reward-bench).
* For reward models that rate single prompts and completions, you can cache the scores of many reference models and easily see how a new model performs.

