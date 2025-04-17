"""
Script definitivo para arreglar todos los problemas en los archivos .po
"""
import os
import sys
import re

def fix_po_file(file_path):
    """Corrige varios problemas típicos en archivos .po de Django"""
    print(f"Procesando: {file_path}")
    
    try:
        # Leer el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Crear copia de seguridad
        backup_path = file_path + '.final_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Backup creado: {backup_path}")
        
        # 1. Corregir el encabezado
        lang = 'es' if '/es/' in file_path else 'en'
        new_header = f"""# Translation for Hypergamy.
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
        
        # Encontrar el final del encabezado
        header_end_index = content.find('msgid "', content.find('msgstr "'))
        if header_end_index == -1:
            header_end_index = content.find('msgid "')
        
        if header_end_index > 0:
            # Eliminar el encabezado existente y añadir el nuevo
            content = new_header + content[header_end_index:]
            print("  ✓ Encabezado corregido")
        
        # 2. Arreglar líneas con error de comillas
        lines = content.split('\n')
        fixed_lines = []
        line_fixed = False
        
        for i, line in enumerate(lines):
            # Buscar líneas con comillas de apertura pero sin cierre
            if line.startswith('msgstr "') and not line.endswith('"') and not line.endswith('\\"'):
                # Corregir la línea específica del testimonio
                if "Subir de nivel" in line or "desbloquear un nuevo mundo" in line:
                    fixed_line = 'msgstr "Subir de nivel fue como desbloquear un nuevo mundo. No todos los hombres valen la pena... pero los que lo hacen, están aquí."'
                    fixed_lines.append(fixed_line)
                    print(f"  ✓ Línea {i+1} corregida: {line} -> {fixed_line}")
                    line_fixed = True
                # Para otras líneas, simplemente añadir la comilla de cierre
                else:
                    fixed_line = line + '"'
                    fixed_lines.append(fixed_line)
                    print(f"  ✓ Añadida comilla de cierre en línea {i+1}")
                    line_fixed = True
            else:
                fixed_lines.append(line)
        
        if line_fixed:
            content = '\n'.join(fixed_lines)
            print("  ✓ Líneas con errores de comillas corregidas")
        
        # 3. Eliminar entradas duplicadas
        entries = []
        current_entry = {"msgid": "", "msgstr": "", "comments": []}
        entry_start = False
        
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Saltar líneas vacías
            if not line:
                i += 1
                continue
            
            # Capturar comentarios
            if line.startswith('#'):
                if entry_start:
                    # Nuevo comentario, nueva entrada
                    if current_entry["msgid"] and current_entry["msgstr"]:
                        entries.append(current_entry)
                    current_entry = {"msgid": "", "msgstr": "", "comments": [line]}
                    entry_start = False
                else:
                    current_entry["comments"].append(line)
            
            # Capturar msgid
            elif line.startswith('msgid "'):
                if entry_start and current_entry["msgid"] and current_entry["msgstr"]:
                    # Nueva entrada
                    entries.append(current_entry)
                    current_entry = {"msgid": "", "msgstr": "", "comments": []}
                
                entry_start = True
                msgid_content = line[7:-1] if line.endswith('"') else line[7:]
                current_entry["msgid"] = msgid_content
                
                # Continuar leyendo posibles líneas de continuación
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('"') and lines[j].strip().endswith('"'):
                    current_entry["msgid"] += lines[j].strip()[1:-1]
                    j += 1
                i = j - 1
            
            # Capturar msgstr
            elif line.startswith('msgstr "'):
                msgstr_content = line[8:-1] if line.endswith('"') else line[8:]
                current_entry["msgstr"] = msgstr_content
                
                # Continuar leyendo posibles líneas de continuación
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith('"') and lines[j].strip().endswith('"'):
                    current_entry["msgstr"] += lines[j].strip()[1:-1]
                    j += 1
                i = j - 1
            
            i += 1
        
        # Añadir la última entrada
        if current_entry["msgid"] and current_entry["msgstr"]:
            entries.append(current_entry)
        
        # Eliminar duplicados
        unique_entries = {}
        duplicate_count = 0
        
        for entry in entries:
            if entry["msgid"] == "":
                # Encabezado, lo ignoramos ya que lo reemplazamos antes
                continue
            
            if entry["msgid"] not in unique_entries:
                unique_entries[entry["msgid"]] = entry
            else:
                duplicate_count += 1
        
        if duplicate_count > 0:
            print(f"  ✓ Se encontraron y eliminaron {duplicate_count} entradas duplicadas")
        
        # Reconstruir el contenido sin duplicados
        new_content = new_header
        
        for msgid, entry in unique_entries.items():
            for comment in entry["comments"]:
                new_content += comment + "\n"
            
            new_content += f'msgid "{entry["msgid"]}"\n'
            new_content += f'msgstr "{entry["msgstr"]}"\n\n'
        
        # Guardar el archivo corregido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ Archivo guardado correctamente")
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("="*60)
    print("CORRECCIÓN DEFINITIVA DE ARCHIVOS .PO")
    print("="*60)
    
    # 1. Eliminar archivos .mo existentes
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            try:
                os.remove(mo_path)
                print(f"Eliminado: {mo_path}")
            except:
                print(f"No se pudo eliminar: {mo_path}")
    
    # 2. Procesar cada archivo .po
    success = True
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if not fix_po_file(po_path):
            success = False
    
    # 3. Instrucciones finales
    if success:
        print("\n✅ ARCHIVOS .PO CORREGIDOS CORRECTAMENTE")
        print("\nAhora ejecuta estos comandos para compilar los archivos .mo:")
        print("msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po")
        print("msgfmt -o locale/en/LC_MESSAGES/django.mo locale/en/LC_MESSAGES/django.po")
        print("\nLuego inicia el servidor Django:")
        print("python manage.py runserver")
    else:
        print("\n⚠️ HUBO PROBLEMAS AL CORREGIR ALGUNOS ARCHIVOS")
        print("\nIntenta editar manualmente los archivos .po para corregir los errores")

if __name__ == "__main__":
    main()
