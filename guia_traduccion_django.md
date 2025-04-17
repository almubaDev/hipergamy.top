# Guía de Traducciones en Django

## Flujo de trabajo para internacionalización

Cuando añadas nuevas páginas o textos a tu proyecto, debes seguir este flujo de trabajo:

### 1. Marcar texto para traducción en las plantillas

```html
<!-- En los templates -->
{% trans "Texto a traducir" %}

<!-- Para bloques más largos -->
{% blocktrans %}
Este es un texto más largo
que ocupa varias líneas
{% endblocktrans %}
```

### 2. Marcar texto para traducción en Python

```python
from django.utils.translation import gettext as _

# En código Python
mensaje = _("Texto a traducir")
```

### 3. Extraer mensajes a archivos .po (automatizado)

Django tiene un comando que automáticamente extrae todos los textos marcados para traducción:

```bash
python manage.py makemessages -l es  # Para español
python manage.py makemessages -l en  # Para inglés

# Para extraer de todos los idiomas configurados:
python manage.py makemessages -a
```

Este comando:
- Busca en todas las plantillas y archivos Python
- Extrae textos marcados para traducción
- Actualiza los archivos .po (crea nuevos msgid para textos nuevos)
- Mantiene las traducciones existentes

### 4. Editar traducciones

Una vez actualizado el archivo .po, puedes editar las traducciones manualmente.
También existen herramientas como [Poedit](https://poedit.net/) que facilitan esta tarea.

### 5. Compilar mensajes a archivos .mo

```bash
python manage.py compilemessages
```

## Automatización de todo el proceso

Para automatizar completamente el proceso, puedes crear un script:

```python
# update_translations.py
import os
import subprocess

def update_translations():
    """Actualiza los archivos de traducción del proyecto"""
    # 1. Extraer mensajes de todas las plantillas y archivos Python
    subprocess.run(['python', 'manage.py', 'makemessages', '-a'])
    
    # 2. Compilar los mensajes a archivos .mo
    subprocess.run(['python', 'manage.py', 'compilemessages'])
    
    print("✅ Traducciones actualizadas correctamente")

if __name__ == "__main__":
    update_translations()
```

Este script puedes ejecutarlo cada vez que actualices el contenido:

```bash
python update_translations.py
```

## Buenas prácticas

1. **Mantén las cadenas de traducción simples**: Evita incluir HTML en las cadenas de traducción.

2. **Usa contexto cuando sea necesario**: Si la misma palabra puede tener diferentes significados:
   ```python
   _("May", "month_name")  # Mayo (mes)
   _("May", "verb")        # Puede (verbo)
   ```

3. **Actualiza traducciones frecuentemente**: Es más fácil traducir pocas cadenas regularmente que muchas de golpe.

4. **Usa nombres descriptivos**: Para bloques largos, usa nombres que ayuden a identificar el contenido:
   ```html
   {% blocktrans trimmed context "homepage-welcome" %}
   Bienvenido a nuestra aplicación...
   {% endblocktrans %}
   ```

5. **Revisa las advertencias**: El comando makemessages muestra advertencias cuando encuentra problemas.

## Herramientas adicionales

- **django-rosetta**: Una interfaz web para editar traducciones directamente en tu aplicación Django.
- **Poedit**: Editor de archivos .po con interfaz gráfica.
- **Weblate**: Plataforma completa de traducción para proyectos más grandes.
