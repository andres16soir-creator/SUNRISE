"""
===========================================
SISTEMA DENTAL SUNRISE - VERSIÓN LICENCIADA
PROPIEDAD DE: [Andres Emanuel Terrazas Rios]
CONTACTO: [69764651 / andres16soir@gmail.com]
PROHIBIDA SU COPIA O DISTRIBUCIÓN
===========================================
"""

import os
from pathlib import Path

class CodigoInstalacion:
    def __init__(self):
        self.codigo_file = Path(__file__).parent.parent / 'instalado.ini'
        self.codigo_correcto = "Cdefgabc#m7b5JEEC2020"  # Tu código aquí
    
    def verificar_codigo(self, codigo_ingresado):
        return codigo_ingresado.strip() == self.codigo_correcto
    
    def ya_esta_instalado(self):
        return self.codigo_file.exists()
    
    def marcar_instalado(self):
        with open(self.codigo_file, 'w') as f:
            f.write('INSTALADO')
        # Archivo oculto en Windows
        try:
            os.system(f'attrib +h "{self.codigo_file}"')
        except:
            pass

codigo_manager = CodigoInstalacion()