from fastapi import APIRouter, Request
from app.logic._extractor import Extractor

router = APIRouter()
xml_extractor = Extractor()


@router.get("/extract_xml")
async def custom_endpoint():
    result = xml_extractor.extract()
    return {"result": result}
