"""
Module `ui` contains user interface components for the admin
cogs. These are subclasses relevant classes in `source.abc`.

This module is separate from `bot` because it simply provides
a client-side interface. Some pieces of logic are, however,
executed within callbacks.
"""
from .views import *