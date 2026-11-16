"""ig_downloader — bulk Instagram media downloader.

Public API:
    Client(session_cookie, proxy=None) — main entry point
    Item                                 — dataclass with media metadata
"""
from .client import Client
from .models import Item

__version__ = "2026.1.0"
__all__ = ["Client", "Item", "__version__"]
