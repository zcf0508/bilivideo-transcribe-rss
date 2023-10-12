import os


def read_file(video_dir: str) -> str:
    return os.path.join(
        video_dir,
        os.listdir(video_dir)[0],
        "Videos",
        os.listdir(os.path.join(video_dir, os.listdir(video_dir)[0], "Videos"))[0],
    )
