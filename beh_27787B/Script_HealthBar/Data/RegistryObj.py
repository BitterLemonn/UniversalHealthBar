from ..QuModLibs.Server import serverApi


class RegistryObj(object):

    def __init__(self):
        self.bossName = None
        self.panelOffset = None
        self.maskPath = None
        self.fillPath = None
        self.maskSize = None
        self.fillSize = None
        self.maskOffset = None
        self.fillOffset = None
        self.fillColor = None
        self.fillOnTop = False
        self.overwrite = False

    def setBossName(self, name):  # type: ("RegistryObj", str) -> "RegistryObj"
        """
        设置血条对应的Boss名称
        """
        self.bossName = name
        return self

    def setPanelOffset(self, offset):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置血条面板偏移
        """
        self.panelOffset = offset
        return self

    def setMaskPath(self, path):  # type: ("RegistryObj", str) -> "RegistryObj"
        """
        设置外层路径
        """
        self.maskPath = path
        return self

    def setFillPath(self, path):  # type: ("RegistryObj", str) -> "RegistryObj"
        """
        设置内层路径
        """
        self.fillPath = path
        return self

    def setMaskSize(self, size):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置外层尺寸
        """
        self.maskSize = size
        return self

    def setFillSize(self, size):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置内层尺寸
        """
        self.fillSize = size
        return self

    def setMaskOffset(self, offset):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置外层偏移
        """
        self.maskOffset = offset
        return self

    def setFillOffset(self, offset):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置内层偏移
        """
        self.fillOffset = offset
        return self

    def setFillColor(self, color):  # type: ("RegistryObj", tuple) -> "RegistryObj"
        """
        设置内层颜色
        """
        self.fillColor = color
        return self

    def setFillOnTop(self):  # type: ("RegistryObj") -> "RegistryObj"
        """
        设置内层在外层之上
        """
        self.fillOnTop = True
        return self

    def setOverwrite(self):  # type: ("RegistryObj") -> "RegistryObj"
        """
        设置覆盖已存在的Boss血条数据
        """
        self.overwrite = True
        return self

    def registry(self):
        if not self.bossName:
            raise ValueError("未设置Boss名称")
        if not self.maskPath:
            self.maskPath = "textures/ui/empty_progress_bar"
        if not self.fillPath:
            self.fillPath = "textures/ui/filled_progress_bar"
        if not self.maskSize:
            self.maskSize = (182, 5)
        if not self.fillOffset:
            self.fillOffset = (0, 0)
        if not self.maskOffset:
            self.maskOffset = (0, 0)
        if not self.panelOffset:
            self.panelOffset = (0, 0)
        if not self.fillSize:
            self.fillSize = self.maskSize
        if not self.fillColor:
            self.fillColor = (1.0, 1.0, 1.0)

        serverApi.GetSystem("lemonUHB", "UHBServer").registry(self)
