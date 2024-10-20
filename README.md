- 中文
- [English](https://github.com/Mooling0602/MatrixSync-MCDR/blob/2.3.0/README_en_us.md)

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的pypi项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

当前分支版本：主分支@2.3.2

## 用法
从release下载最新版本，在MCDReforged的启动环境中安装好需要的Python依赖，然后扔到plugins文件夹里面即可。

### 使用 Git
> This part doesn't support English yet, please use translate tools at present.
> 
> 依赖软件包`zip`
> 
> 在终端上运行`git clone https://github.com/Mooling0602/MatrixSync-MCDR.git`，然后进入`MatrixSync-MCDR`目录下并运行`pack_plugin.sh`（记得给文件设置可执行权限）
>
> 若无法正常访问GitHub，可以运行`git clone https://mirror.ghproxy.com/https://github.com/Mooling0602/MatrixSync-MCDR.git`
>
> 懒人用命令：`git clone https://mirror.ghproxy.com/https://github.com/Mooling0602/MatrixSync-MCDR.git && cd MatrixSync-MCDR && chmod +x pack_plugin.sh && ./pack_plugin.sh`
>
> 正常情况下，请不要修改脚本内容及所用配置（config.ini）

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步，并认真阅读下面的内容以进行插件配置。

配置完毕并启用插件后，若有测试消息成功发送到matrix群组，则表示消息同步开始工作。

若消息同步的过程中有任意方向的消息转发出现问题，也请按下面的内容检查配置是否正确。

### 配置文件
#### config.json

| 配置项 | 配置内容 |
| - | - |
| **homeserver** | 机器人账号登录所使用的根服务器 |
| **user_id** | 机器人的账号ID，格式为@<用户名>:<根服务器>，如@mcchatbot:example.com |
| **password** | 机器人账号的密码，一般仅在初次登录使用 |
| **room_id** | 需要接收游戏消息的房间的ID，目前只能设置一个 |
| **room_name** | 需要转发消息到游戏内的房间的显示名称（必须准确无误，若发生更新也需要同步修改，否则你将看不到任何消息），目前只能设置一个 |
| **device_id** | 登录用的设备名，一般无需修改，可自定义 |

#### settings.json

| 配置项 | 配置内容 |
| - | - |
| plugin-enabled | 插件是否启用，请确保配置文件和所需设置修改无误后再开启 |
| allow_all_rooms_msg | 是否允许来自所有房间的消息，若开启，则来自机器人账号所加入的房间的消息都会被转发到游戏中，并注明房间的显示名称，否则只转发已设置的房间的消息 |
| sync_old_msg | 是否同步旧的消息，默认开启，可在插件配置目录下的token.json文件中增加有效的`next_batch`项后关闭 |

## 接口（API）
插件提供了一个协程函数`sendMsg()`供其他开发者调用以实现向Matrix群组发送自定义内容，其回调参数为`message`，下面是代码参考：
```python
import asyncio
import ...

from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg
from ... import ...

def main():
    pass
    asyncio.run(sendMsg(message))
```
如果要在协程内调用该接口：
```python
import asyncio
import ...

from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg
from ... import ...

async def main():
    pass
    await sendMsg(message)
```
将主插件（MatrixSync）添加到MCDR依赖中，并将其Python依赖一并添加到自己的插件中，然后在开发过程中把`message`替换成你想要发送的自定义内容即可。

请注意，该接口的支持是实验性的，若要调用此接口，请确保用户安装并配置好了主插件（MatrixSync）。

2.2.0版本以后，机器人的初始化将直接在加载插件时进行，所以如果需要判断主插件的消息上报器是否能够正常工作，可以在调用函数前导入相关的全局变量并加入判断条件，下面是示例代码：
```python
import asyncio
import matrix_sync.client
import ...

from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg

def main():
    pass
    clientStatus = matrix_sync.client.clientStatus
    if clientStatus:
        asyncio.run(sendMsg(message))
    else:
        # 可以在此自定义报错的内容，也可以直接删除此部分忽略该接口
        server.logger.info("error")
```
协程函数示例：
```python
import asyncio
import matrix_sync.client
import ...

from mcdreforged.api.all import *
from matrix_sync.reporter import sendMsg

async def main():
    pass
    clientStatus = matrix_sync.client.clientStatus
    if clientStatus:
        await sendMsg(message)
    else:
        # 可以在此自定义报错的内容，也可以直接删除此部分忽略该接口
        server.logger.info("error")
```

由于2.3.0版本新增了Matrix房间消息的分发事件，且2.3.1版本重构了这部分接口，所以该部分内容已过时。

这些过时的内容仍然持续有效，但其做法不再推荐，请等待后续更详细的文档更新。

重构后接口的简单用法：
```python
import matrix_sync.client

def main():
    clientStatus = matrix_sync.client.clientStatus
    if clientStatus:
        sender(message)

# 消息将在独立线程中被发送到Matrix，不再可能会阻塞MCDR主线程
```

## 热重载（reload）及消息互通控制
插件默认在游戏服务端启动完成时才会自动启动房间消息接收进程，重新加载插件后，消息接收器并不会自动启动。

要手动启动房间消息接收进程，请执行MCDR命令`!!msync start`，游戏内和控制台上都可以使用。

要关闭房间消息接收进程，可以在控制台使用`!!msync stop`，直到下次服务器启动完成前消息接收器都必须手动重启。

要在详细阅读后关闭2.3.1版本新增的大量提示，可以使用`!!msync closetip`，目前想重新查看提示，只能在源码中查看语言文件，或自行修改token.json

插件会自动在解析到游戏内的消息时尝试转发到配置好的Matrix房间内，暂时无法禁用。

该指令没有权限要求，但设置了进程锁（安全机制），重复执行会警告提示，不会影响插件功能的正常运行。

请注意，该功能是实验性的，若发现任何错误请及时通过GitHub Issue向插件作者反馈！

## 注意
- 首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，并在settings.json中启用plugin_enabled配置项以启用插件，然后重启服务器或着重载插件以正常使用。

- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件，欢迎PR。

- 多语言目前只支持中文（简体）和英语（用谷歌和ChatGPT从中文翻译），任何人都可以联系我帮助完善翻译，欢迎PR到/lang语言文件中。
