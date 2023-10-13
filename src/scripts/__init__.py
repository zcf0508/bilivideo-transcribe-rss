import subprocess


def dev():
    subprocess.run(["flask", "--app", "./src/bilivideo_transcribe_rss", "run", "--debug"])
