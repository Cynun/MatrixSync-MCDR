import asyncio
import threading
import matrix_sync.logger.get_logger as get_logger
import matrix_sync.plg_globals as plg_globals

from mcdreforged.api.all import *
from ..client.reporter import send_to_matrix
from ..client.receiver import get_messages, stop_sync
from ..client import *
from ..utils import *
from .help import *


builder = SimpleCommandBuilder()

plg_globals.tLock = threading.Lock()

def start_sync():
    logger = get_logger()
    if not plg_globals.tLock.locked():
        run_sync_task()
    else:
        logger.warning(tr("on_sync_running"))

@new_thread('MatrixReceiver')
def run_sync_task():
    logger = get_logger()
    plg_globals.sync = True
    if plg_globals.token_vaild:
        with plg_globals.tLock:
            logger.info(tr("on_sync_start"))
            asyncio.run(add_sync_task())
    else:
        logger.error(tr("token_mismatch"))
        plg_globals.sync = False

async def add_sync_task():
    await get_messages()

@new_thread('MatrixReporter')
def matrix_reporter(message: str):
    asyncio.run(add_report_task(message))

async def add_report_task(message: str):
    report_task = asyncio.create_task(send_to_matrix(message))
    await report_task

def command_register(server: PluginServerInterface):
    server.register_help_message("!!msync", help_message)
    builder.arg("message", QuotableText)
    builder.arg("pack_name", Text)
    builder.register(server)

@builder.command("!!msync start")
def on_command_start():
    start_sync()

@builder.command("!!msync stop")
async def on_command_stop():
    await stop_sync()

@builder.command("!!msync status")
def show_status():
    logger = get_logger()
    logger.info(f"Receiver: {plg_globals.sync}")
    if plg_globals.sync:
        logger.info(tr("sync_status.running"))
    else:
        logger.info(tr("sync_status.not_running"))

@builder.command("!!msync send <message>")
def on_command_send(src: CommandSource, ctx: CommandContext):
    if plg_globals.token_vaild:
        matrix_reporter(ctx["message"])
        src.reply(tr("on_send_command.sending"))
    else:
        src.reply(tr("on_send_command.failed") + ": " + tr("token_mismatch"))

@builder.command("!!msync reload")
def on_command_reload():
    psi.reload_plugin(plgSelf.id)

@builder.command("!!msync reload <pack_name>")
def on_command_reload_subpack(src: CommandSource, ctx: CommandContext):
    plugin_list = psi.get_plugin_list()
    subpack_id = "msync_" + ctx["pack_name"]
    if subpack_id in plugin_list:
        psi.reload_plugin(subpack_id)
    else:
        src.reply("Reload subpack error: Invaild name!")

@builder.command("!!msync")
@builder.command("!!msync help")
def show_help(src: CommandSource):
    src.reply(help_page)