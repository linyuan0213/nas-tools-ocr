FROM python:3.10-slim-buster

RUN mkdir -p /app/ocr_app

COPY ./*.txt ./*.py ./*.sh ./*.onnx /app/
COPY ./ocr_app/*.py /app/ocr_app/


RUN cd /app \
    && python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple\
    && pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf /tmp/* && rm -rf /root/.cache/* \
    && sed -i 's#http://deb.debian.org#http://mirrors.aliyun.com/#g' /etc/apt/sources.list\
    && apt-get --allow-releaseinfo-change update && apt install libgl1-mesa-glx libglib2.0-0 -y

WORKDIR /app

CMD ["python3", "ocr_server.py"]