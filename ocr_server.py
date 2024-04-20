import base64
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from ocr_app.ocr import CaptchaOcr


app = FastAPI()


class OCR(BaseModel):
    image_b64: str


@app.post("/ocr/base64")
async def captcha(data: OCR):
    ocr = CaptchaOcr()
    image_b64 = data.model_dump().get("image_b64")
    img_b = base64.b64decode(image_b64.encode('utf-8'))

    try:
        res = ocr.recognize_captcha(img_b)
        logger.info(f"识别成功， 验证码为 {res}")
    except Exception as e:
        logger.error(f"识别失败: {e}")
        return {"code": -1, "res": ""}
    return {"code": 0, "res": res}


if __name__ == '__main__':
    uvicorn.run('ocr_server:app', host="0.0.0.0", port=9300, reload=False)
