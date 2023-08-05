# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import inspect
import os
import re
import sys
from pathlib import Path
from time import gmtime, sleep, strftime
from traceback import format_exc

from plugins import ultroid_version as ult_ver
from telethon import __version__ as telever
from telethon import events
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendInlineForbiddenError,
    FloodWaitError,
    MessageDeleteForbiddenError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    UserIsBotError,
)
from telethon.utils import get_display_name

from .. import HNDLR, LOGS, SUDO_HNDLR, asst, udB, ultroid_bot
from ..dB import DEVLIST
from ..dB.core import LIST, LOADED
from ..functions.all import bash
from ..functions.all import time_formatter as tf
from ..functions.sudos import is_fullsudo
from ..version import __version__ as pyver
from . import owner_and_sudos, should_allow_sudo, ultroid_bot
from ._assistant import admin_check
from ._wrappers import eod

hndlr = "\\" + HNDLR

black_list_chats = eval(udB.get("BLACKLIST_CHATS"))


def compile_pattern(data, hndlr):
    if data.startswith(r"\#"):
        pattern = re.compile(data)
    else:
        pattern = re.compile(hndlr + data)
    return pattern


# decorator

# ultroid_cmd (base decorator) was taken from RaphielGang/Telegram-Paperlane
# It was Later Modified by TeamUltroid, to use in our way.
# https://github.com/RaphielGang/Telegram-Paperplane/blob/625875a9ecdfd267a53067b3c1580000f5006973/userbot/events.py#L22


def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args["pattern"]
    black_chats = args.get("chats", None)
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    fullsudo = args.get("fullsudo", False)
    allow_all = args.get("allow_all", False)
    type = args.get("type", ["official"])
    manager = udB.get("MANAGER")
    if udB.get("DUAL_MODE"):
        type.append("dualmode")
    args["forwards"] = False
    if pattern is not None:
        args["pattern"] = compile_pattern(pattern, hndlr)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    args["blacklist_chats"] = True
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats
    if black_chats is not None:
        if len(black_chats) == 0:
            args["chats"] = []
        else:
            args["chats"] = black_chats

    if "admins_only" in args:
        del args["admins_only"]
    if "groups_only" in args:
        del args["groups_only"]
    if "type" in args:
        del args["type"]
    if "allow_all" in args:
        del args["allow_all"]
    if "fullsudo" in args:
        del args["fullsudo"]

    def decorator(func):
        pass

        def doit(mode):
            async def wrapper(ult):
                chat = ult.chat
                if mode in ["dualmode", "official", "sudo"]:
                    if not ult.out and not allow_all and mode in ["dualmode", "sudo"]:
                        if str(ult.sender_id) not in owner_and_sudos():
                            return
                        if fullsudo and not is_fullsudo(ult.sender_id):
                            return await eod(
                                ult, "`Full Sudo User Required...`", time=15
                            )
                    if hasattr(chat, "title"):
                        if (
                            "#noub" in chat.title.lower()
                            and not (chat.admin_rights or chat.creator)
                            and not (str(ult.sender_id) in DEVLIST)
                        ):
                            return
                    if admins_only:
                        if ult.is_private:
                            return await eod(ult, "`Use this in group/channel.`")
                        if not (chat.admin_rights or chat.creator):
                            return await eod(ult, "`I am not an admin.`")
                elif mode == "manager":
                    if not (ult.out or await admin_check(ult)):
                        return
                if groups_only and ult.is_private:
                    return await eod(ult, "`Use this in group/channel.`")
                try:
                    await func(ult)
                except FloodWaitError as fwerr:
                    await asst.send_message(
                        int(udB.get("LOG_CHANNEL")),
                        f"`FloodWaitError:\n{str(fwerr)}\n\nSleeping for {tf((fwerr.seconds + 10)*1000)}`",
                    )
                    sleep(fwerr.seconds + 10)
                    await asst.send_message(
                        int(udB.get("LOG_CHANNEL")),
                        "`Bot is working again`",
                    )
                except ChatSendInlineForbiddenError:
                    return await eod(ult, "`Inline Locked In This Chat.`")
                except (BotMethodInvalidError, UserIsBotError) as boterror:
                    return await eod(ult, str(boterror))
                except (
                    MessageIdInvalidError,
                    MessageNotModifiedError,
                    MessageDeleteForbiddenError,
                ):
                    pass
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except BaseException as e:
                    LOGS.exception(e)
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    naam = get_display_name(chat)
                    ftext = "**Ultroid Client Error:** `Forward this to` @UltroidSupport\n\n"
                    ftext += "`Py-Ultroid Version: " + str(pyver)
                    ftext += "\nUltroid Version: " + str(ult_ver)
                    ftext += "\nTelethon Version: " + str(telever) + "\n\n"
                    ftext += "--------START ULTROID CRASH LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup: " + str(ult.chat_id) + " " + str(naam)
                    ftext += "\nSender ID: " + str(ult.sender_id)
                    ftext += "\nReplied: " + str(ult.is_reply)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(ult.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END ULTROID CRASH LOG--------"
                    ftext += "\n\n\nLast 5 commits:\n"

                    stdout, stderr = await bash('git log --pretty=format:"%an: %s" -5')
                    result = str(stdout.strip()) + str(stderr.strip())

                    ftext += result + "`"

                    if len(ftext) > 4096:
                        with open("logs.txt", "w") as log:
                            log.write(ftext)
                        await asst.send_file(
                            int(udB["LOG_CHANNEL"]),
                            "logs.txt",
                            caption="**Ultroid Client Error:** `Forward this to` @UltroidSupport\n\n",
                        )
                        os.remove("logs.txt")
                    else:
                        await asst.send_message(
                            int(udB["LOG_CHANNEL"]),
                            ftext,
                        )

            return wrapper

        if "official" in type:
            args["outgoing"] = True
            ultroid_bot.add_event_handler(doit("official"), events.NewMessage(**args))
            del args["outgoing"]

            if allow_sudo:
                args["outgoing"] = False
                args["pattern"] = compile_pattern(pattern, "\\" + SUDO_HNDLR)
                ultroid_bot.add_event_handler(doit("sudo"), events.NewMessage(**args))
                del args["outgoing"]
            wrapper = doit("official")
            try:
                LOADED[file_test].append(wrapper)
            except Exception:
                LOADED.update({file_test: [wrapper]})

        if "assistant" in type:
            args["pattern"] = compile_pattern(pattern, "/")
            asst.add_event_handler(doit("assistant"), events.NewMessage(**args))
        if manager and "manager" in type:
            args["pattern"] = compile_pattern(pattern, "/")
            asst.add_event_handler(doit("manager"), events.NewMessage(**args))
        DH = udB.get("DUAL_HNDLR")
        if "dualmode" in type:
            if not (manager and DH == "/"):
                args["pattern"] = compile_pattern(pattern, "\\" + DH)
                asst.add_event_handler(doit("dualmode"), events.NewMessage(**args))

    return decorator
