
# Reward Model Based Evaluation

Reward models are a type of model that outputs a reward score for a given prompt and completion.
They are often used in the context of reinforcement learning, where the goal is to maximize the reward signal.

A good place to find high performing models is the [RewardBench Leaderboard](https://huggingface.co/spaces/allenai/reward-bench).

## Bradley-Terry models

The most common type is a so-called Bradley-Terry model, which outputs a single score with the following interpretation:

$$p(\text{completion b is better than completion a}) = \text{sigmoid}(\text{score}_b - \text{score}_a)$$

As these models are trained only on comparisons, it is important to keep in mind that a scores between different prompts can never be compared,
 as they can be arbitrarily offset.

## Evaluation using reward models

Given a dataset of prompts, we can generate completions from a model and ask a reward model to score these.
Although the average reward can be a valid metric to look at,
 it can be biased by a few very good or very bad completions,
  as different prompts may have different scales of rewards due to being easier or harder to evaluate.

Instead, we can take a reference set of completions and calculate the percentage of completions from the model that are ranked higher than the reference completions.
Another useful metric is the mean probability of the completions being better than the reference completions, which can give a more fine-grained and smoothly changing signal.

## Other types of reward models

Some reward models output one or more absolute scores, which can be used to evaluate the model directly without the need for pairs.
These models can be easier to use for evaluation, but are also harder to collect data for.

Another type of reward model are pair-wise models, which output a single score for a pair of completions.
These models have the advantage of being able to judge subtle differences between completions, 
 but at the cost of not being able to easily save and compare scores.

## Pros and cons of reward models

Reward models are typically very fast, as getting a score is as simple as running a forward pass of the model.
The scores they give are also deterministic, have no position bias, and no prompt engineering is needed to generate scores.

On the other hand they need to be fine-tuned separately, and although they inherit many capabilities from a base model, they may still perform poorly on tasks that are not in the training distribution.
In addition, the usefulness of reward model-based evaluation decreases when the same model is also used in reinforcement learning, or when using direct alignment algorithms on datasets that are similar to the training data of the reward model, as the model may overfit to the reward model's preferences.







