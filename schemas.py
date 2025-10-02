from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ImageRequest(BaseModel):
    images_base64: List[str]
    object_id: str
    delivery_id: str
    date: Optional[str] = None

class ProcessedData(BaseModel):
    data: Dict[str, Any]
    file_url: str

class ExtractResponse(BaseModel):
    results: List[ProcessedData]