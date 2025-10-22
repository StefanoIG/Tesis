#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from drf_spectacular.generators import SchemaGenerator

try:
    gen = SchemaGenerator()
    # Don't pass request, let it create its own
    schema = gen.get_schema(public=True)
    print("Schema generated successfully!")
    print(f"Endpoints: {len(schema['paths'])}")
    
    # Print all paths
    print("\nAll endpoints:")
    for i, path in enumerate(sorted(schema['paths'].keys()), 1):
        print(f"  {i}. {path}")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
