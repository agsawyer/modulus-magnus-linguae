import json

# Open the JSONL file for reading
with open('13B_july1st.jsonl', 'r') as jsonl_file:
    # Open the output text file for writing
    with open('ch1-5.sentences.txt', 'w') as output_file:
        # Read each line from the JSONL file
        for line in jsonl_file:
            # Parse the JSON object
            data = json.loads(line)
            # Extract the "output" value
            output = data['output']
            # Write the output value to the text file as a new line
            output_file.write(output + '\n')