from data.vocabulary_engine import get_a1_words
from data.a1_dictionary import A1_DICTIONARY
from data.sentence_engine import get_example_sentences

print("\n===== GermanPath AI =====\n")

print("TOP VOCABULARY\n")

words = get_a1_words(10)

for index, word in enumerate(words, start=1):
    meaning = A1_DICTIONARY.get(word, "Meaning not found")
    print(f"{index}. {word} -> {meaning}")

print("\nEXAMPLE SENTENCES\n")

sentences = get_example_sentences(5)

for german, english in sentences:
    print(f"🇩🇪 {german}")
    print(f"🇬🇧 {english}")
    print()