"""
Solución manual para corregir los archivos de traducción
"""
import os

def rewrite_po_file(lang):
    """Reescribe el archivo .po con formato correcto para asegurar compatibilidad"""
    po_path = f'locale/{lang}/LC_MESSAGES/django.po'
    
    print(f"Reescribiendo archivo {po_path}...")
    
    # Encabezado corregido
    header = f"""# Translation for Hypergamy.
# Copyright (C) 2025 Hypergamy Team
msgid ""
msgstr ""
"Project-Id-Version: 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-04-15 12:00+0000\\n"
"PO-Revision-Date: 2025-04-15 12:00+0000\\n"
"Last-Translator: Dev <dev@example.com>\\n"
"Language-Team: {lang.upper()}\\n"
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"
"""
    
    # Leer las traducciones existentes, saltando el encabezado actual
    translations = []
    in_header = True
    
    try:
        with open(po_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Ya pasamos el encabezado cuando llegamos a la primera entrada msgid
                if in_header and line.startswith('msgid "') and not line.startswith('msgid ""'):
                    in_header = False
                
                if not in_header:
                    translations.append(line)
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return False
    
    # Crear un archivo nuevo con el encabezado corregido y las traducciones
    try:
        backup_path = po_path + '.original'
        if not os.path.exists(backup_path):
            with open(po_path, 'r', encoding='utf-8') as orig:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(orig.read())
            print(f"  ✓ Backup creado: {backup_path}")
        
        with open(po_path, 'w', encoding='utf-8') as f:
            f.write(header)
            f.writelines(translations)
        
        print(f"  ✓ Archivo {po_path} reescrito correctamente")
        return True
    except Exception as e:
        print(f"Error escribiendo archivo: {e}")
        return False

def delete_mo_files():
    """Elimina los archivos .mo existentes"""
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            try:
                os.remove(mo_path)
                print(f"Eliminado archivo {mo_path}")
            except Exception as e:
                print(f"Error eliminando {mo_path}: {e}")

def main():
    print("="*60)
    print("SOLUCIÓN MANUAL PARA LOS ARCHIVOS DE TRADUCCIÓN")
    print("="*60)
    
    print("\n1. Eliminando archivos .mo existentes...")
    delete_mo_files()
    
    print("\n2. Reescribiendo archivos .po con formato correcto...")
    for lang in ['es', 'en']:
        rewrite_po_file(lang)
    
    print("\n3. Instrucciones:")
    print("   - Ejecuta: python manage.py compilemessages")
    print("   - Luego inicia el servidor: python manage.py runserver")
    
    print("\n"+"="*60)

if __name__ == "__main__":
    main()
