import os

# Specify the directory containing the small text files
directory = 'ch1-5-online'

# Specify the path to the output big text file
output_file = 'ch1-5_lines-no-accent.txt'

# Open the output file in write mode
with open(output_file, 'w') as output:
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # Open each small text file in read mode
            with open(file_path, 'r') as file:
                # Read each line from the small text file
                lines = file.readlines()
                # Write each line to the big text file
                output.writelines(lines)

print("Combination complete. The big text file is ready!")