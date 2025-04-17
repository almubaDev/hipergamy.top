"""
Script para corregir el error específico de línea en el archivo de traducciones
"""
import os

def fix_line_133_error():
    """Corrige el error específico en la línea 133 del archivo de traducciones en español"""
    file_path = 'locale/es/LC_MESSAGES/django.po'
    print(f"Corrigiendo error en {file_path}")
    
    try:
        # Leer el archivo línea por línea
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Crear copia de seguridad
        backup_path = file_path + '.line_error_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"  ✓ Copia de seguridad guardada: {backup_path}")
        
        # Encontrar y corregir el error específico
        error_fixed = False
        
        for i, line in enumerate(lines):
            # Buscar la línea con el error: msgid con comillas sin cerrar
            if line.startswith('msgstr "\\') and not line.endswith('"\n'):
                print(f"  ✓ Encontrada línea con error en línea {i+1}: {line.strip()}")
                # Corregir la línea añadiendo la comilla de cierre
                lines[i] = 'msgstr "Subir de nivel fue como desbloquear un nuevo mundo. No todos los hombres valen la pena... pero los que lo hacen, están aquí."\n'
                error_fixed = True
                print(f"  ✓ Línea corregida a: {lines[i].strip()}")
                break
        
        # Si no se encontró esa línea específica, buscar cualquier línea con error similar
        if not error_fixed:
            for i, line in enumerate(lines):
                if (line.startswith('msgid') or line.startswith('msgstr')) and '"' in line and not line.endswith('"\n') and not line.endswith('\\"\n'):
                    print(f"  ✓ Encontrada línea con posible error en línea {i+1}: {line.strip()}")
                    
                    # Si la línea habla de "Subir de nivel...", es la que buscamos
                    if "Subir de nivel" in line or "desbloquear un nuevo mundo" in line:
                        if line.startswith('msgid'):
                            # Si es msgid, lo dejamos intacto ya que el problema está en msgstr
                            continue
                        
                        # Corregir msgstr
                        lines[i] = 'msgstr "Subir de nivel fue como desbloquear un nuevo mundo. No todos los hombres valen la pena... pero los que lo hacen, están aquí."\n'
                        error_fixed = True
                        print(f"  ✓ Línea corregida a: {lines[i].strip()}")
                        break
        
        # Guardar el archivo corregido
        if error_fixed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"  ✓ Archivo guardado con correcciones")
        else:
            print(f"  ✗ No se encontró la línea con el error específico")
        
        return error_fixed
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    print("="*60)
    print("CORRECCIÓN DE ERROR ESPECÍFICO EN LÍNEA")
    print("="*60)
    
    # Eliminar archivos .mo existentes
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            try:
                os.remove(mo_path)
                print(f"Eliminado: {mo_path}")
            except:
                print(f"No se pudo eliminar: {mo_path}")
    
    # Corregir el error específico
    if fix_line_133_error():
        print("\n✅ Error corregido correctamente")
        print("\nAhora ejecuta este comando para compilar:")
        print("msgfmt -o locale/es/LC_MESSAGES/django.mo locale/es/LC_MESSAGES/django.po")
        print("msgfmt -o locale/en/LC_MESSAGES/django.mo locale/en/LC_MESSAGES/django.po")
    else:
        print("\n⚠️ No se pudo corregir el error automáticamente")
        print("\nDeberás editar manualmente el archivo locale/es/LC_MESSAGES/django.po")
        print("y corregir la línea 133 que tiene un error de comillas sin cerrar.")

if __name__ == "__main__":
    main()
