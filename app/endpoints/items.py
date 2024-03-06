from fastapi import APIRouter, Request
from app.logic._extractor import Extractor
from app.database.mongo_utils import MongoDB

router = APIRouter()


@router.get("/extract_xml")
async def custom_endpoint(request: Request):
    mongo: MongoDB = request.app.state.mongo
    xml_extractor = Extractor
    result = xml_extractor.extract()
    return {"result": result}
