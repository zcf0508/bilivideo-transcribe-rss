import whisper

from .download import download
from .utils import read_file


def main():
    (id, download_path), process = download("https://www.bilibili.com/video/BV1zB4y1Z7XJ")
    if process.returncode == 0:
        print("下载成功" + id)
    video_file = read_file(download_path)
    video_file_name = video_file.split("/")[-1].split(".")[0]

    model = whisper.load_model("large")

    result = model.transcribe(
        video_file,
        language="zh",
        temperature=0.2,
        initial_prompt=f"视频标题是《{video_file_name}》,使用简体中文，增加标点。",
    )
    print(result["text"])
