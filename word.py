import pandas as pd
from langdetect import detect
from langdetect import detect_langs
from collections import defaultdict
import re
import nltk
nltk.download('words')
from nltk.corpus import words as nltk_words

def count_words_by_language(text):
    word_count_by_language = defaultdict(lambda: defaultdict(int))

    french_words = set(nltk_words.words('fr'))
    english_words = set(nltk_words.words('en'))
    vietnamese_words = set(nltk_words.words('vn'))
    for sentence in text:
        # Regular expression pattern to match words including Chinese, Korean, Japanese characters, numbers, and phone numbers
        words = re.findall(r"[\u4e00-\u9fff\uac00-\ud7a3\u3040-\u309f\u30a0-\u30ff\w']+|\b\d+\b", sentence)
        for word in words:
            try:
                word_lower = word.lower()
                lang = detect(word_lower)
                word_count_by_language[lang][word_lower] += 1
            except:
                word_count_by_language['unknown'][word_lower] += 1

    return word_count_by_language

# Load the Excel file (assuming the text is in the first column)
file_path = './signs-1.xlsx'
data = pd.read_excel(file_path)

# Access the text from the first column
text_column = data.iloc[:, 0]

# Convert the column values to a list
text_list = text_column.tolist()

word_counts = count_words_by_language(text_list)
print(detect_langs('market'))

for lang, words in word_counts.items():
    print(f"Language: {lang}")
    total_words = sum(words.values())
    print(f"Total Words: {total_words}")
    print("Word Count:")
    for word, count in words.items():
        print(f"{word}: {count}")
    print("\n")

