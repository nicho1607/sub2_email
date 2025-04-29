import json

class PreInscripcion:
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return {
            'nombre': data.get('nombre', ''),
            'apellido': data.get('apellido', ''),
            'email': data.get('email', ''),
            'programa_interes': data.get('programa_interes', ''),
            'telefono': data.get('telefono', '')
        }
    
    @staticmethod
    def to_email_body(data):
        return f"""
        Datos del interesado:
        
        Nombre: {data['nombre']} {data['apellido']}
        Email: {data['email']}
        Teléfono: {data['telefono']}
        Programa de interés: {data['programa_interes']}
        
        Por favor contactar al interesado a la brevedad.
        """