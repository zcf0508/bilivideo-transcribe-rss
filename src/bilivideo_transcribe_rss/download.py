import subprocess

BASE_SAVE_PATH = r"E:\Downloads"


def download(url: str) -> ((str, str), subprocess.CompletedProcess):
    id = url.split("/")[-1].split("?")[0]
    download_path = f"{BASE_SAVE_PATH}/bilili/{id}"
    return (id, download_path), subprocess.run(
        ["bilili", "-d", download_path, url, "-y", "--playlist-type", "no", "--danmaku", "no"]
    )
