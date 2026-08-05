"""Florent Code League submission entry point.

The platform checks the submission entry point for a class declaration named
``Player`` (rather than only accepting an imported alias), so keep this thin
wrapper here and the implementation in :mod:`bot.player`.
"""

from bot.player import Player as _Player


class Player(_Player):
    """Platform-visible entry point for the candidate bot."""

    pass

__all__ = ["Player"]
