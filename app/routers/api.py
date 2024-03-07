from app.logic._extractor import Extractor

from fastapi import APIRouter, Request
from fastapi_utils.tasks import repeat_every

router = APIRouter()
xml_extractor = Extractor()


@router.get("/extract_xml")
async def custom_endpoint(file_name: str):
    result = xml_extractor.extract(file_name)
    return {"result": result}


@router.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
async def periodic_xml_check() -> None:
    xml_extractor.extract_periodically()
