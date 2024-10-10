# The LLM Evaluation guidebook ⚖️

If you've ever wondered how to make sure an LLM performs well on your specific task, this guide is for you! 

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
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Automated%20benchmarks/Basics.md)
- [Designing your automatic evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Automated%20benchmarks/Designing%20your%20automatic%20evaluation.md)
- [Some evaluation datasets](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Automated%20benchmarks/Some%20evaluation%20datasets.md)
- [Tips and tricks](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Automated%20benchmarks/Tips%20and%20tricks.md)

### Human evaluation
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Human%20evaluation/Basics.md)
- [Using human annotators](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Human%20evaluation/Using%20human%20annotators.md)

### LLM-as-a-judge
- [Basics](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/Basics.md)
- [Getting a Judge-LLM](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/Getting%20a%20Judge-LLM.md)
- [Designing your evaluation prompt](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/Designing%20your%20evaluation%20prompt.md)
- [Evaluating your evaluator](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/Evaluating%20your%20evaluator.md)
- [Tips and tricks](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Model%20as%20a%20judge/Tips%20and%20tricks.md)

### Troubleshooting
The most densely practical part of this guide. 
- [Troubleshooting inference](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Troubleshooting/Troubleshooting%20inference.md)
- [Troubleshooting reproducibility](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/Troubleshooting/Troubleshooting%20reproducibility.md)

### General knowledge
These are mostly beginner guides to LLM basics, but will still contain some tips and cool references! 
If you're a advanced user, I suggest skimming to the `Going further` sections.
- [Model inference and evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/General%20knowledge/Model%20inference%20and%20evaluation.md)
- [Tokenization](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/General%20knowledge/Tokenization.md)

## Planned next articles
- contents/Automated benchmarks/Metrics -> Description of automatic metrics
- contents/Introduction: Why do we need to do evaluation?
- contents/Troubleshooting/Troubleshooting ranking: Why comparing models is hard

## Resources
Links I like
- [About evaluation](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20evaluation.md)
- [About NLP](https://github.com/huggingface/evaluation-guidebook/blob/main/resources/About%20NLP.md)

## Thanks
This guide has been heavily inspired by the [ML Engineering Guidebook](https://github.com/stas00/ml-engineering) by Stas Bekman! Thanks for this cool resource!

Many thanks also to all the people who inspired this guide through discussions either at events or online, notably and not limited to:
- 🤝 Luca Soldaini, Kyle Lo and Ian Magnusson (Allen AI), Max Bartolo (Cohere), Kai Wu (Meta), Swyx and Alessio Fanelli (Latent Space Podcast), Hailey Schoelkopf (EleutherAI), Moritz Hardt (Max Planck Institute), Ludwig Schmidt (Anthropic)
- 🤗 people at Hugging Face, like Lewis Tunstall, Omar Sanseviero, Arthur Zucker, Hynek Kydlíček, Guilherme Penedo and Thom Wolf,
- of course my team ❤️ doing evaluation and leaderboards, Nathan Habib and Alina Lozovskaya.

## Citation
```
@misc{fourrier2024evaluation,
  author = {Fourrier, Clémentine},
  title = {LLM Evaluation Guidebook},
  year = {2024},
  journal = {GitHub repository},
  url = {https://github.com/huggingface/evaluation-guidebook)
}
```
