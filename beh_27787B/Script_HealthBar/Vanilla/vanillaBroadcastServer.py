import pickle

from ..Data.RegistryObj import RegistryObj
from ..QuModLibs.Server import *

ServerCls = serverApi.GetServerSystemCls()


class VanillaBroadcastServer(ServerCls):
    def __init__(self, namespace, serverName):
        ServerCls.__init__(self, namespace, serverName)
        print("[DEBUG] VanillaBoss血条服务器已加载")
        ListenForEvent("ClientLoadAddonsFinishServerEvent", self, self.onClientLoadAddonsFinishServerEvent)

    @staticmethod
    def getRegistryObj():
        return RegistryObj()

    def registry(self, registryObj):  # type: ("vanillaBroadcastServer", "RegistryObj") -> None
        print("[DEBUG] 发送Boss血条数据: {}".format(registryObj.bossName))
        Call("*", "UHB/client/registry", pickle.dumps(registryObj))
