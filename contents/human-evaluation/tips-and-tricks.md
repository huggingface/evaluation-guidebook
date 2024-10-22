# Tips and tricks

## Designing the task

- **Simple is better**: Annotation tasks can get unnecessarily complex, so keep it as simple as possible. Keeping the cognitive load of the annotators to a minimum will help you ensure that they stay focused and make annotations of a higher quality.

- **Check what to show**: Only show the necessary information for annotators to complete the task and make sure you don't include anything that could introduce extra bias.

- **Consider your annotators time**: Where and how things are displayed can introduce extra work or cognitive load and therefore negatively impact in the quality of results. For example, make sure that the texts and the task are visible together and avoid unnecessary scrolling. If you combine tasks and the result of one informs the other, you can display them sequentially. Think about how everything is displayed in your annotation tool and see if there's any way you can simplify even more.

- **Test the setup**: Once you have your task designed and some guidelines in place, make sure you test it yourself on a few samples before involving the whole team, and iterate as needed. 

## During the annotation

- **Annotators should work independently**: It's better if annotators don't help each other or see each other's work during the task, as they can propagate their own biases and cause annotation drift. Alignment should always happen through comprehensive guidelines. You may want to train any new team members first on a separate dataset and/or use inter-annotator agreement metrics to make sure the team is aligned.

- **Consistency is key**: If you make important changes to your guidelines (e.g., changed a definition or instruction, or have added/removed labels), consider if you need to iterate over the annotated data. At least, you should track the changes in your dataset through a metadata value like `guidelines-v1`.

## Hybrid human-machine annotation

Sometimes teams face contraints on time and resources but don't want to sacrifice on the pros of human evaluation. In these cases, you may use the help of models to make the task more efficient.

- **Model-aided annotation**: You may use the predictions or generations of a model as pre-annotations, so that the annotation team doesn't need to start from scratch. Just note that this could introduce the model's biases into human annotations, and that if the model's accuracy is poor it may increase work for annotators.

- **Supervise model as a judge**: You can combine the power of the model as a judge methodology (see the section on "Model as a judge") and human supervisors who validate or discard the results. Note that the biases discussed in the "Pros and cons of human evaluation" will apply here.

- **Idenfity edge cases**: For an even faster task, use a jury of models and then have your human supervisor(s) step in where models disagree or there's a tie to break. Again, be aware of the biases discussed in the "Pros and cons of human evaluation".
