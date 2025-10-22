#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        # Borrar la tabla
        cursor.execute("DROP TABLE IF EXISTS envios")
        print("✓ Tabla envios eliminada")
        
        # Recrearla via syncdb
        from django.core.management import call_command
        call_command('migrate', 'logistica', verbosity=0)
        print("✓ Tabla envios recreada")
    except Exception as e:
        print(f"✗ Error: {e}")
