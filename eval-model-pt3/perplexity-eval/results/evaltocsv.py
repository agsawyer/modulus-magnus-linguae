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
filtered_df = df[df['model'].isin(['hugging13B', '13Bjuly2nd1', 'davinci', 'davinci:ft-personal:ch1to35-txt-2023-07-03-21-57-28'])] # Filter for specific models

# renaming models
model_name_mapping = {
    'hugging13B': 'LLaMA-base',
    '13Bjuly2nd1': 'LLaMA-finetuned',
    'davinci': 'davinci-base',
    'davinci:ft-personal:ch1to35-txt-2023-07-03-21-57-28': 'davinci-finetuned'
}
filtered_df['model'] = filtered_df['model'].replace(model_name_mapping)


pivot_df_model_chapter = create_pivot_table(filtered_df, 'model', 'chapter', 'accuracy')
pivot_df_model_chapter.to_csv(output_directory + 'results-model-chapter.csv')

# model chapter plot
ax = pivot_df_model_chapter.T.plot(kind='line')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set(xlabel='Chapter', ylabel='Accuracy', title='Accuracy per model and chapter')

# Move the legend to the bottom right corner
plt.legend(title='Model', loc='lower right')

# Save the figure
plt.savefig(output_directory + 'model_chap.png')
plt.close()


# chapter quiz type table
pivot_df_chapter_quiztype = create_pivot_table(filtered_df, 'model', 'quiz_type', 'accuracy')
pivot_df_chapter_quiztype.to_csv(output_directory + 'results-model-quiz_type.csv')

# Group by model and calculate the mean accuracy
model_accuracy = df.groupby('model')['accuracy'].mean()
plt.clf()

# Create bar graph
model_accuracy.plot(kind='bar', xlabel='Model', ylabel='Accuracy', title='Accuracy per Model')
plt.savefig(output_directory + 'model_accuracy.png')

# Create bar chart for quiz type accuracy
pivot_df_chapter_quiztype.plot(kind='bar', xlabel='Model', ylabel='Accuracy', title='Accuracy per Quiz Type')
plt.savefig(output_directory + 'quiztype_accuracy.png')
