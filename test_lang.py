
# test_lang.py
from data_pipeline.services.language_detector import detect_language

text_es = "Juan Diego Corella Camacho completó exitosamente el programa de desarrollo."
text_en = "This certificate is proudly presented for completing the full stack track."

print("Prueba Español:", detect_language(text_es)) # Debería imprimir: es
print("Prueba Inglés:", detect_language(text_en))  # Debería imprimir: en