"""Dataclasses for media items."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

MediaKind = Literal["post", "reel", "story", "highlight", "igtv"]


@dataclass(slots=True)
class Item:
    id: str
    shortcode: str
    kind: MediaKind
    url: str
    size: int
    username: str
    taken_at: datetime
    caption: str = ""
    likes: int = 0
    is_video: bool = False
    extra: dict = field(default_factory=dict)

    @property
    def filename(self) -> str:
        ext = ".mp4" if self.is_video else ".jpg"
        return f"{self.taken_at:%Y-%m-%d}_{self.shortcode}{ext}"

    @classmethod
    def from_raw(cls, raw: dict, kind: MediaKind) -> "Item":
        return cls(
            id=str(raw["id"]),
            shortcode=raw.get("code", raw["id"]),
            kind=kind,
            url=raw["video_versions"][0]["url"] if raw.get("video_versions")
                else raw["image_versions2"]["candidates"][0]["url"],
            size=int(raw.get("original_width", 0) * raw.get("original_height", 0)),
            username=raw["user"]["username"],
            taken_at=datetime.fromtimestamp(raw["taken_at"]),
            caption=(raw.get("caption") or {}).get("text", ""),
            likes=int(raw.get("like_count", 0)),
            is_video=bool(raw.get("video_versions")),
        )
