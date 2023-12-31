This folder contains the third part of the process of evaluating the model. It takes the json files of the exercises that include the specialized format to make the API calls as well as the answers, and calls upon the model to respond to the input.

Based on the output of the model, the question will either be marked as right or wrong, and eventually be saved as both a raw output file and a total score file. We then use the series of output json files in results with a script to generate graphs that reflect how well the model has done across chapters and compared to other models. Other versions of our experiments also included things like question type and number of prompts given.

The perplexity-eval folder includes all of the scripts that were used to generate the graphs for the final version of the paper. The accuracy-eval folder includes the evaluation and results for before we evaluated based on perplexity and instead looked at the exact answer the model gave. 

We also experimented with trying to "grade" the model's output free response style, seen in the free-response folder.