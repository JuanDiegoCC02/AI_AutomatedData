import logging
from langdetect import detect, DetectorFactory

# Forzar a que los resultados de langdetect sean deterministas 
# (Evita que el mismo texto a veces dé 'es' y a veces 'en')
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

def detect_language(text: str) -> str:
    """
    Analiza el corpus de texto extraído del documento y determina el idioma predominante.
    
    Args:
        text (str): El texto limpio extraído del archivo PDF.
        
    Returns:
        str: Código de idioma de dos caracteres (ISO 639-1) o 'unknown' en caso de fallo.
    """
    # 1. Validación de seguridad sanitaria del texto
    if not text or not isinstance(text, str) or not text.strip():
        logger.warning("Detección de idioma omitida: El texto provisto está vacío o no es válido.")
        return "unknown"
        
    # Limpiamos espacios innecesarios y tomamos una muestra significativa para agilizar el cómputo
    sample_text = text.strip()[:2000]

    try:
        # 2. Ejecución del motor de inferencia lingüística
        lang_code = detect(sample_text)
        
        # Normalizamos la salida a minúsculas
        return lang_code.lower()

    except Exception as e:
        # 3. Control de degradación elegante (Graceful Degradation)
        logger.error(f"Error inesperado en el motor de detección de idioma: {str(e)}")
        
        # Salvaguarda: Análisis heurístico básico por conectores comunes en español
        spanish_connectors = {"el", "la", "los", "las", "de", "que", "en", "un", "una", "y", "para"}
        words = sample_text.lower().split()
        match_count = sum(1 for word in words if word in spanish_connectors)
        
        # Si contiene conectores españoles claros, asumimos español, si no, lo dejamos desconocido
        return "es" if match_count > 3 else "unknown"