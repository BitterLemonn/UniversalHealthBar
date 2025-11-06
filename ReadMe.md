# 通用Boss血条 使用说明

## 简介

通用Boss血条（Universal Health Bar）是一个用于我的世界网易版的模组，允许开发者为自定义Boss创建独特的血条样式，替代游戏原生的Boss血条显示。

## 如何使用

### 第一步：获取注册对象

通过服务端系统获取注册对象：

```python
# 获取注册对象
uhbServer = serverApi.GetSystem("lemonUHB", "UHBServer")
registryObj = uhbServer.getRegistryObj()
```

### 第二步：配置血条参数

使用链式调用设置血条的各项参数：

```python
registryObj.setBossName("你的Boss名称")\
.setMaskPath("textures/ui/boss_bar_mask")\
.setFillPath("textures/ui/boss_bar_fill")\
.setMaskSize((182, 14))\
.registry()
```

### 参数说明

| 方法                       | 参数类型    | 必填 | 默认值             | 说明                          |
|--------------------------|---------|----|-----------------|-----------------------------|
| `setBossName(name)`      | `str`   | ✓  | 无               | 设置Boss的名称（与游戏中显示的名称一致）      |
| `setMaskPath(path)`      | `str`   | ✓  | 无               | 设置血条外层（边框）贴图路径              |
| `setFillPath(path)`      | `str`   | ✓  | 无               | 设置血条内层（填充）贴图路径              |
| `setMaskSize(size)`      | `tuple` | ✓  | 无               | 设置外层贴图尺寸，格式：`(宽, 高)`        |
| `setFillSize(size)`      | `tuple` | ✗  | 与 `maskSize` 相同 | 设置内层贴图尺寸，格式：`(宽, 高)`        |
| `setPanelOffset(offset)` | `tuple` | ✗  | `(0, 0)`        | 设置整个血条面板的偏移，格式：`(x, y)`     |
| `setMaskOffset(offset)`  | `tuple` | ✗  | `(0, 0)`        | 设置外层贴图的偏移，格式：`(x, y)`       |
| `setFillOffset(offset)`  | `tuple` | ✗  | `(0, 0)`        | 设置内层贴图的偏移，格式：`(x, y)`       |
| `setFillColor(color)`    | `tuple` | ✗  | `(1.0,1.0,1.0)` | 设置内层贴图颜色（色调），格式：`(r, g, b)` |
| `setFillOnTop()`         | 无       | ✗  | `False`         | 设置内层显示在外层之上（用于特殊血条样式）       |
| `setOverwrite()`         | 无       | ✗  | `False`         | 允许覆盖已存在的同名Boss血条配置          |

### 第三步：准备贴图资源

1. 在资源包的 `textures` 目录下创建你的血条贴图
2. 建议准备两张贴图：
    - **外层贴图**（mask）：血条的边框或底色
    - **内层贴图**（fill）：血条的填充部分，会随血量变化

### 完整示例

```python
# 示例：为Boss"末影龙"创建血条

import serverApi


# 在合适的时机（需在客户端加载mod完成后）注册血条
def registerCustomBossBar():
    uhbServer = serverApi.GetSystem("lemonUHB", "UHBServer")

    # 创建并配置注册对象
    uhbServer.getRegistryObj()\
    .setBossName("末影龙")\
    .setMaskPath("textures/ui/custom/dragon_bar_mask")\
    .setFillPath("textures/ui/custom/dragon_bar_fill")\
    .setMaskSize((182, 14))\
    .registry()
```

## 注意事项

1. **Boss名称必须精确匹配**：`setBossName()` 中设置的名称必须与游戏中Boss显示的名称完全一致
2. **贴图路径格式**：路径相对于资源包根目录，不需要添加文件扩展名
3. **尺寸和偏移**：所有尺寸和偏移值使用像素单位
4. **注册时机**：必须在客户端加载完成后注册，避免同步问题
5. **未注册的Boss**：未通过此模组注册的Boss会自动显示原生血条

## 常见问题

**Q: 血条没有显示怎么办？**  
A: 检查以下几点：

- Boss名称是否与游戏内显示完全一致
- 贴图路径是否正确
- 资源包是否正确安装并启用

**Q: 血条位置不对怎么调整？**  
A: 使用 `setPanelOffset()` 调整整体位置，使用 `setMaskOffset()` 和 `setFillOffset()` 微调细节

**Q: 可以为同一个Boss设置多个血条样式吗？**  
A: 同一个Boss名称只能有一个血条配置，使用 `setOverwrite()` 可以覆写已经注册的配置

**Q: 内层和外层有什么区别？**  
A: 外层通常是固定的边框或底色，内层是会随血量变化的填充部分

---

## 技术重点

### 核心创新：多模组协同的"礼让机制"

本模组最巧妙的设计在于：**每个模组只显示一次自己不管的Boss的原生血条，却每tick隐藏自己管理的Boss的原生血条**。这种"
礼让机制"完美解决了多模组血条冲突问题。

### 工作原理详解

#### 场景假设

假设有两个模组同时安装：

- **模组A**：注册了Boss"末影龙"的自定义血条
- **模组B**：注册了Boss"凋灵"的自定义血条

#### 执行流程（每tick）

当"末影龙"出现时：

```
模组A的处理逻辑：
1. 检查"末影龙"是否在自己的注册列表 → 是 ✓
2. 每tick执行：隐藏原生血条，显示自定义血条
3. UI数据设置：仅第一次设置

模组B的处理逻辑：
1. 检查"末影龙"是否在自己的注册列表 → 否 ✗
2. 仅执行一次：显示原生血条，隐藏自定义血条
3. 返回，不再处理
```

**结果**：模组B只执行了一次"显示原生"，而模组A每tick都在"隐藏原生"，所以模组A的自定义血条成功显示！

#### 核心代码逻辑

```python
# 每个模组都会执行这段代码
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
    # 情况1：不是我的Boss，我只显示一次原生血条就不管了
    if not self.bossStateCache[cacheKey]["dataModified"]:
        vanillaHealthBar.SetVisible(True)  # 显示原生（仅一次）
        uhbHealthBar.SetVisible(False)  # 隐藏自定义（仅一次）
        self.bossStateCache[cacheKey]["dataModified"] = True
    return  # 关键：直接返回，不再每tick处理

# 情况2：是我的Boss，我要持续控制
vanillaHealthBar.SetVisible(False)  # 每tick隐藏原生
uhbHealthBar.SetVisible(True)  # 每tick显示自定义

# UI数据只设置一次（性能优化）
if not self.bossStateCache[cacheKey]["dataModified"]:
    registryData = self.registryData.getRegistryData(bossName)
    if not registryData:
        return
    self._modifyUHBBar(registryData, gridItemPath)
    self.bossStateCache[cacheKey]["dataModified"] = True
```

### 为什么这样设计？

#### 传统方案的问题

如果未注册的Boss也每tick显示原生血条：

```python
# ❌ 错误做法
if not isRegistered:
    vanillaHealthBar.SetVisible(True)  # 每tick执行
    uhbHealthBar.SetVisible(False)
    return
```

**问题**：模组A和模组B会互相抢夺控制权，谁后执行谁就赢，导致血条闪烁或混乱。

#### 本模组的巧妙之处

```python
# ✅ 正确做法
if not isRegistered:
    if not self.bossStateCache[cacheKey]["dataModified"]:
        vanillaHealthBar.SetVisible(True)  # 仅执行一次
        uhbHealthBar.SetVisible(False)
        self.bossStateCache[cacheKey]["dataModified"] = True
    return  # 礼让：不是我的Boss，我就不再干预
```

**优势**：

- 模组A注册了"末影龙"，每tick隐藏原生 → **主动权**
- 模组B没注册"末影龙"，只显示一次原生就退出 → **礼让**
- 结果：模组A的持续隐藏 > 模组B的一次显示 → **和谐共存**
