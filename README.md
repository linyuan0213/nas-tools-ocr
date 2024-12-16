# Nas-tools Ocr Server

### 运行方式

  - 直接安装

    ```sh
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

    python ocr_server.py
    ```

  - 通过 docker 部署

    ```
    docker run -p 9300:9300 -d linyuan0213/nas-tools-ocr:latest
    ```

