## Knowledge
### General
- [Foundational Model Development Cheatsheet](https://fmcheatsheet.org/), by AllenAI

### Automatic evaluation
Two cool overviews on the challenges of automatic evaluation! 
- [Challenges in LM evaluation](https://github.com/lm-evaluation-challenges/lm-evaluation-challenges.github.io/blob/main/%5BMain%5D%20ICML%20Tutorial%202024%20-%20Challenges%20in%20LM%20Evaluation.pdf), a presentation by Hailey Schoelkopf and Lintang Sutawika. 
- [Lessons from the trenches on Reproducible Evaluation of LMs](https://arxiv.org/abs/2405.14782), a paper by EleutherAI
- Two podcasts by Latent Space on evaluation
    - [Benchmarks 101](https://www.latent.space/p/benchmarks-101), on automatic benchmarks history and well-known associated issues 
    - [Benchmarks 201](https://www.latent.space/p/benchmarks-201), on which evaluation method to use when, plus some tidbits about the Leaderboard with yours truly!


### LLM as a judge
Cool summaries and experience feedbacks:
- https://eugeneyan.com/writing/llm-evaluators/
- https://cameronrwolfe.substack.com/p/llm-as-a-judge
- https://dylandigitalgarden.com/2024/July/July+31%2C+2024+LLM+%26+VLM-as-a-Judge

## Software
### Evaluation suites
- [`lm_eval`](https://github.com/EleutherAI/lm-evaluation-harness/), by Eleuther (also known as "the Harness"). The powerhouse of LLM evaluations, allowing you to evaluate any LLMs from many providers on a range of benchmarks, in a stable and reproducible way.
- [`lighteval`](https://github.com/huggingface/lighteval), by Hugging Face (disclaimer: I'm one of the authors). A light LLM evaluation suite, focused on customization and recent benchmarks.

### Leaderboards
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard), by Hugging Face. 
  Neutral 3rd party evaluation of Open LLMs on reference static benchmarks (open to submissions)
- [HELM](https://crfm.stanford.edu/helm/lite/latest/#/leaderboard), by Stanford. 
  Also evaluates models on static benchmarks, but uses win-rates to rank models
- [Chatbot Arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard), by LMSys 
  Arena using crowdsourced human evaluation to score 150 LLMs
- [LLM Performance Leaderboard](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard), by Artificial Analysis
  Performance benchmarks and pricing of the biggest LLM API providers, if you want to use an API instead of running things locally
- [All our blogs about evaluations and leaderboards](https://huggingface.co/blog?tag=leaderboard)
- [Leaderboard finder](https://huggingface.co/spaces/leaderboards/LeaderboardFinder): Find the most relevant leaderboard for your use case

### Tutorials
- [End-to-end custom domain evaluation tutorial](https://github.com/argilla-io/argilla-cookbook/tree/main/domain-eval): This tutorial guides you through building a custom evaluation task for your domain. It uses with synthetic data and manual evaluation with [Argilla](https://github.com/argilla-io/argilla/) and [distilabel](https://github.com/argilla-io/distilabel).

