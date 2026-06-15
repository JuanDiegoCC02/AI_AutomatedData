import re


def clean_text(text):

    if not text:
        return ""

    # Eliminar saltos de línea
    text = text.replace("\n", " ")

    # Eliminar tabs
    text = text.replace("\t", " ")

    # Eliminar espacios múltiples
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Eliminar caracteres extraños
    text = re.sub(
        r"[^\w\s.,;:!?()áéíóúÁÉÍÓÚñÑ-]",
        "",
        text
    )

    return text.strip()