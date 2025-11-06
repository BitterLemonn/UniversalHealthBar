from .RegistryObj import RegistryObj


class ClientRegistryData(object):
    INSTANCE = None

    def __init__(self):
        self.registryData = {}

    @classmethod
    def getInstance(cls):
        if not cls.INSTANCE:
            cls.INSTANCE = ClientRegistryData()
        return cls.INSTANCE

    def registry(self, data):  # type: ("ClientRegistryData", "RegistryObj") -> None
        bossName = data.bossName
        if data.overwrite:
            print("[WARN] Boss '{}' 覆盖注册".format(bossName))
        elif bossName in self.registryData.keys():
            print("[WARN] Boss '{}' 已存在, 跳过注册".format(bossName))
            return

        self.registryData[bossName] = data

    def getBossNames(self):  # type: ("ClientRegistryData") -> list
        return list(self.registryData.keys())

    def getRegistryData(self, bossName):  # type: ("ClientRegistryData", str) -> "RegistryObj" | None
        return self.registryData.get(bossName, None)
