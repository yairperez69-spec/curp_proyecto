"""
Diccionario de apellidos más comunes en México
Incluye variaciones con y sin acentos
"""

APELLIDOS_MEXICANOS = {
    'GARCIA', 'GARCÍA', 'MARTINEZ', 'MARTÍNEZ', 'RODRIGUEZ', 'RODRÍGUEZ',
    'HERNANDEZ', 'HERNÁNDEZ', 'LOPEZ', 'LÓPEZ', 'GONZALEZ', 'GONZÁLEZ',
    'PEREZ', 'PÉREZ', 'SANCHEZ', 'SÁNCHEZ', 'RAMIREZ', 'RAMÍREZ',
    'TORRES', 'FLORES', 'RIVERA', 'GOMEZ', 'GÓMEZ', 'DIAZ', 'DÍAZ',
    'CRUZ', 'MORALES', 'REYES', 'GUTIERREZ', 'GUTIÉRREZ', 'ORTIZ',
    'CHAVEZ', 'CHÁVEZ', 'RUIZ', 'JIMENEZ', 'JIMÉNEZ', 'MENDOZA',
    'ALVAREZ', 'ÁLVAREZ', 'CASTILLO', 'ROMERO', 'HERRERA', 'MEDINA',
    'AGUILAR','FARRERA', 'VARGAS', 'VAZQUEZ', 'VÁZQUEZ', 'RAMOS', 'MENDEZ', 'MÉNDEZ',
    'MORENO', 'JUAREZ', 'JUÁREZ', 'CASTRO', 'GUERRERO', 'ORTEGA', 'LUNA',
    'ESTRADA', 'BAUTISTA', 'LOZANO', 'CAMPOS', 'CONTRERAS', 'LEON', 'LEÓN',
    'CARRILLO', 'ROJAS', 'DOMINGUEZ', 'DOMÍNGUEZ', 'SALAZAR', 'IBARRA',
    'VEGA','ALFARO', 'MALDONADO', 'SOTO', 'PONCE', 'GUZMAN', 'GUZMÁN', 'AVILA', 'ÁVILA',
    'DELGADO', 'SANTOS', 'VELAZQUEZ', 'VELÁZQUEZ', 'NUÑEZ', 'NÚÑEZ', 'SILVA',
    'SANTIAGO', 'NAVARRO', 'CAMACHO', 'CERVANTES', 'CABRERA', 'RUEDA', 'OCHOA',
    'RIOS', 'RÍOS', 'MOLINA', 'ALVARADO', 'MEZA', 'ESCOBAR', 'VALDEZ', 'VÁLDEZ',
    'PADILLA', 'PENA', 'PEÑA', 'DURAN', 'DURÁN', 'CORDOVA', 'CÓRDOVA', 'SANDOVAL',
    'MARQUEZ', 'MÁRQUEZ', 'MONTOYA', 'SERRANO', 'CARDENAS', 'CÁRDENAS', 'ROSALES',
    'GALLEGOS', 'BLANCO', 'ACOSTA', 'VILLANUEVA', 'VILLARREAL', 'RUBIO', 'TREJO',
    'BARRERA', 'HUERTA', 'MATA', 'CORONA', 'MONTES','DAN', 'PAREDES', 'CUELLAR', 'CUÉLLAR',
    'FERRER', 'CISNEROS', 'MIRANDA', 'CORTEZ', 'CORTÉS', 'AYALA', 'VILLEGAS',
    'ZAMORA', 'ARELLANO', 'SALAS', 'QUINTERO', 'FIGUEROA', 'PACHECO', 'VILLA',
    'ESPINOZA', 'GALVAN', 'GALVÁN', 'RANGEL', 'FUENTES', 'OROZCO', 'BENITEZ',
    'BENÍTEZ', 'MERCADO', 'MONROY', 'ESQUIVEL', 'CARBAJAL', 'CALDERON', 'CALDERÓN',
    'NAVA', 'BERNAL', 'MURILLO', 'VALENZUELA', 'VASQUEZ', 'VÁSQUEZ', 'ARANDA',
    'DUARTE', 'MEJIA', 'MEJÍA', 'VALLE', 'GALLARDO', 'PERALTA', 'MARIN', 'MARÍN',
    'IBAÑEZ', 'IBÁÑEZ', 'SUAREZ', 'SUÁREZ', 'AGUIRRE', 'LEYVA', 'TAPIA', 'BENAVIDES',
    'ZUNIGA', 'ZÚÑIGA', 'BALDERAS', 'GUILLEN', 'GUILLÉN', 'PALACIOS', 'ZUÑIGA',
    'SALINAS', 'TOVAR', 'BARAJAS', 'CABALLERO', 'MACIAS', 'MACÍAS', 'BETANCOURT',
    'SOLIS', 'SOLÍS', 'DAVILA', 'DÁVILA', 'FRANCO', 'SOSA', 'ARAGON', 'ARAGÓN',
    'BARRIOS', 'MORA', 'ZARATE', 'ZÁRATE', 'GALINDO', 'CASTELLANOS', 'CARRASCO',
    'FARIAS', 'FARÍAS', 'PORTILLO', 'TEJADA', 'FELIX', 'FÉLIX', 'PAZ', 'SEGURA',
    'AMADOR', 'AGUAYO', 'ARROYO', 'CORREA', 'HINOJOSA', 'JARAMILLO', 'LUCERO',
    'PUENTES', 'ROSARIO', 'URRUTIA',
}

APELLIDOS_COMPUESTOS = {
    'DE LA CRUZ', 'DE LA ROSA', 'DE LA TORRE', 'DE LA GARZA',
    'DEL ANGEL', 'DEL ÁNGEL', 'DEL VALLE', 'DE LOS SANTOS',
    'DE LOS REYES', 'SAN MARTIN', 'SAN MARTÍN', 'SANTA CRUZ',
    'SANTA MARIA', 'SANTA MARÍA',
}

def obtener_todos_los_apellidos():
    """Retorna todos los apellidos válidos"""
    return APELLIDOS_MEXICANOS.union(APELLIDOS_COMPUESTOS)

def normalizar_apellido(apellido):
    """Normaliza un apellido"""
    return ' '.join(apellido.strip().upper().split())

def es_apellido_valido(apellido):
    """Valida si un apellido es válido"""
    if not apellido or not isinstance(apellido, str):
        return False
    
    apellido_normalizado = normalizar_apellido(apellido)
    todos_apellidos = obtener_todos_los_apellidos()
    
    # Verificar si está en el diccionario
    if apellido_normalizado in todos_apellidos:
        return True
    
    # Verificar apellidos compuestos
    partes = apellido_normalizado.split()
    if len(partes) > 1:
        for parte in partes:
            if parte not in todos_apellidos and parte not in {'DE', 'DEL', 'LA', 'LOS', 'LAS'}:
                return False
        return True
    
    return False