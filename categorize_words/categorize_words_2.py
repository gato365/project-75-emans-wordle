import pandas as pd

# Function to count vowels in a string
def count_vowels(text):
    vowels = 'aeiouAEIOU'
    return sum(1 for char in str(text) if char in vowels)

# Read the CSV file
df = pd.read_csv('five_letter_words_2025.csv')  # Replace with your CSV filename

# Apply the vowel counting function to your column
df['vowel_count'] = df['word'].apply(count_vowels)  # Replace 'your_column' with your column name


# # Export this file to a new CSV
# df.to_csv('five_letter_words_2025_vowels.csv', index=False)  