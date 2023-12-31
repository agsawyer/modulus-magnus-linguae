for dir in "eval_1-5_accent_experiment"/*; do
	for FILE in "$dir"/*; do 
		python3 get_perplexity.py $FILE
		done
done
