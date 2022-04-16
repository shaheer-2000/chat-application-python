import sys
import os

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

print(is_venv())
print(os.environ['VIRTUAL_ENV'])