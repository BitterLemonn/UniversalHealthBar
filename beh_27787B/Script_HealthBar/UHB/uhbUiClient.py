# -*- coding: utf-8 -*-
import re
from ..Data.ClientRegistryData import ClientRegistryData
from ..QuModLibs.Client import *

ProxyCls = clientApi.GetUIScreenProxyCls()
Binding = clientApi.GetViewBinderCls()
NativeScreenManager = clientApi.GetNativeScreenManagerCls()

compFactory = clientApi.GetEngineCompFactory()
proxyObj = None  # type: "UHBUiProxy" | None

getInitRegistry = False  # 是否已请求初始注册表


@CallBackKey("UHB/client/registry")
def onUHBRegistry(packedRegistryObj):
    import pickle

    global getInitRegistry
    getInitRegistry = True
    registryObj = pickle.loads(packedRegistryObj)
    ClientRegistryData.getInstance().registry(registryObj)
    print("[DEBUG] 已注册Boss血条数据: {}".format(registryObj.bossName))


@Listen("LoadClientAddonScriptsAfter")
def onLoadClientAddonScriptsAfter(_):
    global getInitRegistry
    if not getInitRegistry:
        Call("UHB/server/request_registry")


@Listen("UiInitFinished")
def onUiInitFinished(_):
    def getAndForceSet():
        topNode = clientApi.GetTopUINode()
        if proxyObj is None or topNode.GetScreenName() != "hud.hud_screen":
            compFactory.CreateGame(levelId).AddTimer(0.0, getAndForceSet)
            return
        else:
            proxyObj.forceGetBossBarGridSize()

    getAndForceSet()


class UHBUiProxy(ProxyCls):

    def __init__(self, screenName, screenNode):
        ProxyCls.__init__(self, screenName, screenNode)
        self.registryData = ClientRegistryData.getInstance()
        self.screen = screenNode
        self.bossBarGridPath = None

        self._forceBossBarGridPath = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/boss_health_panel/boss_hud_panel/boss_health_grid"
        self.nowShowingBossNames = {}
        # 按索引缓存状态,当名称改变时自动重置
        self.bossStateCache = {}  # 格式: {"index_X": {"bossName": str, "isRegistered": bool, "dataModified": bool}}

    def OnCreate(self):
        # print("[DEBUG] 通用Boss血条UI代理已创建")
        global proxyObj
        proxyObj = self
        ListenForEvent("GridComponentSizeChangedClientEvent", self, self.onGridComponentSizeChanged)

    def OnDestroy(self):
        # print("[DEBUG] 通用Boss血条UI代理已销毁")
        global proxyObj
        proxyObj = None
        UnListenForEvent("GridComponentSizeChangedClientEvent", self, self.onGridComponentSizeChanged)

    def OnTick(self):
        if not self.bossBarGridPath:
            return
        bossBarGrid = self.screen.GetBaseUIControl(self.bossBarGridPath).asGrid()
        gridItemList = self.screen.GetChildrenName(bossBarGrid.GetPath())
        for gridItem in gridItemList:
            bossNameLabel = self.screen.GetBaseUIControl(
                self.bossBarGridPath + "/" + gridItem + "/boss_name/boss_name"
            ).asLabel()
            index = int(re.findall(r'\d+', gridItem)[0]) - 1
            self.nowShowingBossNames[index] = bossNameLabel.GetText()
            self.handleHealthBar(index, self.bossBarGridPath + "/" + gridItem)

    def forceGetBossBarGridSize(self):
        def checkAndForceSet():
            if self.bossBarGridPath:
                return
            # print("[DEBUG] 强制获取Boss血条网格大小")
            self.bossBarGridPath = self._forceBossBarGridPath

        compFactory.CreateGame(levelId).AddTimer(1.0, checkAndForceSet)

    def onGridComponentSizeChanged(self, data):
        path = data.get("path", "")
        controlName = path.split("/")[-1]
        if controlName != "boss_health_grid":
            return
        # print("[DEBUG] 检测到网格大小变化事件")
        self.bossBarGridPath = "/".join(path.split("/")[2:])

    def handleHealthBar(self, index, gridItemPath):
        bossName = self.nowShowingBossNames.get(index, "")
        if not bossName:
            return

        vanillaHealthBar = self.screen.GetBaseUIControl(gridItemPath + "/progress_bar_for_collections")
        uhbHealthBar = self.screen.GetBaseUIControl(gridItemPath + "/uhb_bar")

        # 检查boss是否在注册列表中
        isRegistered = bossName in self.registryData.getBossNames()

        # 检查该索引位置的boss名称是否发生变化
        cacheKey = "index_{}".format(index)
        if cacheKey not in self.bossStateCache or self.bossStateCache[cacheKey]["bossName"] != bossName:
            # 名称变化或首次出现，重置缓存
            self.bossStateCache[cacheKey] = {
                "bossName": bossName,
                "isRegistered": isRegistered,
                "dataModified": False
            }

        if not isRegistered:
            # boss未注册，显示原生血条（仅执行一次）
            if not self.bossStateCache[cacheKey]["dataModified"]:
                vanillaHealthBar.SetVisible(True)
                uhbHealthBar.SetVisible(False)

                self.bossStateCache[cacheKey]["dataModified"] = True
                # print("[DEBUG] 显示原生血条: {}".format(bossName))
            return

        # boss已注册，每tick隐藏原生血条
        vanillaHealthBar.SetVisible(False)
        # 每tick显示UHB血条
        uhbHealthBar.SetVisible(True)

        # 仅第一次对UHB血条进行数据设置
        if not self.bossStateCache[cacheKey]["dataModified"]:
            registryData = self.registryData.getRegistryData(bossName)
            if not registryData:
                return
            self._modifyUHBBar(registryData, gridItemPath)
            self.bossStateCache[cacheKey]["dataModified"] = True

    def _modifyUHBBar(self, registryData, gridItemPath):
        """仅执行一次的UHB血条数据设置"""
        # print("[DEBUG] 设置UHB血条数据: {}".format(registryData.bossName))

        uhbBarPath = gridItemPath + "/uhb_bar"
        uhbBar = self.screen.GetBaseUIControl(uhbBarPath)
        uhbMaskBar = self.screen.GetBaseUIControl(uhbBarPath + "/mask_bar").asImage()
        uhbFillBar = self.screen.GetBaseUIControl(uhbBarPath + "/fill_bar").asImage()

        uhbOffset = (registryData.panelOffset[0], registryData.panelOffset[1] + 10)
        uhbBar.SetPosition(uhbOffset)
        uhbMaskBar.SetSprite(registryData.maskPath)
        uhbFillBar.SetSprite(registryData.fillPath)
        uhbMaskBar.SetSize(registryData.maskSize, True)
        uhbFillBar.SetSize(registryData.fillSize, True)
        uhbMaskBar.SetPosition(registryData.maskOffset)
        uhbFillBar.SetPosition(registryData.fillOffset)
        uhbFillBar.SetSpriteColor(registryData.fillColor)
        if registryData.fillOnTop:
            uhbFillBar.SetLayer(2, False, False)
            uhbMaskBar.SetLayer(1, True, True)
        return self.screen.UpdateScreen()


NativeScreenManager.instance().RegisterScreenProxy("hud.hud_screen", "Script_HealthBar.UHB.uhbUiClient.UHBUiProxy")
