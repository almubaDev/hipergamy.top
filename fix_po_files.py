"""
Script para arreglar problemas con archivos .po en formato UTF-8
"""
import os
import re

def fix_po_file(file_path):
    """Arregla problemas comunes en archivos .po"""
    print(f"Arreglando archivo: {file_path}")
    
    try:
        # Leer el archivo original
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hacer una copia de respaldo
        backup_path = file_path + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Copia de seguridad creada en {backup_path}")
        
        # Corregir el encabezado para asegurar que especifica UTF-8 correctamente
        fixed_content = re.sub(
            r'(Content-Type:\s*text/plain;\s*charset=)([^\n]+)',
            r'\1UTF-8',
            content
        )
        
        # Normalizar los finales de línea a LF (Linux style)
        fixed_content = fixed_content.replace('\r\n', '\n')
        
        # Verificar y arreglar comillas no balanceadas en entradas msgid/msgstr
        lines = fixed_content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if (line.startswith('msgid "') or line.startswith('msgstr "')) and not line.endswith('"'):
                # Arreglar línea que no termina en comillas
                fixed_line = line + '"'
                print(f"  ✓ Arreglada línea sin comillas de cierre: {line}")
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        
        fixed_content = '\n'.join(fixed_lines)
        
        # Escribir el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"  ✓ Archivo guardado correctamente")
        return True
    
    except Exception as e:
        print(f"  ✗ Error al procesar {file_path}: {e}")
        return False

def main():
    """Procesa todos los archivos .po en la estructura de locale"""
    locale_dir = 'locale'
    success_count = 0
    error_count = 0
    
    print("="*60)
    print("REPARADOR DE ARCHIVOS .PO PARA DJANGO")
    print("="*60)
    
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                file_path = os.path.join(root, file)
                if fix_po_file(file_path):
                    success_count += 1
                else:
                    error_count += 1
    
    print("\n" + "="*60)
    print(f"Proceso completado: {success_count} archivos arreglados, {error_count} errores")
    print("="*60)
    
    if success_count > 0:
        print("\nAhora intenta compilar las traducciones nuevamente con el comando:")
        print("python manage.py compilemessages")
        
    if error_count > 0:
        print("\nAlternativa: edita manualmente los archivos .po para corregir problemas")

if __name__ == "__main__":
    main()
