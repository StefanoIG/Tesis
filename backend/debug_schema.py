#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from drf_spectacular.generators import SchemaGenerator
from django.urls import get_resolver

try:
    gen = SchemaGenerator()
    schema = gen.get_schema()
    print("✓ Schema generated successfully!")
    print(f"  - Endpoints: {len(schema['paths'])}")
    print("\nEndpoints in schema:")
    for path in sorted(schema['paths'].keys())[:10]:
        print(f"  - {path}")
    
    # Also check registered URLs
    print("\n\nRegistered URL patterns:")
    resolver = get_resolver()
    patterns = resolver.url_patterns
    print(f"  Total patterns: {len(patterns)}")
    
except Exception as e:
    print(f"✗ Error generating schema:")
    print(f"  {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
