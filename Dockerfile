FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

SHELL ["/bin/bash", "-c"]

RUN pip install gunicorn

RUN mkdir -p /app

WORKDIR /app
COPY ./requirements.lock /app/requirements.lock
COPY ./pyproject.toml /app/pyproject.toml
RUN cp requirements.lock requirements.txt
RUN pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118
COPY . /app

WORKDIR /app/src
# gunicorn
CMD ["gunicorn", "bilivideo_transcribe_rss:app", "-b", "0.0.0.0:5000"]
