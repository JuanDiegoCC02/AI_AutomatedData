import logging
from langdetect import detect, DetectorFactory

# Forzar a que los resultados de langdetect sean deterministas 
# (Evita que el mismo texto a veces dé 'es' y a veces 'en')
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

def detect_language(text: str) -> str:

    if not text or not isinstance(text, str) or not text.strip():
        logger.warning("Detección de idioma omitida: El texto provisto está vacío o no es válido.")
        return "unknown"
        
    sample_text = text.strip()[:2000]

    try:
        lang_code = detect(sample_text)
        
        return lang_code.lower()

    except Exception as e:
        logger.error(f"Error inesperado en el motor de detección de idioma: {str(e)}")
        
        spanish_connectors = {"el", "la", "los", "las", "de", "que", "en", "un", "una", "y", "para"}
        words = sample_text.lower().split()
        match_count = sum(1 for word in words if word in spanish_connectors)
        
        return "es" if match_count > 3 else "unknown"