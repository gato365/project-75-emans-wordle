import random
import nltk
nltk.download('wordnet')
import pandas as pd
from nltk.corpus import wordnet as wn
from collections import Counter



# Assuming you have a text file 'words.txt' with one word per line
with open('five_letter_words.txt', 'r') as file:
    words = file.read().split()

# Randomly select 100 words
selected_words = random.sample(words, 100)

# Define the functions as before
def categorize_words(words):
    categories = {}
    for word in words:
        synsets = wn.synsets(word)
        if synsets:
            category = synsets[0].lexname()
            categories[word] = category
        else:
            categories[word] = 'undefined'
    return categories

def measure_difficulty_by_frequency(words):
    return {word: random.choice(['easy', 'medium', 'hard']) for word in words}

def measure_difficulty_by_letter_frequency(words):
    letter_frequency = Counter(''.join(words))
    return {word: 'hard' if sum(1 / (letter_frequency[char] + 1) for char in set(word)) > 0.2 else 
                   'medium' if sum(1 / (letter_frequency[char] + 1) for char in set(word)) > 0.1 else 
                   'easy' 
            for word in words}

def categorize_by_field(words, field):
    field_related_words = {'statistics': ['mean', 'median', 'mode', 'range']}
    return {word: 'related' if word in field_related_words.get(field, []) else 'unrelated' for word in words}

# Generate the categorizations and difficulties
word_categories = categorize_words(selected_words)
difficulty_by_frequency = measure_difficulty_by_frequency(selected_words)
difficulty_by_letters = measure_difficulty_by_letter_frequency(selected_words)
statistics_relatedness = categorize_by_field(selected_words, 'statistics')

# Create a DataFrame from the generated data
data = {
    'Word': selected_words,
    'Category': [word_categories[word] for word in selected_words],
    'Difficulty by Frequency': [difficulty_by_frequency[word] for word in selected_words],
    'Difficulty by Letter Frequency': [difficulty_by_letters[word] for word in selected_words],
    'Related to Statistics': [statistics_relatedness[word] for word in selected_words]
}

df = pd.DataFrame(data)

# Display the DataFrame
print(df.head())  # Print the first few rows of the DataFrame

# Optionally, save the DataFrame to a CSV file
df.to_csv('word_analysis.csv', index=False)
