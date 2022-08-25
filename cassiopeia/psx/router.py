
import builtins

__old_import__ = __import__

def import_router(name, locals, globals, fromlist, level):
    print(f'name: {name!r}')
    print(f'fromlist: {fromlist}')
    print(f'level: {level}')
    return __old_import__(name, locals, globals, fromlist, level)

def init_router():
    builtins.__import__ = import_router
def restore_router():
    builtins.__import__ = __old_import__
