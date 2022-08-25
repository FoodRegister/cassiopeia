
import builtins
import importlib
import os

from cassiopeia.psx.transpile import transpile_file

__old_import__ = __import__

CASSIOPEIA_PSX_CONFIG = []

__directory__ = os.path.dirname(__file__)
__cache_dir__ = os.path.join(__directory__, "__cassiopeia_cache_dir__")

if not os.path.exists(__cache_dir__): os.mkdir(__cache_dir__)

def import_router(name, locals, globals, fromlist, level):
    for psx_folder in CASSIOPEIA_PSX_CONFIG:
        if name.startswith(psx_folder + '.'):
            break
    else: return __old_import__(name, locals, globals, fromlist, level)

    file_data = transpile_file(os.path.abspath(os.path.join(*name.split(".")) + '.py'))
    
    cache_path = os.path.join(__cache_dir__, os.path.join(*name.split(".")) + '.py')
    if not os.path.exists(os.path.dirname(cache_path)): os.makedirs(os.path.dirname(cache_path))
    
    with open(cache_path, 'wb') as f:
        f.write(file_data)
    
    return __old_import__(
        'cassiopeia.psx.__cassiopeia_cache_dir__.' + name,
        locals, globals, fromlist, level
    )

def init_router(config):
    global CASSIOPEIA_PSX_CONFIG
    CASSIOPEIA_PSX_CONFIG = config

    builtins.__import__ = import_router
def restore_router():
    builtins.__import__ = __old_import__
