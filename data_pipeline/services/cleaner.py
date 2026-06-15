import re
import numpy as np
import logging
from typing import List
from .embeddings import generate_embeddings

logger = logging.getLogger(__name__)

def chunk_text(text: str, target_chunk_size: int = 600, threshold_percentile: int = 85) -> List[str]:
    """
    Segmenta el texto de forma semántica basándose en la distancia vectorial 
    entre oraciones consecutivas.
    
    Args:
        text (str): El texto limpio extraído del PDF.
        target_chunk_size (int): Tamaño aproximado en caracteres para agrupar si no hay saltos temáticos.
        threshold_percentile (int): Percentil de diferencia (0-100) para declarar un cambio de tema.
                                     Un valor de 85 significa que solo el 15% de los cambios más drásticos cortarán el texto.
    """
    if not text or not text.strip():
        return []

    # 1. Segmentación inicial por oraciones utilizando Regex avanzada
    # Corta en puntos, signos de exclamación o interrogación seguidos de un espacio y mayúscula.
    sentence_endings = re.compile(r'(?<!\b\p{Lu})(?<=[.!?])\s+(?=\p{Lu})', re.UNICODE)
    sentences = [s.strip() for s in sentence_endings.split(text) if s.strip()]
    
    if len(sentences) <= 1:
        return sentences

    # 2. Generar embeddings para cada oración de forma masiva
    try:
        sentence_embeddings = generate_embeddings(sentences)
    except Exception as e:
        logger.error(f"Fallo al generar embeddings en el Chunker Semántico: {str(e)}. Usando fallback de longitud fija.")
        return _fallback_length_chunker(sentences, target_chunk_size)

    # 3. Calcular las distancias de coseno entre oraciones consecutivas
    distances = []
    for i in range(len(sentence_embeddings) - 1):
        vec1 = sentence_embeddings[i]
        vec2 = sentence_embeddings[i+1]
        
        # Fórmula del producto punto y normas para la distancia de coseno
        dot_product = np.dot(vec1, vec2)
        norm_1 = np.linalg.norm(vec1)
        norm_2 = np.linalg.norm(vec2)
        
        # Distancia de coseno (0 significa idéntico, 1 significa ortogonal/distinto)
        cosine_distance = 1.0 - (dot_product / (norm_1 * norm_2))
        distances.append(cosine_distance)

    # 4. Establecer el umbral (Threshold) dinámico basado en percentiles
    # Si las distancias son muy altas en un punto, indica ruptura semántica
    if distances:
        breakpoint_threshold = np.percentile(distances, threshold_percentile)
    else:
        breakpoint_threshold = 0.5

    # 5. Agrupar las oraciones en Chunks finales respetando los breakpoints semánticos
    chunks = []
    current_chunk = ""

    for index, sentence in enumerate(sentences):
        # Si el chunk está vacío, inicializarlo con la oración actual
        if not current_chunk:
            current_chunk = sentence
            continue

        # Verificar si la oración anterior (index - 1) fue un punto de ruptura temática
        is_breakpoint = False
        if index - 1 < len(distances):
            if distances[index - 1] > breakpoint_threshold:
                is_breakpoint = True

        # Restricción de seguridad: Si el chunk ya es muy grande, forzar el corte
        too_long = len(current_chunk) + len(sentence) > (target_chunk_size * 2)

        if is_breakpoint or too_long:
            # Guardamos el chunk estructurado actual
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            # Si mantienen el contexto, las unimos con un espacio limpio
            current_chunk += " " + sentence

    # No olvidar agregar el último bloque remanente
    if current_chunk:
        chunks.append(current_chunk.strip())

    logger.info(f"Chunking semántico completado con éxito. Oraciones: {len(sentences)} -> Chunks generados: {len(chunks)}")
    return chunks


def _fallback_length_chunker(sentences: List[str], max_chars: int) -> List[str]:
    """Fallback seguro por si la GPU/Modelo falla al calcular distancias."""
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) > max_chars:
            chunks.append(current.strip())
            current = s
        else:
            current += " " + s
    if current:
        chunks.append(current.strip())
    return chunks