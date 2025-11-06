# -*- coding: utf-8 -*-
from .QuModLibs.QuMod import *

miniMod = EasyMod()

# 服务端
miniMod.regNativePyServer("lemonUHB", "UHBServer",
                          "Vanilla.vanillaBroadcastServer.VanillaBroadcastServer")

# 客户端
miniMod.Client("UHB.uhbUiClient")
