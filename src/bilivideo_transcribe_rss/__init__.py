import json
import os
import threading

from flask import Flask, jsonify

from .constant import BASE_SAVE_PATH
from .download import download
from .feed import parse
from .utils import read_file
from .whisper import transcribe

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify(main())


lock = threading.Lock()


def download_and_transcribe(urls: list[str], save_dir: str):
    # 避免多次请求的时候，会重复创建 whisper model ，占用计算资源
    with lock:
        for url in urls:
            id = url.split("/")[-1].split("?")[0]

            status_file = os.path.join(save_dir, "status.json")
            download_dir = os.path.join(save_dir, id)

            with open(status_file, "r", encoding="utf-8") as f:
                status = json.load(f)
                for item in status:
                    if item["url"] == url:
                        if item["status"] == "finished":
                            break

            returncode = download(url, download_dir)

            if returncode == 0:
                # 视频文件地址
                file_path = read_file(download_dir)
                subtitle_file = file_path.split(".")[0] + ".txt"
                if not os.path.exists(subtitle_file):
                    text = transcribe(file_path)
                    with open(status_file, "r", encoding="utf-8") as f:
                        status = json.load(f)
                        for item in status:
                            if item["url"] == url:
                                item["text"] = text
                                item["status"] = "finished"
                                break
                    with open(status_file, "w", encoding="utf-8") as f:
                        json.dump(status, f)
                else:
                    with open(subtitle_file, "r", encoding="utf-8") as f:
                        text = f.read()
                        with open(status_file, "r", encoding="utf-8") as f:
                            status = json.load(f)
                            for item in status:
                                if item["url"] == url:
                                    item["text"] = text
                                    item["status"] = "finished"
                                    break
                        with open(status_file, "w", encoding="utf-8") as f:
                            json.dump(status, f)
            else:
                with open(status_file, "r", encoding="utf-8") as f:
                    status = json.load(f)
                    for item in status:
                        if item["url"] == url:
                            item["status"] = "failed"
                            break
                with open(status_file, "w", encoding="utf-8") as f:
                    json.dump(status, f)


def main():
    user_id, urls, _ = parse()
    save_dir = os.path.join(BASE_SAVE_PATH, user_id)
    status_file = os.path.join(save_dir, "status.json")
    if not os.path.exists(status_file):
        status = [
            {
                "url": url,
                "status": "processing",
                "text": "",
            }
            for url in urls
        ]

        os.makedirs(save_dir)
        with open(status_file, "w", encoding="utf-8") as f:
            json.dump(status, f)

        t = threading.Thread(target=download_and_transcribe, args=(urls, save_dir), daemon=True)
        t.start()

        return status
    else:
        with open(status_file, "r", encoding="utf-8") as f:
            status = json.load(f)
        if len(urls) != len(status):
            # 把没有的url加到顶部
            for url in urls:
                if url not in [item["url"] for item in status]:
                    status.insert(0, {"url": url, "status": "processing", "text": ""})
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status, f)

        t = threading.Thread(target=download_and_transcribe, args=(urls, save_dir), daemon=True)
        t.start()
        with open(status_file, "r", encoding="utf-8") as f:
            status = json.load(f)
            return status
