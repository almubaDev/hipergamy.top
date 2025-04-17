"""
Script para compilar archivos .po a .mo usando polib
"""
import os
import polib
import sys

def compile_with_polib(po_path, mo_path):
    """Compila un archivo .po a .mo usando polib directamente"""
    print(f"Compilando: {po_path}")
    try:
        # Primero eliminamos el archivo .mo si existe
        if os.path.exists(mo_path):
            os.remove(mo_path)
            print(f"  ✓ Eliminado archivo .mo antiguo")
        
        # Cargar el archivo .po con polib
        po = polib.pofile(po_path)
        
        # Guardar como .mo
        po.save_as_mofile(mo_path)
        
        # Verificar que se creó el archivo
        if os.path.exists(mo_path):
            size = os.path.getsize(mo_path)
            print(f"  ✓ Archivo .mo creado correctamente ({size} bytes)")
            return True
        else:
            print(f"  ✗ No se pudo crear el archivo .mo")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Compila todos los archivos .po a .mo usando polib"""
    locale_dir = 'locale'
    success = True
    
    print("="*60)
    print("COMPILADOR DE ARCHIVOS .PO A .MO USANDO POLIB")
    print("="*60)
    
    for lang in ['es', 'en']:
        po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_path):
            if not compile_with_polib(po_path, mo_path):
                success = False
        else:
            print(f"  ✗ No se encontró el archivo .po: {po_path}")
            success = False
    
    if success:
        print("\n✅ Todos los archivos fueron compilados correctamente")
        print("\nAhora puedes iniciar el servidor con:")
        print("python manage.py runserver")
    else:
        print("\n❌ Hubo problemas al compilar algunos archivos")
        print("\nProblemas comunes y soluciones:")
        print("1. Asegúrate de tener instalado polib: pip install polib")
        print("2. Verifica que los archivos .po no tengan errores")
        print("3. Asegúrate de tener permisos de escritura en la carpeta")

if __name__ == "__main__":
    main()
