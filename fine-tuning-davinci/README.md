The following is meant to provide some insight into how we prepared the textbook data to finetune OpenAI's davinci. 

Within raw-text there are multiple folders of different data that we used (ie we experimented with using hand transcribed text, text from an online book, and text with vs without accents). 

The OpenAI API utilizes jsonl files as input for finetuning it's models, so the jsonl folder contains all of the files we trainined davinci with. Before we switched to evaluating the model by only looking at it's perplexity, the finetuning process also included instruction tuning for various numbers of examples which can also be seen in that folder. The to-jsonlques folder includes the scripts that took the text and created fake questions for the model to train it on.

Finally, paper-experiments-final includes the jsonl file that the model evaluated in the final version of our paper used.