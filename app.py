from flask import Flask, render_template, request, jsonify
from validador_ortografico import validar_campo
from generador_curp import GeneradorCURP
from datetime import datetime

app = Flask(__name__)
generador = GeneradorCURP()

curps_cache = {}
validaciones_realizadas = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validar-campo', methods=['POST'])
def validar_campo_endpoint():
    data = request.get_json()
    texto = data.get('texto', '').strip()
    tipo = data.get('tipo', 'nombre')
    
    if not texto:
        return jsonify({
            'valido': False,
            'tipo_error': 'vacio',
            'mensaje': f'El {tipo.replace("_", " ")} no puede estar vacío',
            'sugerencias': []
        })
    
    resultado = validar_campo(texto, tipo)
    return jsonify(resultado)

@app.route('/generar-curp', methods=['POST'])
def generar_curp_endpoint():
    global validaciones_realizadas
    
    data = request.get_json()
    required_fields = ['apellido_paterno', 'apellido_materno', 'nombre',
                      'fecha_nacimiento', 'sexo', 'estado']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': f'Falta el campo: {field.replace("_", " ")}'
            }), 400
    
    try:
        try:
            fecha = datetime.strptime(data['fecha_nacimiento'], '%d/%m/%Y')
            if fecha > datetime.now():
                return jsonify({'success': False, 'error': 'Fecha futura no válida'}), 400
            if fecha.year < 1900:
                return jsonify({'success': False, 'error': 'Fecha anterior a 1900 no válida'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Formato de fecha inválido'}), 400
        
        if data['sexo'].upper() not in ['H', 'M', 'X']:
            return jsonify({'success': False, 'error': 'Sexo inválido'}), 400
        
        if data['estado'].upper() not in generador.estados:
            return jsonify({'success': False, 'error': 'Estado inválido'}), 400
        
        curp = generador.generar_curp(data)
        validacion = generador.validar_curp_sintaxis(curp)
        
        curps_cache[curp] = {
            'datos': data,
            'validacion': validacion,
            'timestamp': datetime.now().isoformat()
        }
        
        validaciones_realizadas += 1
        
        return jsonify({
            'success': True,
            'curp': curp,
            'validacion': validacion,
            'total_validaciones': validaciones_realizadas
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar CURP: {str(e)}'
        }), 500

@app.route('/validar-curp', methods=['POST'])
def validar_curp_endpoint():
    global validaciones_realizadas
    
    data = request.get_json()
    curp = data.get('curp', '').strip().upper()
    
    if not curp:
        return jsonify({'success': False, 'error': 'CURP vacía'}), 400
    
    if curp in curps_cache:
        return jsonify({
            'success': True,
            'cached': True,
            'validacion': curps_cache[curp]['validacion']
        })
    
    validacion = generador.validar_curp_sintaxis(curp)
    
    if validacion['valida']:
        curps_cache[curp] = {
            'validacion': validacion,
            'timestamp': datetime.now().isoformat()
        }
        validaciones_realizadas += 1
        
        return jsonify({
            'success': True,
            'cached': False,
            'validacion': validacion,
            'total_validaciones': validaciones_realizadas
        })
    else:
        return jsonify({
            'success': False,
            'error': 'CURP no válida',
            'validacion': validacion
        }), 400

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    return jsonify({
        'total_validaciones': validaciones_realizadas,
        'curps_en_cache': len(curps_cache),
        'curps_cache': list(curps_cache.keys())
    })

@app.route('/limpiar-cache', methods=['POST'])
def limpiar_cache():
    global curps_cache
    cantidad = len(curps_cache)
    curps_cache.clear()
    return jsonify({
        'success': True,
        'mensaje': f'Se eliminaron {cantidad} CURPs del cache'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SISTEMA GENERADOR DE CURP - ANÁLISIS SINTÁCTICO")
    print("=" * 60)
    print("📚 Diccionarios cargados:")
    print("   - 200+ apellidos mexicanos comunes")
    print("   - 150+ nombres mexicanos comunes")
    print("🔍 Análisis sintáctico + corrección ortográfica")
    print("✅ Sistema listo para usar")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0')