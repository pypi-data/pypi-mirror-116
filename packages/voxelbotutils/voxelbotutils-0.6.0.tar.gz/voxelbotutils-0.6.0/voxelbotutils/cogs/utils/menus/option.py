import typing
import inspect

from discord.ext import commands

from .errors import ConverterFailure
from .converter import Converter
from .mixins import MenuDisplayable
from .utils import async_wrap_callback


class Option(MenuDisplayable):
    """
    An object for use in menus so as to represent one of the clickable options in the settings menus.
    """

    def __init__(
            self, display: typing.Union[str, typing.Callable[[commands.Context], str]],
            component_display: str = None, converters: typing.Optional[typing.List[Converter]] = None,
            callback: typing.Callable[[commands.Context, typing.List[typing.Any]], None] = None,
            cache_callback: typing.Optional[typing.Callable[[commands.Context, typing.List[typing.Any]], None]] = None,
            allow_none: bool = False):
        """
        Attributes:
            display (typing.Union[str, typing.Callable[[commands.Context], str]]): The item
                that string be shown on the menu itself. If a string is passed, then it will
                be given :code:`.format(ctx)`. If a method is passed, then it will be given a
                :class:`discord.ext.commands.Context` object as an argument.
            component_display (str): The string that gets shown in the button for this option.
            converters (typing.Optional[typing.List[Converter]]): A list of converters that the
                user should be asked for.
            callback (typing.Callable[[commands.Context, typing.List[typing.Any]], None]): An [async]
                function that will be given the context object and a list of the converted user-provided
                arguments.
            cache_callback (typing.Optional[typing.Callable[[commands.Context, typing.List[typing.Any]], None]]):
                An [async] function that will be given the context object and a list of the
                converted user-provided arguments. This is provided as well as the :code:`callback` parameter
                so as to allow for the seperation of different reusable methods.
            allow_none (bool): Whether or not the option should allow :code:`None` as a valid input.
        """

        self.display = display
        self.component_display = component_display or display
        self._button_style = None
        self.converters = converters or list()
        self._callback = callback
        self.callback = async_wrap_callback(callback)
        self._cache_callback = cache_callback
        self.cache_callback = async_wrap_callback(cache_callback)
        self.allow_none = allow_none

    async def run(self, ctx: commands.Context):
        """
        Runs the converters and callback for this given option.
        """

        data = []
        messages_to_delete = []
        has_failed = False
        for i in self.converters:
            try:
                data.append(await i.run(ctx, messages_to_delete))
                if data[-1] is None and not self.allow_none:
                    has_failed = True
                    break
            except ConverterFailure:
                has_failed = True
                break
        if not has_failed:
            await self.callback(ctx, data)
            await self.cache_callback(ctx, data)
        ctx.bot.loop.create_task(ctx.channel.delete_messages(messages_to_delete))
