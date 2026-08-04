from collections import Counter
with open("sample_text.txt", "r") as file:
    text = file.read().lower()
text = text.replace(".", "").replace(",", "")
words = text.split()
frequency = Counter(words)
print("Word Frequency Distribution:")
for word, count in frequency.items():
    print(word, ":", count)