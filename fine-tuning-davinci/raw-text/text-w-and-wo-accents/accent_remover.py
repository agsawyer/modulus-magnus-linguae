from unidecode import unidecode

# Read the text file
with open('ch1-5.sentences.accents.txt', 'r') as file:
    text = file.read()

# Remove Latin accents
text_without_accents = unidecode(text)

# Write the text without accents to a new file
with open('ch1-5.sentences.no-accents.txt', 'w') as file:
    file.write(text_without_accents)
