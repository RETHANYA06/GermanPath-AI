from app.data.content_loader import load_vocabulary_topics

words = load_vocabulary_topics()

print(f"Loaded {len(words)} words\n")

for word in words[:10]:
    print(word)