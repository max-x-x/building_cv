from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from schemas import ExtractResponse, ImageRequest, ProcessedData
import os
import json
import logging
from utils import extract_text_from_base64, send_text_to_external_api
from api import upload_photos_to_storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok"}


@router.post("/extract", response_model=ExtractResponse)
async def extract_text(request: ImageRequest):
    try:
        results = []
        
        file_urls = upload_photos_to_storage(
            request.images_base64, 
            request.object_id, 
            request.delivery_id, 
            request.date
        )
        
        if not file_urls:
            logger.error("Не удалось загрузить изображения в хранилище")
            raise HTTPException(status_code=500, detail="Ошибка загрузки изображений в хранилище")
        
        for i, image_base64 in enumerate(request.images_base64):
            logger.info(f"Обрабатываю изображение {i + 1} из {len(request.images_base64)}")
            
            text = extract_text_from_base64(image_base64)
            file_url = file_urls[i] if i < len(file_urls) else ""
            
            external_api_result = send_text_to_external_api(text, i)
            
            if external_api_result and 'result' in external_api_result:
                try:
                    structured_data = json.loads(external_api_result['result'])
                    results.append(ProcessedData(data=structured_data, file_url=file_url))
                    logger.info(f"Изображение {i + 1} обработано")
                except json.JSONDecodeError as e:
                    logger.error(f"Ошибка разбора JSON для изображения {i + 1}: {e}")
                    empty_data = {
                        "Наименование материала": "",
                        "Количество материала": "",
                        "Размер": "",
                        "Объем": "",
                        "Нетто": ""
                    }
                    results.append(ProcessedData(data=empty_data, file_url=file_url))
            else:
                logger.warning(f"Внешний API недоступен для изображения {i + 1}, возвращаю пустые данные")
                empty_data = {
                    "Наименование материала": "",
                    "Количество материала": "",
                    "Размер": "",
                    "Объем": "",
                    "Нетто": ""
                }
                results.append(ProcessedData(data=empty_data, file_url=file_url))
        
        logger.info(f"Обработка завершена. Результатов: {len(results)}")
        return ExtractResponse(results=results)
    except Exception as e:
        logger.error(f"Критическая ошибка обработки: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Ошибка обработки изображений: {str(e)}")