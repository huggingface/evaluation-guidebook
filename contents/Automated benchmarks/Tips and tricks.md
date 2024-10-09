## Managing contamination
In general, you should assume that a dataset publicly available on the internet is or will be contaminated. 

Solutions to mitigate this include:
- providing a **canary string** in the evaluation set (like in [BigBench](https://github.com/google/BIG-bench)): it is a specific character combination that model creators can look for in their training sets, which would indicate that it contains an evaluation
- providing evaluation sets in **[encrypted](https://arxiv.org/pdf/2309.16575) or [gated](https://huggingface.co/datasets/Idavidrein/gpqa)** forms so that they can't be parsed easily by web crawlers - therefore not ending up accidentally in training sets 
- running [dynamic benchmarks](https://arxiv.org/abs/2104.14337): benchmarks regularly updated through time so that models can't "learn the answers by heart" (but it makes datasets more costly)
- if you are running a benchmark, trying to [detect contamination](https://arxiv.org/abs/2311.06233) post-hoc (for example, by looking at the generation perplexity or designing adversarial versions of the prompts - however, no method is a foolproof contamination detection method)

However, it's not because a dataset is contaminated that it won't still be interesting and have signal during training.