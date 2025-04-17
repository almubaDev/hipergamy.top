#!/usr/bin/env python
"""
Script para automatizar el proceso de actualización de traducciones en Django.

Este script:
1. Extrae todos los textos marcados para traducción
2. Compila los mensajes a archivos .mo
3. Hace una copia de seguridad de los archivos existentes

Uso:
    python update_translations.py
"""
import os
import subprocess
import datetime
import shutil

def backup_translation_files():
    """Hace una copia de seguridad de los archivos de traducción existentes"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"locale/backup_{timestamp}"
    
    # Crear directorio de backup si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Hacer backup de los archivos .po
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if os.path.exists(po_path):
            backup_po = f"{backup_dir}/{lang}_django.po"
            shutil.copy2(po_path, backup_po)
            print(f"✓ Backup creado: {backup_po}")
    
    return backup_dir

def extract_translation_messages():
    """Extrae mensajes para traducción de todas las plantillas y archivos Python"""
    print("\n=== Extrayendo mensajes para traducción ===")
    
    # Ejecutar makemessages para todos los idiomas configurados
    result = subprocess.run(
        ['python', 'manage.py', 'makemessages', '-a', '--verbosity=1'], 
        capture_output=True, 
        text=True
    )
    
    # Mostrar salida
    if result.stdout:
        print(result.stdout)
    
    # Mostrar errores si los hay
    if result.stderr:
        print("ERRORES:")
        print(result.stderr)
    
    return result.returncode == 0

def compile_messages():
    """Compila los archivos .po a .mo"""
    print("\n=== Compilando mensajes ===")
    
    # Primero eliminar archivos .mo existentes para evitar problemas
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            os.remove(mo_path)
            print(f"✓ Eliminado archivo .mo antiguo: {mo_path}")
    
    # Intentar compilar usando el comando de Django
    django_compile = subprocess.run(
        ['python', 'manage.py', 'compilemessages', '--verbosity=1'],
        capture_output=True,
        text=True
    )
    
    # Mostrar salida
    if django_compile.stdout:
        print(django_compile.stdout)
    
    # Si hay errores con Django compilemessages, intenta usar msgfmt directamente
    if django_compile.returncode != 0:
        print("Intentando compilar con msgfmt directamente...")
        
        # Verificar si msgfmt está disponible
        try:
            subprocess.run(['msgfmt', '--version'], capture_output=True, check=True)
            msgfmt_available = True
        except (subprocess.SubprocessError, FileNotFoundError):
            msgfmt_available = False
        
        if msgfmt_available:
            for lang in ['es', 'en']:
                po_path = f'locale/{lang}/LC_MESSAGES/django.po'
                mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
                
                if os.path.exists(po_path):
                    result = subprocess.run(
                        ['msgfmt', '-o', mo_path, po_path],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print(f"✓ Compilado {po_path} → {mo_path}")
                    else:
                        print(f"✗ Error al compilar {po_path}:")
                        if result.stderr:
                            print(result.stderr)
        else:
            print("✗ msgfmt no está disponible en el sistema")
            return False
    
    # Verificar que se crearon los archivos .mo
    success = True
    for lang in ['es', 'en']:
        mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'
        if os.path.exists(mo_path):
            size = os.path.getsize(mo_path)
            print(f"✓ {mo_path} creado correctamente ({size} bytes)")
        else:
            print(f"✗ No se pudo crear {mo_path}")
            success = False
    
    return success

def fix_common_errors():
    """Corrige errores comunes en los archivos .po"""
    print("\n=== Corrigiendo errores comunes ===")
    
    for lang in ['es', 'en']:
        po_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if not os.path.exists(po_path):
            continue
            
        print(f"Revisando {po_path}...")
        
        # Leer contenido del archivo
        with open(po_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Comprobar y corregir error común: líneas con comillas sin cerrar
        lines = content.split('\n')
        fixed_lines = []
        fixed = False
        
        for i, line in enumerate(lines):
            if (line.startswith('msgid "') or line.startswith('msgstr "')) and not line.endswith('"') and not line.endswith('\\"'):
                # Cerrar las comillas
                fixed_line = line + '"'
                fixed_lines.append(fixed_line)
                print(f"✓ Línea {i+1} corregida: añadida comilla de cierre")
                fixed = True
            else:
                fixed_lines.append(line)
        
        # Guardar cambios si hubo correcciones
        if fixed:
            with open(po_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines))
            print(f"✓ Guardado {po_path} con correcciones")

def main():
    """Función principal para actualizar las traducciones"""
    print("="*60)
    print("ACTUALIZACIÓN DE TRADUCCIONES DJANGO")
    print("="*60)
    
    # 1. Hacer backup de los archivos existentes
    print("\n=== Creando copias de seguridad ===")
    backup_dir = backup_translation_files()
    
    # 2. Extraer mensajes para traducción
    if not extract_translation_messages():
        print("\n✗ Error al extraer mensajes para traducción")
        return
    
    # 3. Corregir errores comunes
    fix_common_errors()
    
    # 4. Compilar mensajes
    if compile_messages():
        print("\n✅ TRADUCCIONES ACTUALIZADAS CORRECTAMENTE")
        print(f"\nCopias de seguridad guardadas en: {backup_dir}")
        print("\nAhora puedes iniciar el servidor con: python manage.py runserver")
    else:
        print("\n⚠️ HUBO PROBLEMAS AL COMPILAR LOS MENSAJES")
        print("\nPosibles soluciones:")
        print("1. Asegúrate de tener gettext instalado: https://mlocati.github.io/articles/gettext-iconv-windows.html")
        print("2. Comprueba si hay errores en los archivos .po")
        print(f"3. Restaura los archivos de backup desde: {backup_dir}")

if __name__ == "__main__":
    main()
