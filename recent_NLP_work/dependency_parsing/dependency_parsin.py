import ast
import spacy
import pandas as pd

# Load Spacy English model
nlp = spacy.load("en_core_web_sm")

# Read your CSV into a DataFrame
df = pd.read_csv('/Users/sukaraca/DERSLER/2023-autumn-matloob-lab/utils/dependency_parsing/cross_with_characters.csv')

# Function to extract nsubj or pobj from a sentence
def extract_dependencies(sentence):
    doc = nlp(sentence)
    dependencies = []
    for token in doc:
        if token.dep_ in ['nsubj',
                          #'pobj'
                          ]:
            dependencies.append(token.text)
    return dependencies

# Convert string representations of lists to actual lists
df['characters_in_paragraph'] = df['characters_in_paragraph'].apply(ast.literal_eval)

# Apply the extract_dependencies function to each paragraph and create the 'dependencies' column
df['dependencies'] = df['paragraph'].apply(lambda x: [extract_dependencies(sentence.text) for sentence in nlp(x).sents])

# Flatten the 'dependencies' column
df['dependencies'] = df['dependencies'].apply(lambda x: [item for sublist in x for item in sublist])

def find_common_elements(list1, list2):
    common_elements = list(set(list1).intersection(list2))
    return common_elements

# Create the 'overlaps' column using find_common_elements for all rows
df['overlaps'] = df.apply(lambda row: find_common_elements(row['characters_in_paragraph'], row['dependencies']), axis=1)

# Create a new column 'overlap_percentage' with the percentage of characters_in_paragraph found in overlaps
df['overlap_percentage'] = df.apply(lambda row: round((len(row['overlaps']) / len(row['characters_in_paragraph'])) * 100, 2) if len(row['characters_in_paragraph']) > 0 else 0, axis=1)

# Display descriptive statistics for the 'overlap_percentage' column
statistics_table = df['overlap_percentage'].describe().to_frame().T

# Save the updated DataFrame to a new CSV
df.to_csv('/Users/sukaraca/DERSLER/2023-autumn-matloob-lab/utils/dependency_parsing/nsubj_parsing.csv', index=False)

# Save the descriptive statistics table to a new CSV file
statistics_table.to_csv('statistics_table.csv', index=False)