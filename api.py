import os
import time
import requests
import logging
import base64
from datetime import datetime

logger = logging.getLogger(__name__)

def upload_photos_to_storage(photos_base64: list, object_id: str, delivery_id: str, date: str = None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    url = f"https://building-s3-api.itc-hub.ru/upload/delivery/{object_id}/{delivery_id}"
    payload = {
        "photos_base64": photos_base64,
        "date": date
    }
    
    try:
        logger.info(f"Загружаю {len(photos_base64)} изображений в хранилище")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Изображения успешно загружены в хранилище")
            
            file_urls = []
            if 'files' in result:
                for file_info in result['files']:
                    if 'presigned_url' in file_info:
                        file_urls.append(file_info['presigned_url'])
            
            return file_urls
        else:
            logger.error(f"Ошибка загрузки в хранилище: {response.status_code}")
            logger.error(f"Ответ сервера: {response.text}")
            return []
            
    except Exception as e:
        logger.error(f"Ошибка загрузки в хранилище: {str(e)}")
        return []

 
