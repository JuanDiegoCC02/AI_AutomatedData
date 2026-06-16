import re


def clean_text(text):

    if not text:
        return ""

    text = text.replace("\n", " ")

    text = text.replace("\t", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = re.sub(
        r"[^\w\s.,;:!?()áéíóúÁÉÍÓÚñÑ-]",
        "",
        text
    )

    return text.strip()