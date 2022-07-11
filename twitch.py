from typing import Callable

from twitchio.ext.commands import Command, Context

from logger import logger

import config

__all__ = ["TwitchCommand"]

class TwitchCommand(Command):
    def __init__(self, name: str, func: Callable, flag="", **attrs):
        super().__init__(name, func, **attrs)
        self.__doc__ = func.__doc__
        self.flag = flag
        self.required = func.__required__
        self.enabled = True

    async def invoke(self, context: Context, *, index=0):
        if not self.enabled:
            return
        if self.flag:
            is_editor = (context.author.name in config.editors)
            if self.flag and (
                (not context.author.is_broadcaster) and
                ("e" in self.flag and not is_editor) and
                ("m" in self.flag and not context.author.is_mod)
            ):
                return
        logger.debug(f"Invoking command {self.name} by {context.author.display_name}")
        await super().invoke(context, index=index)
