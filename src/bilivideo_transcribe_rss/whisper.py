from faster_whisper import WhisperModel


def transcribe(
    file_path: str,
) -> str:
    file_name = file_path.split("/")[-1].split(".")[0]

    model_size = "medium"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    segments, _ = model.transcribe(
        file_path,
        language="zh",
        # https://github.com/guillaumekln/faster-whisper/issues/71
        temperature=0,
        initial_prompt=f"视频标题是《{file_name}》,使用简体中文，增加标点。",
        vad_filter=True,
    )

    segments = list(segments)

    text: str = " ".join([segment.text for segment in segments])

    del model

    # 保存到同名的 txt 文本中
    subtitle_file = file_path.split(".")[0] + ".txt"
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write(text)

    return text
