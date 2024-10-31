# The LLM Evaluation guidebook ⚖️

If you've ever wondered how to make sure an LLM performs well on your specific task, this guide is for you! 
It covers the different ways you can evaluate a model, guides on designing your own evaluations, and tips and tricks from practical experience.

Whether working with production models, a researcher or a hobbyist, I hope you'll find what you need; and if not, open an issue (to suggest ameliorations or missing resources) and I'll complete the guide!

## How to read this guide
- **Beginner user**: 
  If you don't know anything about evaluation, you should start by the  `Basics` sections in each chapter before diving deeper. 
  You'll also find explanations to support you about important LLM topics in `General knowledge`: for example, how model inference works and what tokenization is.
- **Advanced user**:
  The more practical sections are the `Tips and Tricks` ones, and `Troubleshooting` chapter. You'll also find interesting things in the `Designing` sections.

In text, links prefixed by ⭐ are links I really enjoyed and recommend reading.

## Table of contents
If you want an intro on the topic, you can read this [blog](https://huggingface.co/blog/clefourrier/llm-evaluation) on how and why we do evaluation!

### Automatic benchmarks
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/basics.md)
- [Designing your automatic evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/designing-your-automatic-evaluation.md)
- [Some evaluation datasets](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/some-evaluation-datasets.md)
- [Tips and tricks](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/tips-and-tricks.md)

### Human evaluation
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/basics.md)
- [Using human annotators](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/using-human-annotators.md)
- [Tips and tricks](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/human-evaluation/tips-and-tricks.md)

### LLM-as-a-judge
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/basics.md)
- [Getting a Judge-LLM](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/getting-a-judge-llm.md)
- [Designing your evaluation prompt](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/designing-your-evaluation-prompt.md)
- [Evaluating your evaluator](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/evaluating-your-evaluator.md)
- [What about reward models](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/what-about-reward-models.md)
- [Tips and tricks](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/model-as-a-judge/tips-and-tricks.md)

### Troubleshooting
The most densely practical part of this guide. 
- [Troubleshooting inference](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/troubleshooting/troubleshooting-inference.md)
- [Troubleshooting reproducibility](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/troubleshooting/troubleshooting-reproducibility.md)

### General knowledge
These are mostly beginner guides to LLM basics, but will still contain some tips and cool references! 
If you're an advanced user, I suggest skimming to the `Going further` sections.
- [Model inference and evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/model-inference-and-evaluation.md)
- [Tokenization](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/general-knowledge/tokenization.md)

### Examples
You'll also find examples as jupyter notebooks, to get a more hands on experience of evaluation if that's how you learn!
- [Comparing task formulations during evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/examples/comparing_task_formulations.ipynb): This notebook walks you through how to define prompt variations for a single task, run the evaluations, and analyse the results.  

## Planned next articles
- contents/automated-benchmarks/Metrics -> Description of automatic metrics
- contents/Introduction: Why do we need to do evaluation?
- contents/Thinking about evaluation: What are the high level things you always need to consider when building your task?
- contents/Troubleshooting/Troubleshooting ranking: Why comparing models is hard

## Resources
Links I like
- [About evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20evaluation.md)
- [About NLP](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20NLP.md)

## Thanks
This guide has been heavily inspired by the [ML Engineering Guidebook](https://github.com/stas00/ml-engineering) by Stas Bekman! Thanks for this cool resource!

Many thanks also to all the people who inspired this guide through discussions either at events or online, notably and not limited to:
- 🤝 Luca Soldaini, Kyle Lo and Ian Magnusson (Allen AI), Max Bartolo (Cohere), Kai Wu (Meta), Swyx and Alessio Fanelli (Latent Space Podcast), Hailey Schoelkopf (EleutherAI), Martin Signoux (Open AI), Moritz Hardt (Max Planck Institute), Ludwig Schmidt (Anthropic)
- 🔥 community users of the Open LLM Leaderboard and lighteval, who often raised very interesting points in discussions
- 🤗 people at Hugging Face, like Lewis Tunstall, Omar Sanseviero, Arthur Zucker, Hynek Kydlíček, Guilherme Penedo and Thom Wolf,
- of course my team ❤️ doing evaluation and leaderboards, Nathan Habib and Alina Lozovskaya.

## Citation
[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC-BY--NC--SA-4.0-lightgrey.svg

```
@misc{fourrier2024evaluation,
  author = {Clémentine Fourrier and The Hugging Face Community},
  title = {LLM Evaluation Guidebook},
  year = {2024},
  journal = {GitHub repository},
  url = {https://github.com/huggingface/evaluation-guidebook)
}
```
