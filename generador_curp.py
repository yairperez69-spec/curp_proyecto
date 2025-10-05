"""
Generador y Validador de CURP basado en Análisis Sintáctico
Gramática BNF Formal para CURP México
"""

import re
import unicodedata
from datetime import datetime
from typing import Dict

class GeneradorCURP:
    """Analizador léxico y sintáctico para CURP"""
    
    # Tokens léxicos
    VOCALES = 'AEIOU'
    CONSONANTES = 'BCDFGHJKLMNÑPQRSTVWXYZ'
    ALFABETO = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    DIGITOS = '0123456789'
    
    # Gramática de estados de México (alias para compatibilidad)
    estados = ESTADOS = {
        'AS': 'Aguascalientes', 'BC': 'Baja California', 'BS': 'Baja California Sur',
        'CC': 'Campeche', 'CL': 'Coahuila', 'CM': 'Colima', 'CS': 'Chiapas',
        'CH': 'Chihuahua', 'DF': 'Ciudad de México', 'DG': 'Durango',
        'GT': 'Guanajuato', 'GR': 'Guerrero', 'HG': 'Hidalgo', 'JC': 'Jalisco',
        'MC': 'México', 'MN': 'Michoacán', 'MS': 'Morelos', 'NT': 'Nayarit',
        'NL': 'Nuevo León', 'OC': 'Oaxaca', 'PL': 'Puebla', 'QT': 'Querétaro',
        'QR': 'Quintana Roo', 'SP': 'San Luis Potosí', 'SL': 'Sinaloa',
        'SR': 'Sonora', 'TC': 'Tabasco', 'TS': 'Tamaulipas', 'TL': 'Tlaxcala',
        'VZ': 'Veracruz', 'YN': 'Yucatán', 'ZS': 'Zacatecas', 'NE': 'Nacido en el Extranjero'
    }
    
    # Palabras altisonantes (filtro léxico)
    PALABRAS_PROHIBIDAS = {
        'BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO',
        'CAKA', 'CAKO', 'COGE', 'COJI', 'COJA', 'COJE', 'KOJI', 'COJO',
        'COLA', 'CULO', 'FALO', 'FETO', 'GETA', 'GUEI', 'GUEY', 'JOTO',
        'KACA', 'KACO', 'KAGA', 'KAGO', 'KAKA', 'KAKO', 'KOGE', 'KOGI',
        'KOJA', 'KOJE', 'KOJI', 'KOJO', 'KOLA', 'KULO', 'LILO', 'LOCA',
        'LOCO', 'LOKA', 'LOKO', 'MAME', 'MAMO', 'MEAR', 'MEAS', 'MEON',
        'MIAR', 'MION', 'MOCO', 'MOKO', 'MULA', 'MULO', 'NACA', 'NACO',
        'PEDA', 'PEDO', 'PENE', 'PIPI', 'PITO', 'POPO', 'PUTA', 'PUTO',
        'QULO', 'RATA', 'ROBA', 'ROBE', 'ROBO', 'RUIN', 'SENO', 'TETA',
        'VACA', 'VAGA', 'VAGO', 'VAKA', 'VUEI', 'VUEY', 'WUEI', 'WUEY'
    }
    
    # Nombres compuestos comunes (para análisis léxico)
    NOMBRES_IGNORAR = {'MARIA', 'JOSE', 'MA', 'MA.', 'J', 'J.', 'DE', 'DEL', 'LA', 'LOS', 'LAS'}
    
    # Tabla para cálculo de homoclave
    TABLA_HOMOCLAVE = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    
    def __init__(self):
        self.tokens = []
        self.posicion = 0
    
    # ==================== FASE 1: ANÁLISIS LÉXICO ====================
    
    def normalizar_texto(self, texto: str) -> str:
        """Tokenización: Normaliza texto removiendo acentos y caracteres especiales"""
        if not texto:
            return ""
        # Remover acentos (normalización NFD)
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        # Convertir a mayúsculas y limpiar
        texto = texto.upper()
        texto = re.sub(r'[^A-ZÑ\s]', '', texto)
        return texto.strip()
    
    def extraer_primera_vocal_interna(self, palabra: str) -> str:
        """Análisis léxico: Extrae primera vocal después de la inicial"""
        if len(palabra) < 2:
            return 'X'
        for char in palabra[1:]:
            if char in self.VOCALES:
                return char
        return 'X'
    
    def extraer_primera_consonante_interna(self, palabra: str) -> str:
        """Análisis léxico: Extrae primera consonante después de la inicial"""
        if len(palabra) < 2:
            return 'X'
        for char in palabra[1:]:
            if char in self.CONSONANTES:
                return char
        return 'X'
    
    def seleccionar_nombre_principal(self, nombres: str) -> str:
        """Parser de nombres: Selecciona el nombre significativo"""
        if not nombres:
            return ""
        palabras = nombres.strip().split()
        if not palabras:
            return ""
        if len(palabras) == 1:
            return palabras[0]
        # Ignorar nombres comunes como MARIA, JOSE
        if palabras[0] in self.NOMBRES_IGNORAR and len(palabras) > 1:
            return palabras[1]
        return palabras[0]
    
    # ==================== FASE 2: ANÁLISIS SINTÁCTICO ====================
    
    def generar_iniciales(self, ap_paterno: str, ap_materno: str, nombre: str) -> str:
        """
        Producción: <iniciales> ::= <letra1> <vocal> <letra3> <letra4>
        Reglas sintácticas para las 4 iniciales de la CURP
        """
        ap_paterno = self.normalizar_texto(ap_paterno)
        ap_materno = self.normalizar_texto(ap_materno)
        nombre = self.normalizar_texto(nombre)
        nombre_principal = self.seleccionar_nombre_principal(nombre)
        
        # Aplicar gramática
        letra1 = ap_paterno[0] if ap_paterno else 'X'
        vocal = self.extraer_primera_vocal_interna(ap_paterno)
        letra3 = ap_materno[0] if ap_materno else 'X'
        letra4 = nombre_principal[0] if nombre_principal else 'X'
        
        iniciales = letra1 + vocal + letra3 + letra4
        
        # Filtro léxico: verificar palabras prohibidas
        if iniciales in self.PALABRAS_PROHIBIDAS:
            iniciales = iniciales[:3] + 'X'
        
        return iniciales
    
    def generar_fecha(self, fecha_str: str) -> str:
        """
        Producción: <fecha> ::= <año> <mes> <día>
        Valida y formatea la fecha según la gramática
        """
        try:
            fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
            año = fecha.strftime('%y')
            mes = fecha.strftime('%m')
            dia = fecha.strftime('%d')
            return año + mes + dia
        except ValueError:
            raise ValueError(f"Fecha inválida: {fecha_str}. Formato esperado: DD/MM/AAAA")
    
    def generar_sexo(self, sexo: str) -> str:
        """
        Producción: <sexo> ::= 'H' | 'M' | 'X'
        """
        sexo = sexo.upper().strip()
        if sexo not in ['H', 'M', 'X']:
            raise ValueError(f"Sexo inválido: {sexo}. Valores permitidos: H, M, X")
        return sexo
    
    def validar_entidad(self, estado: str) -> str:
        """
        Producción: <entidad> ::= AS | BC | BS | ... (32 estados)
        """
        estado = estado.upper().strip()
        if estado not in self.ESTADOS:
            raise ValueError(f"Estado inválido: {estado}. Debe ser una clave de 2 letras")
        return estado
    
    def generar_consonantes(self, ap_paterno: str, ap_materno: str, nombre: str) -> str:
        """
        Producción: <consonantes> ::= <cons1> <cons2> <cons3>
        Extrae las consonantes internas según la gramática
        """
        ap_paterno = self.normalizar_texto(ap_paterno)
        ap_materno = self.normalizar_texto(ap_materno)
        nombre = self.normalizar_texto(nombre)
        nombre_principal = self.seleccionar_nombre_principal(nombre)
        
        cons1 = self.extraer_primera_consonante_interna(ap_paterno)
        cons2 = self.extraer_primera_consonante_interna(ap_materno) if ap_materno else 'X'
        cons3 = self.extraer_primera_consonante_interna(nombre_principal) if nombre_principal else 'X'
        
        return cons1 + cons2 + cons3
    
    def calcular_homoclave(self, curp_parcial: str) -> str:
        """
        Producción: <homoclave> ::= <digito><digito>
        Algoritmo de verificación usando tabla de homoclave
        """
        suma = 0
        for i, char in enumerate(curp_parcial):
            if char in self.TABLA_HOMOCLAVE:
                valor = self.TABLA_HOMOCLAVE.index(char)
            else:
                valor = 0
            suma += valor * (18 - i)
        
        residuo = suma % 10
        digito = (10 - residuo) % 10
        
        # Retornar dos dígitos
        return str(digito) + str(digito)
    
    # ==================== FASE 3: GENERACIÓN ====================
    
    def generar_curp(self, datos: Dict[str, str]) -> str:
        """Alias para compatibilidad con app.py"""
        return self.generar(datos)
    
    def generar(self, datos: Dict[str, str]) -> str:
        """
        Método principal: Genera CURP completa aplicando todas las producciones
        
        CURP ::= <iniciales> <fecha> <sexo> <entidad> <consonantes> <homoclave>
        """
        try:
            # Aplicar producciones gramaticales
            iniciales = self.generar_iniciales(
                datos['apellido_paterno'],
                datos['apellido_materno'],
                datos['nombre']
            )
            
            fecha = self.generar_fecha(datos['fecha_nacimiento'])
            sexo = self.generar_sexo(datos['sexo'])
            entidad = self.validar_entidad(datos['estado'])
            consonantes = self.generar_consonantes(
                datos['apellido_paterno'],
                datos['apellido_materno'],
                datos['nombre']
            )
            
            # Ensamblar CURP parcial
            curp_parcial = iniciales + fecha + sexo + entidad + consonantes
            
            # Calcular y añadir homoclave
            homoclave = self.calcular_homoclave(curp_parcial)
            curp_completa = curp_parcial + homoclave
            
            return curp_completa
            
        except Exception as e:
            raise ValueError(f"Error al generar CURP: {str(e)}")
    
    # ==================== FASE 4: VALIDACIÓN ====================
    
    def validar_curp_sintaxis(self, curp: str) -> Dict:
        """Alias para compatibilidad con app.py"""
        return self.validar_sintaxis(curp)
    
    def validar_sintaxis(self, curp: str) -> Dict:
        """
        Validador sintáctico: Verifica que la CURP cumpla con la gramática BNF
        """
        curp = curp.upper().strip()
        resultado = {
            'curp': curp,
            'valida': True,
            'errores': [],
            'tokens': {},
            'detalles': []
        }
        
        # Validar longitud
        if len(curp) != 18:
            resultado['valida'] = False
            resultado['errores'].append(f"Longitud incorrecta: {len(curp)} (esperado: 18)")
            return resultado
        
        # Expresión regular basada en la gramática BNF
        patron = r'^[A-ZÑ]{4}\d{6}[HMX](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[BCDFGHJKLMNÑPQRSTVWXYZ]{3}[A-Z0-9]{2}$'
        
        if not re.match(patron, curp):
            resultado['valida'] = False
            resultado['errores'].append("No cumple con la gramática BNF de CURP")
            return resultado
        
        # Tokenizar y validar cada componente
        try:
            # Token: Iniciales
            resultado['tokens']['iniciales'] = curp[0:4]
            
            # Token: Fecha
            año = curp[4:6]
            mes = curp[6:8]
            dia = curp[8:10]
            año_actual = datetime.now().year % 100
            año_completo = f"20{año}" if int(año) <= año_actual else f"19{año}"
            fecha = datetime.strptime(f"{año_completo}{mes}{dia}", "%Y%m%d")
            resultado['tokens']['fecha'] = fecha.strftime('%d/%m/%Y')
            resultado['detalles'].append(f"✓ Fecha válida: {fecha.strftime('%d/%m/%Y')}")
            
            # Token: Sexo
            sexo = curp[10]
            sexo_map = {'H': 'Hombre', 'M': 'Mujer', 'X': 'No binario'}
            resultado['tokens']['sexo'] = sexo_map[sexo]
            resultado['detalles'].append(f"✓ Sexo: {sexo_map[sexo]}")
            
            # Token: Entidad
            estado = curp[11:13]
            if estado in self.ESTADOS:
                resultado['tokens']['estado'] = self.ESTADOS[estado]
                resultado['detalles'].append(f"✓ Estado: {self.ESTADOS[estado]}")
            else:
                resultado['valida'] = False
                resultado['errores'].append(f"Estado inválido: {estado}")
            
            # Token: Consonantes
            resultado['tokens']['consonantes'] = curp[13:16]
            
            # Token: Homoclave
            resultado['tokens']['homoclave'] = curp[16:18]
            
        except ValueError as e:
            resultado['valida'] = False
            resultado['errores'].append(f"Error en análisis léxico: {str(e)}")
        
        return resultado


# ==================== EJEMPLO DE USO ====================

if __name__ == "__main__":
    generador = GeneradorCURP()
    
    print("=" * 70)
    print("GENERADOR DE CURP - ANÁLISIS SINTÁCTICO")
    print("=" * 70)
    
    # Ejemplo: Generar CURP para PEAY000816HCSRGRA5
    datos = {
        'apellido_paterno': 'Pérez',
        'apellido_materno': 'Aguilar',
        'nombre': 'Yair',
        'fecha_nacimiento': '16/08/2000',
        'sexo': 'H',
        'estado': 'CS'
    }
    
    print(f"\nDatos de entrada:")
    for key, value in datos.items():
        print(f"  • {key}: {value}")
    
    try:
        curp_generada = generador.generar(datos)
        print(f"\n✅ CURP generada: {curp_generada}")
        
        # Validar CURP
        validacion = generador.validar_sintaxis(curp_generada)
        print(f"\nValidación: {'✅ VÁLIDA' if validacion['valida'] else '❌ INVÁLIDA'}")
        
        if validacion['detalles']:
            print("\nDetalles:")
            for detalle in validacion['detalles']:
                print(f"  {detalle}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)