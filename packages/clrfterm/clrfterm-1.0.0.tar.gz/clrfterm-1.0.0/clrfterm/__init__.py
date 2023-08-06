__version__ = "1.0.0"

from sys import stdout
from typing import Union

from .ansi import (
    Styles,
    Foreground,
    Backgrounds,
)
from .win import enable_ansi
from .message_builder import MessageBuilder


def rprint(
        text: str,
        *,
        foreground: Union[Foreground, str] = "",
        style: Union[Styles, str] = "",
        background: Union[Backgrounds, str] = ""
) -> None:
    """
    stdout.write auto-reset wrapper
    """
    stdout.write(foreground + style + background + text + Styles.RESET + "\n")


def reset() -> None:
    """
    function reset
    """
    stdout.write(Styles.RESET.value)
