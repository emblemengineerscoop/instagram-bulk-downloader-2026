"""Basic usage: download every Reel and Story of a profile."""
import os
from ig_downloader import Client

cli = Client(
    session_cookie=os.environ["IG_SESSION"],
    proxy=os.environ.get("IG_PROXY"),
    concurrency=20,
)

for item in cli.iter_profile("natgeo", kinds=("reel", "story")):
    cli.download(item, directory="./downloads")
    print(f"ok {item.shortcode} ({item.kind})")

cli.close()
