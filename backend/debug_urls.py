#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trazabilidad_agroindustrial.settings')
django.setup()

from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def print_urls(patterns, prefix=""):
    """Recursively print all URL patterns"""
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            # It's an include()
            new_prefix = prefix + str(pattern.pattern)
            print_urls(pattern.url_patterns, new_prefix)
        elif isinstance(pattern, URLPattern):
            # It's a direct pattern
            full_path = prefix + str(pattern.pattern)
            callback = pattern.callback
            if hasattr(callback, 'cls'):
                print(f"  {full_path:60} -> {callback.cls.__name__}")
            else:
                print(f"  {full_path:60} -> {callback}")

print("All registered URL patterns:")
resolver = get_resolver()
print_urls(resolver.url_patterns)
