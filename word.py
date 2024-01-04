
import pandas as pd
import re
from collections import defaultdict
import nltk
nltk.download('words')

nltk.download('swadesh')
vietnamese_word_set = set()
french_word_set = set()
english_word_set = set()

# Read words from the text file and store them in a set
with open('vietnamese.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word = line.strip()  # Remove leading/trailing whitespaces, newlines, etc.
        vietnamese_word_set.add(word.lower())
with open('english.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word = line.strip()  # Remove leading/trailing whitespaces, newlines, etc.
        english_word_set.add(word.lower())
with open('french.txt', 'r', encoding='utf-8') as file:
    for line in file:
        word = line.strip()  # Remove leading/trailing whitespaces, newlines, etc.
        french_word_set.add(word.lower())

def is_french_word(word):
    return word.lower() in french_word_set
def is_spanish_word(word):
    return word.lower() in spanish_word_set
def is_english_word(word):
    return word.lower() in english_word_set
def is_vietnamse_word(word):
    return word.lower() in vietnamese_word_set
# Function to detect language of a word using character ranges
def detect_language(word):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')  # Chinese character range
    japanese_pattern = re.compile(r'[\u3040-\u30ff\u31f0-\u31ff\u3200-\u32ff]+')  # Japanese character range
    korean_pattern = re.compile(r'[\uac00-\ud7a3]+')  # Korean character range
    number_pattern = re.compile(r'\b\d+\b')  # Matches whole numbers

    if re.match(chinese_pattern, word):
        return 'zh'
    elif re.match(japanese_pattern, word):
        return 'ja'
    elif re.match(korean_pattern, word):
        return 'ko'
    elif re.match(number_pattern, word):
        return 'number'
    elif is_vietnamse_word(word):
        return 'vn'
    elif is_english_word(word):
        return 'en'
    elif is_french_word(word):
        return 'fr'
    else:
        return 'unknown'

def separate_characters_and_words(sentence):
    # Regular expression pattern to match individual Chinese, Korean, and Japanese characters
    chinese_characters = re.findall(r'[\u4e00-\u9fff]', sentence)
    korean_characters = re.findall(r'[\uac00-\ud7a3]', sentence)
    japanese_characters = re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', sentence)

    # Remove CJK characters to get English words and numbers
    sentence_without_cjk = re.sub(r'[\u4e00-\u9fff\uac00-\ud7a3\u3040-\u309f\u30a0-\u30ff]', ' ', sentence)

    # Split the remaining text by spaces to extract English words and numbers
    english_words = re.findall(r'\w+', sentence_without_cjk)

    # Merge all lists into a single array
    all_characters = chinese_characters + korean_characters + japanese_characters + english_words

    return all_characters
# Function to count words by language
def count_words_by_language(text):
    word_count_by_language = defaultdict(lambda: defaultdict(int))

    for sentence in text:
        # Regular expression pattern to match words including Chinese, Korean, Japanese characters, numbers, and phone numbers
        words = separate_characters_and_words(sentence)
        for word in words:
            lang = detect_language(word)
            word_count_by_language[lang][word] += 1

    return word_count_by_language

# Load the Excel file (assuming the text is in the first column)
file_path = './signs-1.xlsx'
data = pd.read_excel(file_path)

# Access the text from the first column
text_column = data.iloc[:, 0]

# Convert the column values to a list
text_list = text_column.tolist()

word_counts = count_words_by_language(text_list)


# Assuming word_counts is the dictionary containing language-wise word counts

file_path = 'word_counts_output.txt'  # File path to save the output

with open(file_path, 'w', encoding='utf-8') as file:
    for lang, words in word_counts.items():
        file.write(f"Language: {lang}\n")
        total_words = sum(words.values())
        file.write(f"Total Words: {total_words}\n")
        file.write("Word Count:\n")
        for word, count in words.items():
            file.write(f"{word}: {count}\n")
        file.write("\n")

