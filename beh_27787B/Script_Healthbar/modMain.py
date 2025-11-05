# -*- coding: utf-8 -*-
from .QuModLibs.QuMod import *

miniMod = EasyMod()


@PRE_SERVER_LOADER_HOOK
def SERVER_LOADER():
    # miniMod.Server("Server")
    miniMod.regNativePyServer()
    pass


@PRE_CLIENT_LOADER_HOOK
def CLIENT_LOADER():
    # miniMod.Client("Client")
    pass
