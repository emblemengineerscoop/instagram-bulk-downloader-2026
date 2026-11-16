# Instagram Bulk Downloader 2026

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Downloads](https://img.shields.io/badge/downloads-50k%2B-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Build](https://img.shields.io/badge/build-passing-success)

> High-speed media extraction utility that batch-downloads photos, videos, Reels,
> Stories and Highlights from public Instagram profiles in their **original quality**.

---

## ✨ Features

- 📥 **Bulk download** entire profiles in one command
- 🎞️ Full support for Posts / Reels / Stories / Highlights / IGTV
- 🖼️ Original quality (no re-encoding, no watermark injection)
- 🚀 Async engine — 20+ concurrent fetches
- 🗂️ Smart naming (date + shortcode) and resumable downloads
- 🕵️ Rotating session cookies & proxies
- 📊 Progress bar + per-item retries
- 💾 JSON metadata export (likes, captions, mentions, timestamps)
- 🌐 Works behind SOCKS5 / HTTP proxy
- 🐍 Python 3.10 – 3.13

## 📦 Installation

```bash
pip install -r requirements.txt
```

Or clone and install from source:

```bash
git clone https://github.com/emblemengineerscoop/instagram-bulk-downloader-2026.git
cd instagram-bulk-downloader-2026
pip install -e .
```

## 🚀 Quick start

```bash
python -m ig_downloader --user nasa --out ./downloads
```

Download only Reels for the last 30 days:

```bash
python -m ig_downloader --user natgeo --kind reels --since 30d
```

Export all media + metadata as JSON:

```bash
python -m ig_downloader --user cristiano --metadata out.json
```

## 🧩 Usage (Python API)

```python
from ig_downloader import Client

cli = Client(session_cookie="sessionid=...")
for item in cli.iter_profile("nasa", kinds=("post", "reel", "story")):
    cli.download(item, directory="./downloads")
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```
IG_SESSION=sessionid=xxxxx
IG_PROXY=http://user:pass@host:port
IG_CONCURRENCY=20
IG_RATE_LIMIT=4.0
```

## 📁 Output structure

```
downloads/
└── nasa/
    ├── posts/
    │   ├── 2026-11-15_C1X2Y3.jpg
    │   └── 2026-11-14_C9Z8A2.mp4
    ├── reels/
    ├── stories/
    └── metadata.json
```

## 🤝 Contributing

PRs welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📄 License

MIT © 2026 – see [LICENSE](./LICENSE).
