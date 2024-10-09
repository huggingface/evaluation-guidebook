## Knowledge
### General
- [Foundational Model Development Cheatsheet](https://fmcheatsheet.org/), by AllenAI

### Automatic evaluation
- Presentation by Hailey

### LLM as a judge
Cool summaries and experience feedbacks:
- https://eugeneyan.com/writing/llm-evaluators/
- https://cameronrwolfe.substack.com/p/llm-as-a-judge
- https://dylandigitalgarden.com/2024/July/July+31%2C+2024+LLM+%26+VLM-as-a-Judge

## Software
### Evaluation suites
- [`lm_eval`](https://github.com/EleutherAI/lm-evaluation-harness/), by Eleuther (also known as "the Harness"). The powerhouse of LLM evaluations, allowing you to evaluate any LLMs from many providers on a range of benchmarks, in a stable and reproducible.
- [`lighteval`](https://github.com/huggingface/lighteval), by Hugging Face (disclaimer: I'm one of the authors). A light LLM evaluation suite, focused on customization and recent benchmarks.

### Leaderboards
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard), by Hugging Face. 
  Neutral 3rd party evaluation of Open LLMs on reference static benchmarks (open to submissions)
- [HELM](https://crfm.stanford.edu/helm/lite/latest/#/leaderboard), by Stanford. 
  Also evaluates models on statif benchmarks, but uses win-rates to rank models
- [Chatbot Arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard), by LMSys 
  Arena using crowdsourced human evaluation to score 150 LLMs
- [LLM Performance Leaderboard](https://huggingface.co/spaces/ArtificialAnalysis/LLM-Performance-Leaderboard), by Artificial Analysis
  Performance benchmarks and pricing of the biggest LLM API providers, if you want to use an API instead of running things locally
- [All our blogs about evaluations and leaderboards](https://huggingface.co/blog?tag=leaderboard)
- [Leaderboard finder](https://huggingface.co/spaces/leaderboards/LeaderboardFinder): Find the most relevant leaderboard for your use case

