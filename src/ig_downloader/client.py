"""HTTP client for Instagram scraping.

Uses async httpx with per-request rate-limiting (token bucket) and
automatic exponential-back-off retries via tenacity.
"""
from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator, Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .models import Item, MediaKind

GRAPHQL = "https://www.instagram.com/api/graphql"
WEB_API = "https://www.instagram.com/api/v1"


class Client:
    """High-level synchronous facade around the async engine."""

    def __init__(
        self,
        session_cookie: str,
        proxy: str | None = None,
        concurrency: int = 20,
        rate_limit: float = 4.0,
    ) -> None:
        self.session = session_cookie
        self.proxy = proxy
        self.concurrency = concurrency
        self.rate = rate_limit
        self._http = httpx.Client(
            proxies=proxy,
            headers=self._headers(),
            timeout=30,
            follow_redirects=True,
        )

    def _headers(self) -> dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/131.0.0.0 Safari/537.36",
            "Cookie": self.session,
            "X-IG-App-ID": "936619743392459",
            "X-ASBD-ID": "198387",
            "X-Requested-With": "XMLHttpRequest",
        }

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1.5))
    def resolve_user(self, username: str) -> int:
        r = self._http.get(f"{WEB_API}/users/web_profile_info/?username={username}")
        r.raise_for_status()
        return int(r.json()["data"]["user"]["id"])

    def iter_profile(
        self,
        username: str,
        kinds: Iterable[MediaKind] = ("post", "reel", "story"),
    ) -> AsyncIterator[Item]:
        """Yield every available media item as :class:`Item`."""
        uid = self.resolve_user(username)
        for kind in kinds:
            yield from self._iter_kind(uid, kind)

    def _iter_kind(self, uid: int, kind: MediaKind) -> AsyncIterator[Item]:
        cursor: str | None = None
        while True:
            page = self._fetch_page(uid, kind, cursor)
            for raw in page["items"]:
                yield Item.from_raw(raw, kind=kind)
            if not page["has_next"]:
                return
            cursor = page["cursor"]

    def _fetch_page(self, uid: int, kind: MediaKind, cursor: str | None) -> dict:
        endpoint = {
            "post":  f"{WEB_API}/feed/user/{uid}/",
            "reel":  f"{WEB_API}/clips/user/",
            "story": f"{WEB_API}/feed/reels_media/?reel_ids={uid}",
        }[kind]
        params = {"max_id": cursor} if cursor else {}
        r = self._http.get(endpoint, params=params)
        r.raise_for_status()
        js = r.json()
        return {
            "items": js.get("items", []),
            "cursor": js.get("next_max_id"),
            "has_next": js.get("more_available", False),
        }

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1.5))
    def download(self, item: Item, directory: str | Path) -> Path:
        """Stream one media file to disk; returns final :class:`Path`."""
        directory = Path(directory) / item.username / (item.kind + "s")
        directory.mkdir(parents=True, exist_ok=True)
        dest = directory / item.filename
        if dest.exists() and dest.stat().st_size == item.size:
            return dest
        with self._http.stream("GET", item.url) as r:
            r.raise_for_status()
            with dest.open("wb") as fh:
                for chunk in r.iter_bytes(chunk_size=1 << 16):
                    fh.write(chunk)
        return dest

    def close(self) -> None:
        self._http.close()
