# Tips and tricks

## Managing contamination
In general, you should assume that a dataset publicly available on the internet is or will be contaminated. 

Solutions to mitigate this include:
- providing a **canary string** in the evaluation set (like in [BigBench](https://github.com/google/BIG-bench)): it is a specific character combination that model creators can look for in their training sets, which would indicate that it contains an evaluation
- providing evaluation sets in **[encrypted](https://arxiv.org/pdf/2309.16575) or [gated](https://huggingface.co/datasets/Idavidrein/gpqa)** forms so that they can't be parsed easily by web crawlers - therefore not ending up accidentally in training sets 
- running [dynamic benchmarks](https://arxiv.org/abs/2104.14337): benchmarks regularly updated through time so that models can't "learn the answers by heart" (but it makes datasets more costly)
- if you are running a benchmark, trying to [detect contamination](https://arxiv.org/abs/2311.06233) post-hoc (for example, by looking at the generation perplexity or designing adversarial versions of the prompts - however, no method is a foolproof contamination detection method)

However, it's not because a dataset is contaminated that it won't still be interesting and have signal during training.

## Practical issues you might encounter

### Fine-tuned models, system prompts and chat templates
A number of instruction tuned models are going to perform terribly if you do not make sure to:
- add their system prompt at the very beginning of inference
- prompt them using a chat template (usually adding `Assistant` and `User` prefixes to the dialogue turns - learn more about this in [this cool guide](https://huggingface.co/docs/transformers/main/en/chat_templating))

It's also very important to not assume that different tokenizers will behave the same, especially with respect to chat templates, as you can see in this cool picture about tokenization spacing and chat templates, from [this tweet](https://x.com/danielhanchen/status/1796952220619157694).

![Spacing, tokenization and template](https://pbs.twimg.com/media/GPANfpiasAA9b6F?format=png&name=medium)

### Tokenization

1. **Tokenizing the context and choices together or separately**

When looking at an MCQA evaluation, in general, you want to tokenize the context together with the choices, as it creates a succession of tokens which is likely/natural for the model. 

However, some tokenizers (like the [Llama one](https://github.com/EleutherAI/lm-evaluation-harness/pull/531#issuecomment-1595586257)) do not satisfy `enc(context + choice) = enc(context) + enc(choice)` (and add or remove spacing). This means that comparing the logprobabilities of the choices is not easy, as the context tokens can "bleed out" into them, messing up the comparison.

So if this is the case for your model, you might want to compute the tokens of context and choice separately and then concatenate them after removing the special start/end of sentence tokens which might have been added.

2. **Paying attention to start and end of sentence tokens**

Some models, like the `Gemma` ones, are extremely sensitive to the [inclusion of start of sentence tokens](https://github.com/EleutherAI/lm-evaluation-harness/pull/1465) at inference. You might need to do a couple of experiments to see if that happens for you, and add these tokens manually when evaluating.

You can also encounter some issues where your model won't stop on an end of sentence token like you would expect (for example, on `\n`), because your model will not predict this token alone but included in an higher level token (for example, `\n\n`, which can be a single token, especially for code models). In this case, you might need to add a specific check to "backtrack" on generated text to make sure you're cutting your generated sentence at the proper spot before computing metrics. 

3. **Multilinguality and tokenization**

When looking at multilingual evaluations, you'll also need to see how to tokenize your text, depending on your evaluation task and metrics. As some languages do not always use spacing as a word separator (Korean, Thai, Japanese, Chinese, to cite a few), they will require language specific tokenizers to be split properly, else it will affect their scores on metrics such as [BLEU](https://github.com/EleutherAI/lm-evaluation-harness/issues/212), F1 scores, etc.

4. **Code evaluations and end of sentence tokens**

Code models usually have been trained with `\n\t` as a single token. This means that when generating text, they will often generate `\n\t` in one step. A task which defines `\n` as an end of sentence token (= to stop the generation) will let the model continue generating after a `\n\t`, if predicted as one token, since it's not the same as `\n`. But you would actually still want the model to stop. In these cases, you either need to update your end of sentence tokens, or define a mechanism to backtrack on the character representation of the latest tokens to stop (and cut) the generation a posteriori.

### Easy speed up for MCQA evaluations
You can speed up your MCQA predictions by a lot if you make sure your model needs to predict only one token for the task.

This way, instead of running your `number_of_choices` predictions (`context + choice 1`, `context + choice 2`, etc), you can simply run inference on `context` and compute the probability distribution on the full vocabulary (which will include all your one token choices) to get your logprobabilities of interest, and do this step in one pass. 

(That's how we do it in `lighteval`).

## Unexpectedly bad results on generative evaluations

The first thing to do is always to inspect your model generations in detail. Some frequent things to look for when troubleshooting are: 
- too strict model output parsing (before computing the metric) which leads to the answer being lost
    - Fixing: adapt your parsing
- unability of the models to follow your output format in few shot (frequent in recent models trained with instructions data, like llama 3.2 or Qwen 2.5)
    - Fixing: either adapt your prompt format, or just assume that models should be able to follow it in few shot
- exceedingly verbose model which never gets to the correct answer (more frequent in long context models and something we observed with Qwen and CommandR models)
    - Fixing: either increase the allowed context length, add instructions to be concise in the task prompt, or just assume that models should be able to answer succinctly

