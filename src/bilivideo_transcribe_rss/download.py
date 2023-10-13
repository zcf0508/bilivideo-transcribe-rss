import os
import subprocess
from typing import Any

from .utils import read_file


def download(url: str, save_dir: str) -> int:
    file_path = read_file(save_dir)

    if (not file_path.startswith("Error")) and os.path.exists(file_path):
        return 0

    result = subprocess.run(["bilili", "-d", save_dir, url, "-y", "--playlist-type", "no", "--danmaku", "no"])
    return result.returncode
