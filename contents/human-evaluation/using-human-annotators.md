# Using human annotators

I suggest reading Section 3 of this [review](https://aclanthology.org/2024.cl-3.1.pdf) of good practices in data annotation quality. If you want production level quality and have the means to implement all of these methods, go ahead! 

  ![Best_annotation_practices](https://github.com/huggingface/evaluation-guidebook/blob/main/assets/best_annotation_practices.png?raw=true)

However, important guidelines (no matter your project size) are the following, once you defined your task and scoring guidelines.

- **Workforce selection, and if you can monetary incentive**
You likely want the people working on your task to:
1) obey some demographics. 
	Some examples: be native speakers of the target language, have a higher education level, be experts in a specific domain, be diverse in their geographical origins, etc. 
	 Your needs will vary depending on your task.
1) produce high quality work. 
	It's notably important now to add a way to check if answers are LLM-generated, and you'll need to filter some annotators out of your pool.
  *Imo, unless you're counting on highly motivated crowdsourced annotators, it's always better to pay your annotators correctly.*

- **Guideline design** 
Make sure to spend a lot of time really brainstorming your guidelines! That's one of the points on which we spent the most time for the [GAIA](https://huggingface.co/gaia-benchmark) dataset.

- **Iterative annotation** 
Be ready to try several rounds of annotations, as your annotators will misunderstand your guidelines (they are more ambiguous than you think)! Generating samples several times will allow your annotators to really converge on what you need.

  - **Quality estimation** and **Manual curation**
You want to control answers (notably via inter-annotator agreement if you can get it) and do a final selection to keep only the highest quality/most relevant answers.

Specialized tools to build annotated high quality datasets like [Argilla](https://argilla.io/) can also help you. 
### Going further
- ⭐ [How to set up your own annotator platform in a couple minutes](https://huggingface.co/learn/cookbook/enterprise_cookbook_argilla), by Moritz Laurer. A good read to get some hands on experience using open source tools (like Argilla and Hugging Face), and understanding better the dos and don'ts of human annotation at scale.
- ⭐ [A guide on annotation good practices](https://aclanthology.org/2024.cl-3.1.pdf). It's a review of all papers about human annotation dating from 2023, and it is very complete. Slightly dense, but very understandable.
- [Another guide on annotation good practices](https://scale.com/guides/data-labeling-annotation-guide), by ScaleAI, specialised in human evaluations. Its a more lightweigth complement to the above document.
- [Assumptions and Challenges of Capturing Human Labels](https://aclanthology.org/2024.naacl-long.126.pdf) is a paper on how to look at source of annotator disagreement and mitigate them in practice
