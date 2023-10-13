# bilivideo-transcribe-rss

生成指定 bilibili 用户的投稿feed，并自动将视频转换为文本。
## 原理

1. 通过 RSSHUB 获取用户的投稿feed
2. 将 feed 中的视频下载到本地的指定目录
3. 使用 faster-whisper 将视频转为文本
4. 生成 feed

## 安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install .

# dev
flask --app ./src/bilivideo_transcribe_rss run --debug
```

### GPU

如果需要使用 GPU ，需要自行安装 cuda 相关依赖，然后安装对应版本的 `pytorch` 。

## 使用

1. 复制 .env.example 为 .env ，并修改其中的配置。

```env
# 数据保存的地址
BASE_SAVE_PATH=""
# RSSHUB 服务的域名
RSSHUB_HOST="rsshub.app"
```

2. 启动 flask 服务，然后访问 `http://localhost:5000/{bilibili_user_id}` 。初次访问会触发视频下载和文本转录，返回的 feed 中，内容为空。转换完成后再次访问即可获得完整结果。

