# Gathering preference data from an arena like setup

Here are some general tips (thanks to Lewis Tunstall for this section) on the most efficient way to gather preference data for evaluations and training using an arena like setup.

- **Collect your data in batches**: This allows you to:
    - Quality check the initial batches for consistency with your guidelines
    - Potentially train new models to generate the next batch of preference data

- **Ask annotators to rate the strength of their preference** by categorizing it into one of several labels. For example, in Llama 3 they used: significantly better, better, slightly better, or marginally better. Llama 3 also had an editing step after preference ranking to encourage annotators to further improve the preferred response and get better labels (edited > chosen > rejected).

- **Focus on hard cases**: Look at where the model fails on evals and then focus on gathering labels for those kind of prompts. E.g. you want to get as much coverage in prompt complexity as possible

- **Open ended prompting**: Ideally you want to let annotators prompt the model in an open ended fashion. For this you should randomly swap the order of model completions to avoid biasing towards e.g. the first / fastest response
