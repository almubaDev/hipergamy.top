"""
Script para arreglar problemas de codificación en archivos .po
"""
import os
import re

def fix_po_file_encoding(file_path):
    """Arregla problemas de codificación en archivos .po"""
    print(f"Arreglando archivo: {file_path}")
    
    try:
        # Leer el archivo original
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Hacer una copia de respaldo
        backup_path = file_path + '.bak2'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Copia de seguridad creada en {backup_path}")
        
        # Arreglar el encabezado de codificación
        # Problema identificado: "UTF-Content-Transfer-Encoding: 8bit" es un encoding inválido
        # Corregimos los encabezados importantes
        header_fixed = False
        
        # Arreglar primero el Content-Type si está mal
        if "Content-Type: text/plain; charset=UTF" in content and not "Content-Type: text/plain; charset=UTF-8" in content:
            content = content.replace(
                "Content-Type: text/plain; charset=UTF", 
                "Content-Type: text/plain; charset=UTF-8"
            )
            header_fixed = True
            print("  ✓ Arreglado Content-Type")
        
        # Asegurarnos que Content-Transfer-Encoding esté en una línea separada
        if "UTF-Content-Transfer-Encoding: 8bit" in content:
            content = content.replace(
                "UTF-Content-Transfer-Encoding: 8bit", 
                "UTF-8\nContent-Transfer-Encoding: 8bit"
            )
            header_fixed = True
            print("  ✓ Separada la línea de Content-Transfer-Encoding")
        
        # Eliminar el archivo .mo para estar seguros
        mo_path = file_path.replace('.po', '.mo')
        if os.path.exists(mo_path):
            os.remove(mo_path)
            print(f"  ✓ Eliminado archivo .mo antiguo")
        
        # Guardar el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if header_fixed:
            print("  ✓ Archivo guardado con encabezados corregidos")
        else:
            print("  ✓ No se encontraron problemas de encabezado para corregir")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Arregla todos los archivos .po en la estructura de directorios locale"""
    locale_dir = 'locale'
    success = True
    
    print("="*60)
    print("CORRECTOR DE ENCODINGS PARA ARCHIVOS .PO DE DJANGO")
    print("="*60)
    
    for lang in ['es', 'en']:
        po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        
        if os.path.exists(po_path):
            if not fix_po_file_encoding(po_path):
                success = False
        else:
            print(f"  ✗ No se encontró el archivo .po: {po_path}")
            success = False
    
    if success:
        print("\n✅ Todos los archivos fueron corregidos correctamente")
        print("\nAhora compila las traducciones con:")
        print("python manage.py compilemessages")
    else:
        print("\n❌ Hubo problemas al corregir algunos archivos")

if __name__ == "__main__":
    main()
