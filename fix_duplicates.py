"""
Script para eliminar mensajes duplicados en archivos .po
"""
import os
import re

def remove_duplicate_entries(file_path):
    """Elimina entradas duplicadas de un archivo .po"""
    print(f"Procesando archivo: {file_path}")
    
    try:
        # Leer el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Crear copia de seguridad
        backup_path = file_path + '.nodupes_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Copia de seguridad guardada: {backup_path}")
        
        # Dividir el contenido en bloques de mensajes
        # Identificamos el encabezado y los bloques de mensajes
        header_match = re.search(r'^(.*?msgid "".*?msgstr "".*?)(\n\n|\n#|$)', content, re.DOTALL)
        
        if not header_match:
            print("  ✗ No se pudo identificar el encabezado del archivo")
            return False
        
        header = header_match.group(1)
        
        # Extraer todos los bloques msgid/msgstr
        blocks = re.findall(r'(msgid ".*?"(?:\n".*?")*\nmsgstr ".*?"(?:\n".*?")*)', content, re.DOTALL)
        
        # Diccionario para almacenar mensajes únicos
        unique_msgs = {}
        duplicates = 0
        
        # Extraer los msgid de cada bloque
        for block in blocks:
            msgid_match = re.search(r'msgid "(.*?)"(?:\n"(.*?)")*', block, re.DOTALL)
            if msgid_match:
                # Reconstruir el msgid completo (puede estar en múltiples líneas)
                if msgid_match.group(2):
                    msgid = msgid_match.group(1) + msgid_match.group(2)
                else:
                    msgid = msgid_match.group(1)
                
                # Si es un msgid vacío, es parte del encabezado, lo ignoramos
                if msgid == "":
                    continue
                
                # Si ya hemos visto este msgid, es un duplicado
                if msgid in unique_msgs:
                    duplicates += 1
                    print(f"  ✓ Encontrado duplicado: \"{msgid}\"")
                else:
                    unique_msgs[msgid] = block
        
        # Si no hay duplicados, no es necesario hacer nada
        if duplicates == 0:
            print(f"  ✓ No se encontraron duplicados en este archivo")
            return True
        
        # Reconstruir el archivo sin duplicados
        new_content = header + "\n\n"
        for block in unique_msgs.values():
            new_content += block + "\n\n"
        
        # Guardar el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ Se eliminaron {duplicates} mensajes duplicados")
        return True
        
    except Exception as e:
        print(f"  ✗ Error al procesar el archivo: {e}")
        return False

def main():
    print("="*60)
    print("ELIMINACIÓN DE MENSAJES DUPLICADOS EN ARCHIVOS .PO")
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
    
    # Procesar archivos .po para eliminar duplicados
    success = True
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if not remove_duplicate_entries(po_path):
            success = False
    
    if success:
        print("\n✅ Archivos procesados correctamente")
    else:
        print("\n⚠️ Hubo problemas al procesar algunos archivos")
    
    print("\nAhora ejecuta estos comandos para compilar los archivos .mo:")
    print("msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po")
    print("msgfmt -o locale/en/LC_MESSAGES/django.mo locale/en/LC_MESSAGES/django.po")

if __name__ == "__main__":
    main()
