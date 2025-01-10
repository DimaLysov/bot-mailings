def is_valid_password(sentence):
    words = sentence.split()
    return len(words) == 4 and all(len(word) == 4 for word in words)
