def calculate_quality(chunks):

    total_chunks = len(chunks)

    average_length = (
        sum(len(chunk) for chunk in chunks)
        / total_chunks
    )

    duplicate_chunks = (
        total_chunks - len(set(chunks))
    )

    score = 100

    if average_length < 100:
        score -= 20

    if duplicate_chunks > 0:
        score -= duplicate_chunks * 5

    score = max(score, 0)

    return {
        "quality_score": score,
        "duplicate_chunks": duplicate_chunks
    }