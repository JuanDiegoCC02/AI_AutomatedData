
def calculate_complexity(text):

    words = text.split()

    if not words:
        return 0

    unique_words = len(set(words))

    score = (
        unique_words / len(words)
    ) * 100

    return round(score, 2)