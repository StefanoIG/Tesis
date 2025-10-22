#!/usr/bin/env python
import os
import sys
import django
import warnings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from drf_spectacular.generators import SchemaGenerator
from django.http import HttpRequest
from unittest.mock import Mock

# Create a mock request
request = Mock(spec=HttpRequest)
request.method = 'GET'
request.META = {}
request.user = Mock()
request.user.is_authenticated = False

try:
    gen = SchemaGenerator()
    schema = gen.get_schema(request=request, public=True)
    print("✓ Schema generated successfully!")
    print(f"  - Endpoints: {len(schema['paths'])}")
    
    # Print paths grouped by tag
    tags = {}
    for path, methods in schema['paths'].items():
        for method, details in methods.items():
            if 'tags' in details and details['tags']:
                tag = details['tags'][0]
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(f"{method.upper()} {path}")
    
    print("\nEndpoints by tag:")
    for tag in sorted(tags.keys()):
        print(f"\n  {tag}:")
        for endpoint in sorted(tags[tag])[:5]:
            print(f"    - {endpoint}")
        if len(tags[tag]) > 5:
            print(f"    ... and {len(tags[tag]) - 5} more")
    
except Exception as e:
    print(f"✗ Error generating schema:")
    print(f"  {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
