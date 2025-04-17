import os
import sys
import polib

def compile_po_files():
    """Compile all .po files to .mo files."""
    locale_dirs = ['locale/es/LC_MESSAGES', 'locale/en/LC_MESSAGES']
    
    for locale_dir in locale_dirs:
        print(f"Checking directory: {locale_dir}")
        if not os.path.exists(locale_dir):
            print(f"Directory {locale_dir} does not exist.")
            continue
            
        po_files = [f for f in os.listdir(locale_dir) if f.endswith('.po')]
        print(f"Found .po files: {po_files}")
        
        if not po_files:
            print(f"No .po files found in {locale_dir}")
            continue
            
        for po_file in po_files:
            po_path = os.path.join(locale_dir, po_file)
            mo_path = po_path.replace('.po', '.mo')
            
            try:
                po = polib.pofile(po_path)
                po.save_as_mofile(mo_path)
                print(f"Compiled {po_path} to {mo_path}")
                # Verify the file was created
                if os.path.exists(mo_path):
                    print(f"Success! {mo_path} exists with size {os.path.getsize(mo_path)} bytes")
                else:
                    print(f"ERROR: {mo_path} was not created!")
            except Exception as e:
                print(f"Error compiling {po_path}: {e}")

if __name__ == "__main__":
    compile_po_files()
