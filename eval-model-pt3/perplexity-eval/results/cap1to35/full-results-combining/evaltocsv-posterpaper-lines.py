import pandas as pd 
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import AutoLocator, MaxNLocator  # Add MaxNLocator to the import statement

roman_to_decimal = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
    'XXI': 21,
    'XXII': 22,
    'XXIII': 23,
    'XXIV': 24,
    'XXV': 25,
    'XXVI': 26,
    'XXVII': 27,
    'XXVIII': 28,
    'XXIX': 29,
    'XXX': 30,
    'XXXI': 31,
    'XXXII': 32,
    'XXXIII': 33,
    'XXXIV': 34,
    'XXXV': 35
}

def create_pivot_table(df, index, columns, values): 
    df = df.groupby([index, columns])[values].mean().reset_index() 
    pivot_df = df.pivot(index=index, columns=columns, values=values)
    return pivot_df
# ...

# iterate through all the files in results folder
directory = 'full'
data = []
for filename in os.listdir(directory):
    if filename.endswith(".raw.json"):
        continue
    filePath = os.path.join(directory, filename)
    if os.path.isfile(filePath):
        with open(filePath) as f:
            rate = f.read()
            try:
                accuracy = float(rate)
            except ValueError:
                print(f"Could not convert {rate} to float. In file: " + filename + " Skipping..")
                continue
        chapter, quiz_type, model = filename.split(".")[0:3]  # Adjusted according to the new file name structure
        data.append([model, chapter, quiz_type, accuracy])

# making data frame
df = pd.DataFrame(data, columns=["model", "chapter", "quiz_type", "accuracy"])
df['chapter'] = df['chapter'].str.split('_').str[1].map(roman_to_decimal)
print(df)

# Set font style and size
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 13


# pivoting to make specific tables
output_directory = "graphs/"
# model chapter table
# No 'shot' column, so we remove that filter
filtered_df = df[df['model'].isin(['hugging13B', 'alltextbook', 'davinci', 'davinci:ft-personal:ch1to35-txt-2023-07-03-21-57-28'])] # Filter for specific models

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# renaming models
model_name_mapping = {
    'hugging13B': 'LLaMA',
    'alltextbook': 'Latin-LLaMA',
    'davinci': 'Davinci',
    'davinci:ft-personal:ch1to35-txt-2023-07-03-21-57-28': 'Latin-Davinci'
}
filtered_df['model'] = filtered_df['model'].replace(model_name_mapping)

pivot_df_model_chapter = create_pivot_table(filtered_df, 'model', 'chapter', 'accuracy')
pivot_df_model_chapter.to_csv(output_directory + 'results-model-chapter.csv')

# Divide models into two groups
models_group1 = ['LLaMA', 'Latin-LLaMA']
models_group2 = ['Davinci', 'Latin-Davinci']

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Plot models from group 1
pivot_df_model_chapter.loc[models_group1].T.plot(kind='line', ax=ax1, color=['darkgreen', 'limegreen'])
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter (Group 1)')
ax1.legend(title='Model', loc='lower right')
ax1.set_xlim(1, 35)  # Set x-axis limits

# Plot models from group 2
pivot_df_model_chapter.loc[models_group2].T.plot(kind='line', ax=ax2, color=['darkblue', 'deepskyblue'])
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter (Group 2)')
ax2.legend(title='Model', loc='lower right')
ax2.set_xlim(1, 35)  # Set x-axis limits

# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.4)

# Save the figure
plt.savefig(output_directory + 'model_chap.png')
plt.savefig('model_chap.svg', format='svg')

plt.close()
