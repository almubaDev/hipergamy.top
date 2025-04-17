"""
Script para arreglar específicamente los encabezados de los archivos .po
"""
import os

def fix_headers_manually():
    """Corrige manualmente los encabezados de los archivos .po"""
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        print(f"Arreglando encabezado de {po_path}")
        
        # Leer todo el contenido
        try:
            with open(po_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear una copia de seguridad
            backup_path = po_path + '.manual_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Copia de seguridad guardada en {backup_path}")
            
            # Reemplazar el encabezado completo
            new_header = f'''# Translation for Hypergamy.
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

'''

            # Encontrar el final del encabezado actual
            header_end_pos = content.find('msgid "', content.find('msgstr "'))
            if header_end_pos == -1:
                header_end_pos = content.find('msgid "')
            
            if header_end_pos > 0:
                # Reemplazar el encabezado antiguo con el nuevo
                new_content = new_header + content[header_end_pos:]
                
                # Guardar el archivo con el encabezado corregido
                with open(po_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✓ Encabezado reemplazado correctamente")
            else:
                print(f"  ✗ No se pudo encontrar el final del encabezado")
                
        except Exception as e:
            print(f"  ✗ Error al procesar {po_path}: {e}")

def main():
    print("="*60)
    print("CORRECCIÓN MANUAL DE ENCABEZADOS .PO")
    print("="*60)
    
    # Primero eliminar los archivos .mo existentes
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            try:
                os.remove(mo_path)
                print(f"Eliminado: {mo_path}")
            except:
                print(f"No se pudo eliminar: {mo_path}")
    
    # Corregir los encabezados
    fix_headers_manually()
    
    print("\nAhora ejecuta este comando exactamente:")
    print("msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po")
    print("msgfmt -o locale/en/LC_MESSAGES/django.mo locale/en/LC_MESSAGES/django.po")
    print("\nLuego inicia el servidor:")
    print("python manage.py runserver")

if __name__ == "__main__":
    main()
