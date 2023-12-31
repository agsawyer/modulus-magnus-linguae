import os

def merge_text_files(directory_path, output_file):
    with open(output_file, 'w') as outfile:
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r') as infile:
                    content = infile.read().replace('\n', ' ')
                    outfile.write(content.strip() + '\n')

# Example usage
directory = 'online-text'
output_file = 'to_1file_sections.txt'
merge_text_files(directory, output_file)
