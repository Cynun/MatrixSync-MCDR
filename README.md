- 中文
- [English](https://github.com/Mooling0602/MatrixSync-MCDR/blob/main/README_en_us.md)
> 为避免合并入主分支后链接指向错误，URL一律使用主分支的地址。如果你正在访问其他分支，请注意自行定位链接跳转位置。

# MatrixSync-MCDR
一个MCDR（全称[MCDReforged](https://mcdreforged.com/)）插件，用于同步Matrix群组和《我的世界》服务器的线上游戏之间的消息。

关于[Matrix](https://matrix.org/): 一个开放的去中心化通讯协议，用于聊天软件。

开发过程中用到的pypi项目：[matrix-nio](https://pypi.org/project/matrix-nio/)。

## 用法
从release下载最新版本，在MCDReforged的启动环境中安装好需要的Python依赖，然后扔到plugins文件夹里面即可。

在使用此插件之前，你必须知道什么是[Matrix](https://matrix.org/)，然后准备一个账号作为matrix机器人用于消息同步，并认真阅读下面的内容以进行插件配置。

配置完毕并启用插件后，若有测试消息成功发送到matrix群组，则表示消息同步开始工作。

若消息同步的过程中有任意方向的消息转发出现问题，也请按配置文件部分的内容检查配置是否正确。

### 配置文件
#### config.json

| 配置项 | 配置内容 |
| - | - |
| **homeserver** | 机器人账号所属的根服务器 |
| **user_id** | 机器人的账号ID，格式为@<用户名>:<根服务器>，如@mcchatbot:example.com |
| **password** | 机器人账号的密码，在初次登录和重新生成token时使用 |
| **room_id** | 需要同步游戏消息的房间的ID，使用管理员权限在房间设置中查看 |
| **device_id** | 登录用的设备名，一般无需修改，可自定义 |

> 只支持单账号和单聊天房间（相当于QQ群），计划在v3版本以后开发多配置管理。
> 
> v2 LTS 即将推出，如果你不需要多账号、多房间管理，可以持续使用v2版本。
> 
> v2 LTS 推送将于v2.5.x进行，届时会对当前的配置文件格式进行修改，可能和之前完全不兼容，请注意。

#### settings.json

| 配置项 | 配置内容 |
| - | - |
| plugin-enabled | 插件是否启用，请确保配置文件和所需设置修改无误后再开启 |
| allow_all_rooms_msg | 是否允许来自所有房间的消息，若开启，则来自机器人账号所加入的房间的消息都会被转发到游戏中，并注明房间的显示名称，否则只转发已设置的房间的消息 |
| sync_old_msg | 是否同步旧的消息，默认关闭，开启以在插件启动同步时加载历史消息 |

## 接口（API）
2.3.0以前的旧接口仍然有效，请到[docs](https://github.com/Mooling0602/MatrixSync-MCDR/blob/dev/docs.md)查看。

> 2.3.x修改的接口将不再受到任何支持，原因为相关函数名和分发的插件事件中提供的参数发生冲突。

2.4.0版本重构后的新接口的简单用法：
```python
import matrix_sync.client
from matrix_sync.reporter import send_matrix

def main():
    message = "你要发送的消息"
    send_matrix(message)

# 消息将在独立线程MatrixReporter中被发送到Matrix，不再可能会阻塞MCDR主线程
# 如果消息没有发送到Matrix，启用MCDR配置中的`debug.plugin`，会显示详情
```

## 热重载（reload）及消息互通控制
始终建议在运行环境稳定时，尽量不使用热重载。

现在Matrix消息的收发已经实现同步，使用`!!msync`查看帮助。

服务器启动完成后，插件会自动启动Minecraft游戏服务器和Matrix之间的消息互通，暂时不能对消息的收发方向进行配置。（将于2.5.x继续改善）

## 注意
### 关于首次使用
首次加载插件的时候，插件将自动初始化配置并卸载自己。你需要正确修改默认的配置文件，并在settings.json中启用plugin_enabled配置项以启用插件，然后重载插件以正常使用。

- 不打算支持加密信息（EE2E），有需要可以二次开发修改插件，欢迎PR。

- 多语言目前只支持中文（简体）和英语（用谷歌和ChatGPT从中文翻译），任何人都可以联系我帮助完善翻译，欢迎PR到/lang语言文件和README中。
