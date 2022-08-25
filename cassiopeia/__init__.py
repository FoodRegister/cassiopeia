
import cassiopeia.psx
import cassiopeia.psx.router

def init_cassiopeia(router_conf=[]):
    cassiopeia.psx.router.init_router(router_conf)

def restore_cassiopeia():
    cassiopeia.psx.router.restore_router()
