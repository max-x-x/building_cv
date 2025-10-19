import pytesseract
from PIL import Image
import base64
import io
import requests
import logging

logger = logging.getLogger(__name__)

def extract_text_from_base64(image_base64, lang='rus'):
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        logger.error(f"Ошибка распознавания текста: {str(e)}")
        return ""

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    except Exception as e:
        logger.error(f"Ошибка кодирования изображения: {str(e)}")
        return ""

def send_text_to_external_api(text: str, image_index: int):
    try:
        external_url = "https://building-ai.itc-hub.ru/extract"
        payload = {"text": text}
        
        logger.info(f"Отправляю текст для изображения {image_index + 1} во внешний API")
        logger.debug(f"Предпросмотр текста: {text[:100]}...")
        
        response = requests.post(external_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Изображение {image_index + 1} обработано внешним API")
            logger.debug(f"Ответ API: {result}")
            return result
        else:
            logger.error(f"Ошибка внешнего API для изображения {image_index + 1}: {response.status_code}")
            logger.error(f"Ответ сервера: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Ошибка подключения для изображения {image_index + 1}")
        return None
    except Exception as e:
        logger.error(f"Ошибка запроса для изображения {image_index + 1}: {str(e)}")
        return None




