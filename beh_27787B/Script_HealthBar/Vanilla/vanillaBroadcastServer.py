import pickle

from ..Data.RegistryObj import RegistryObj
from ..QuModLibs.Server import *

ServerCls = serverApi.GetServerSystemCls()


@CallBackKey("UHB/server/request_registry")
@InjectRPCPlayerId
def onUHBRequestRegistry(playerId):
    serverApi.GetSystem("lemonUHB", "UHBServer").sendRegistryToClient(playerId)


class VanillaBroadcastServer(ServerCls):
    def __init__(self, namespace, serverName):
        ServerCls.__init__(self, namespace, serverName)
        print("[DEBUG] VanillaBoss血条服务器已加载")
        ListenForEvent("ClientLoadAddonsFinishServerEvent", self, self.onClientLoadAddonsFinishServerEvent)
        self._registryData = {}  # type: dict[str, RegistryObj]

    @staticmethod
    def getRegistryObj():
        return RegistryObj()

    def registry(self, registryObj):  # type: ("vanillaBroadcastServer", "RegistryObj") -> None
        if registryObj.overwrite:
            self._registryData[registryObj.bossName] = registryObj
        elif registryObj.bossName not in self._registryData:
            self._registryData[registryObj.bossName] = registryObj

        print("[DEBUG] 发送Boss血条数据: {}".format(registryObj.bossName))
        Call("*", "UHB/client/registry", pickle.dumps(registryObj))

    def sendRegistryToClient(self, playerId):  # type: ("vanillaBroadcastServer", "int") -> None
        for registryObj in self._registryData.values():
            print("[DEBUG] 发送Boss血条数据: {} 给玩家ID: {}".format(registryObj.bossName, playerId))
            Call(playerId, "UHB/client/registry", pickle.dumps(registryObj))
