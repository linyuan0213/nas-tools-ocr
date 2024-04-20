import ddddocr
import cv2
import base64
import numpy as np
from PIL import Image
from loguru import logger


class CaptchaOcr:
    @staticmethod
    def around_white(img):
        """
        四周置白色
        """
        w, h = img.shape
        for _w in range(w):
            for _h in range(h):
                if (_w <= 5) or (_h <= 5) or (_w >= w-5) or (_h >= h-5):
                    img.itemset((_w, _h), 255)
        return img

    @staticmethod
    def noise_unsome_piexl(img):
        '''
        邻域非同色降噪
        查找像素点上下左右相邻点的颜色，如果是非白色的非像素点颜色，则填充为白色
        '''
        w, h = img.shape
        for _w in range(w):
            for _h in range(h):
                if _h != 0 and _w != 0 and _w < w - 1 and _h < h - 1:# 剔除顶点、底点
                    center_color = img[_w, _h] # 当前坐标颜色
                    top_color = img[_w, _h + 1]
                    bottom_color = img[_w, _h - 1]
                    left_color = img[_w - 1, _h]
                    right_color = img[_w + 1, _h]
                    cnt = 0
                    if top_color.all() == center_color.all():
                        cnt += 1
                    if bottom_color.all() == center_color.all():
                        cnt += 1
                    if left_color.all() == center_color.all():
                        cnt += 1
                    if right_color.all() == center_color.all():
                        cnt += 1
                    if cnt < 1:
                        img.itemset((_w, _h), 255)
        return img
    @staticmethod
    def replace_strings(text, replacements):
        """
        替换多个字符串
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def image_pre_process(self, image):
        """
        图片预处理
        """
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        denoised_image = cv2.fastNlMeansDenoising(binary_image, h=30, templateWindowSize=11, searchWindowSize=21)
        noise_unsome = CaptchaOcr.noise_unsome_piexl(denoised_image)
        op_image = CaptchaOcr.around_white(noise_unsome)

        return op_image

    def recognize_captcha(self, image_content):
        """
        识别验证码
        """
        res = ""
        try:
            ocr = ddddocr.DdddOcr(show_ad=False)
            image = np.asarray(bytearray(image_content), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            op_image = self.image_pre_process(image)
            pil_image = Image.fromarray(cv2.cvtColor(op_image, cv2.COLOR_BGR2RGB))
            res = ocr.classification(pil_image)
            res = CaptchaOcr.replace_strings(res, {'之': '2', '>': '7'})
            return res.upper()
        except Exception as e:
            logger.error(f"{str(e)}：{res}")
            return res

    def get_captcha_text(self, image_b64):
        """
        获取验证码图片，并识别内容
        :param image_b64: 图片base64
        """

        if image_b64:
            image_bin = base64.b64decode(image_b64.encode('utf-8'))
            return self.recognize_captcha(image_bin)
        else:
            return ""
