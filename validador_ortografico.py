"""
Validador ortográfico con algoritmo de distancia de Levenshtein
"""

import re
from diccionario_nombres import obtener_todos_los_nombres, es_nombre_valido
from diccionario_apellidos import obtener_todos_los_apellidos, es_apellido_valido

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    fila_anterior = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(s2):
            inserciones = fila_anterior[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_anterior[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_anterior = fila_actual
    return fila_anterior[-1]

def calcular_similitud(s1, s2):
    distancia = distancia_levenshtein(s1.upper(), s2.upper())
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 100.0
    similitud = (1 - distancia / max_len) * 100
    return round(similitud, 2)

def encontrar_sugerencias(texto, diccionario, max_sugerencias=3, umbral_similitud=60):
    texto_upper = texto.upper().strip()
    sugerencias = []
    for palabra in diccionario:
        similitud = calcular_similitud(texto_upper, palabra)
        if similitud >= umbral_similitud:
            sugerencias.append((palabra, similitud))
    sugerencias.sort(key=lambda x: x[1], reverse=True)
    return sugerencias[:max_sugerencias]

def validar_sintaxis_basica(texto):
    texto = texto.strip()
    if not texto:
        return False, "El campo no puede estar vacío"
    if len(texto) < 2:
        return False, "Debe tener al menos 2 caracteres"
    if len(texto) > 50:
        return False, "Es demasiado largo (máximo 50 caracteres)"
    if re.search(r'\d', texto):
        return False, "No puede contener números"
    if re.search(r'[^A-ZÑa-zñáéíóúüÁÉÍÓÚÜ\s\-\'\.]', texto):
        return False, "Contiene caracteres no permitidos"
    if re.search(r'\s{2,}', texto):
        return False, "No puede tener espacios múltiples"
    if re.search(r'(.)\1{2,}', texto):
        return False, "Contiene un patrón sospechoso (letras repetidas)"
    return True, None

def validar_nombre_con_correccion(nombre):
    es_valido_sintaxis, error_sintaxis = validar_sintaxis_basica(nombre)
    if not es_valido_sintaxis:
        return {
            'valido': False,
            'tipo_error': 'sintactico',
            'mensaje': f"Error sintáctico: {error_sintaxis}",
            'sugerencias': []
        }
    
    if es_nombre_valido(nombre):
        return {
            'valido': True,
            'tipo_error': None,
            'mensaje': "Nombre válido",
            'sugerencias': []
        }
    
    diccionario = obtener_todos_los_nombres()
    sugerencias = encontrar_sugerencias(nombre, diccionario, max_sugerencias=3, umbral_similitud=65)
    
    if sugerencias:
        mejor_sugerencia = sugerencias[0]
        mensaje = f"'{nombre}' no está en el diccionario. ¿Quisiste decir '{mejor_sugerencia[0].title()}'?"
        return {
            'valido': False,
            'tipo_error': 'ortografico',
            'mensaje': mensaje,
            'sugerencias': [
                {'palabra': sug[0].title(), 'similitud': sug[1]} 
                for sug in sugerencias
            ]
        }
    else:
        return {
            'valido': False,
            'tipo_error': 'desconocido',
            'mensaje': f"'{nombre}' no es un nombre reconocido",
            'sugerencias': []
        }

def validar_apellido_con_correccion(apellido):
    es_valido_sintaxis, error_sintaxis = validar_sintaxis_basica(apellido)
    if not es_valido_sintaxis:
        return {
            'valido': False,
            'tipo_error': 'sintactico',
            'mensaje': f"Error sintáctico: {error_sintaxis}",
            'sugerencias': []
        }
    
    if es_apellido_valido(apellido):
        return {
            'valido': True,
            'tipo_error': None,
            'mensaje': "Apellido válido",
            'sugerencias': []
        }
    
    diccionario = obtener_todos_los_apellidos()
    sugerencias = encontrar_sugerencias(apellido, diccionario, max_sugerencias=3, umbral_similitud=70)
    
    if sugerencias:
        mejor_sugerencia = sugerencias[0]
        mensaje = f"El apellido '{apellido}' no está bien escrito. ¿Quisiste decir '{mejor_sugerencia[0].title()}'?"
        return {
            'valido': False,
            'tipo_error': 'ortografico',
            'mensaje': mensaje,
            'sugerencias': [
                {'palabra': sug[0].title(), 'similitud': sug[1]} 
                for sug in sugerencias
            ]
        }
    else:
        return {
            'valido': False,
            'tipo_error': 'desconocido',
            'mensaje': f"El apellido '{apellido}' no es reconocido",
            'sugerencias': []
        }

def validar_campo(texto, tipo='nombre'):
    if tipo == 'nombre':
        return validar_nombre_con_correccion(texto)
    else:
        return validar_apellido_con_correccion(texto)