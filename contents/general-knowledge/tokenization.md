# Tokenization

## Why and how do we tokenize text?
Since large language models are actually big mathematical functions, they eat numbers, not text. 

Say you want to transform a sentence to numbers. You first need to decide how to cut your sentence into small pieces, then map every small piece to a number; this is *tokenization*.

In the past, people would try to map each character of a text with its index in a alphabet (`a` -> 1, `b` -> 2, etc) which is called *character based tokenization* (you split between characters). On the other end of the spectrum, people also tried to map each word with its index in a dictionary (`a` -> 1, `aardvark` -> 2, `ab` -> 3, etc) which is called *word based tokenization* (you split on spaces, if your language has spaces - if not, it's a bit harder).

Both these methods share a strong limitation: they remove information from the input text. They erase semantic connections that you can see from word shape (ex: `dis similar`, `similar`, `similar ity`, `similar ly`), information we would like our model to retain, so it connects related words together.
(Plus, what happens if you suddenly have a completely new word in input? It gets no number, and your model can't process it 😔 )

Some people therefore had the idea to cut words into sub-words, and assign index to these sub-words (`dis`, `similar`, `ity`, `ly`)!

This was initially done using morpho-syntactic rules ("morpho-syntax" is like the grammar of word creation). Now most people use byte pair encoding (BPE), a smart statistical method to create the sub-words automatically depending on their frequency in a reference text.

So as a summary: tokenization is a way to map small units of texts (which can be one or several characters, up to the word level) to numbers (similar to an index). When you want to process text, your input text (called a *prompt* at inference) is split into these *tokens* by a tokenizer. The whole range of tokens a model or tokenizer can parse is called its *vocabulary*. 
#### Going further: Understanding tokenization
I advise reading one of the first 2 links in depth.
- ⭐ [Explanation of different tokenization methods in the 🤗 NLP Course](https://huggingface.co/learn/nlp-course/en/chapter2/4)
- ⭐ [Conceptual guide about tokenization in the 🤗 doc](https://huggingface.co/docs/transformers/en/tokenizer_summary)
- [Course by Jurafsky on tokenization (and other things)](https://web.stanford.edu/~jurafsky/slp3/2.pdf) - more academical in its approach, skip to 2.5 and 2.6 (the rest is interesting too but too broad)

#### Going further: Byte Pair Encoding
- ⭐ [Explanation of BPE in the 🤗 NLP Course](https://huggingface.co/learn/nlp-course/en/chapter6/5)
- [Paper introducing BPE to NLP](https://aclanthology.org/P16-1162/)


## Some of the many problems of tokenizations
### Choosing the correct vocabulary size
The size of the vocabulary indicates how many individual tokens (for example, sub-words) the model will have to learn. 

A vocabulary which is **too big** might contain some very rare words as full tokens (for example: `aardvark`), which can lead to 2 problems. 

If such a rare word almost never appears in the training data, it can be hard to connect to other concepts, and the model might be unable to infer what it is about. 

On the other hand, if it appears rarely and only in specific contexts, it can be linked to some very specific other words: for example, if you train on forum data, and your tokenizer mapped a username as one single token in its vocabulary, your model might then associate this token to the specific user's content.

A vocabulary which is **too small** will present 2 other problems: worst representation capabilities, and increased cost at inference. 

Let's go back to our above example, where we tokenized words derived from `similar`. Using a pseudo BPE approach (large vocabulary) to tokenize `similarly` has split the word into 2 tokens (`similar`, `ly`). If we had used instead character level tokenization (therefore with a very small vocabulary, the size of an alphabet), the same word would be cut into 9 tokens (`s`, `i`, `m`, `i`, `l`, `a`, `r`, `l`, `y`). 

Where the first method splits `similarly` into tokens which have an individual semantic  meaning, it's not the case in the second method: with too small a vocabulary, we lost some semantic representation. The difference in representations length also means that it's many times as costly to generate our word with a smaller vocabulary (takes 9 tokens instead of 2, so 5 times more costly!).

At the moment, most people seem to use heuristics for vocabulary size, which seems correlated to number of languages covered and model size, so it's likely that using a number of tokens close to the reference models of a similar size could work for you.
#### Going further: Rare tokens effect
- [SolidGoldMagikarp post on Less Wrong](https://www.lesswrong.com/posts/aPeJE8bSo6rAFoLqg/solidgoldmagikarp-plus-prompt-generation)
	- Very interesting read on how some people identified very rare tokens in Open AI's vocabulary - this is quite cool because it's done without access to the model's internals (we don't know what the training data contains for example)  
- [Fishing for Magikarp, paper by Cohere](https://arxiv.org/abs/2405.05417)
	- Follow up work on to detect these tokens

### Managing several languages
(Recommended: read an explanation of BPE before this section)
When building or choosing your tokenizer, you construct your vocabulary from reference text. This means that your tokenizer will know vocabulary words and characters from this reference text. Usually, it means using data in English, with a Latin script. 

If you want to add new language, and your new language uses the same script and share some roots, you could theoretically hope that some of your original language semantics transfer to the new language. 

However, if you want to allow your tokenizer to correctly split text in other languages (especially languages written in other scripts) you'd better include data from these languages when building said tokenizer. Most of the time, though, this data will contain an unbalanced proportion of the initial language (ex: English) to the new language (ex: Thai, or Burmese), the initial language being much more present. Since most efficient tokenizer methods used nowadays (like BPE) create their complex vocabulary tokens based on the most frequent words seen, most of the long tokens will be English words - and most of the words from the less frequent languages will only be split at the character level.

This effect leads to an unfairness in multilingual tokenization: some (less frequent, or *lower-resourced*) languages require orders of magnitude more tokens to generate a sentence of equivalent length as English.

#### Going further: Language and tokenization
- ⭐ [A beautiful breakdown and demo by Yennie Jun on tokenization issues across languages](https://www.artfish.ai/p/all-languages-are-not-created-tokenized)
	- The breakdown in itself is very clear, and it's worth playing around with the [demo space](https://huggingface.co/spaces/yenniejun/tokenizers-languages)
- ⭐ [A demo by Aleksandar Petrov on unfairness of tokenization](https://aleksandarpetrov.github.io/tokenization-fairness/)
	- I recommend looking at `Compare tokenization of sentences` to get a feel for the differences in cost of inference depending on languages

### What about numbers?
When building your tokenizer, you need to decide what to do about numbers. Do you only index 0 to 9, and assume all other numbers will be compositions of digits, or do you want to store numbers up to, say, one billion, individually? Current well known models display a range of approaches to this, but it's unclear what works better to allow mathematical reasoning. Maybe new approaches to tokenization, such as hierarchical tokenization, might be needed for this.
#### Going further: Number tokenization
- ⭐ [A nice visual demo by Yennie Jun of how tokenizers of Anthropic, Meta, OpenAI, and Mistral models split numbers](https://www.artfish.ai/p/how-would-you-tokenize-or-break-down) 
- [Small history by Beren Millidge of the evolution of number tokenization through the years](https://www.beren.io/2024-05-11-Integer-tokenization-is-now-much-less-insane/)
