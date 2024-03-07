import os

from app.configs.config import InternalConfig
from app.logic._extractor import Extractor
from app.logic._fuzzy_extractor import FuzzyLLMKeyFinder, LLMXMLParser

from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi_utils.tasks import repeat_every

router = APIRouter()
xml_extractor = Extractor()
fuzzy_llm_key_finder = FuzzyLLMKeyFinder()
llm_xml_parser = LLMXMLParser()


@router.get("/extract_xml")
async def extract_xml(file_name: str):
    try:
        result = xml_extractor.extract(file_name)
        return {"result": "Successfully created products..."}
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Error while extracting XML data... :: {exc}"
        )


@router.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
async def periodic_xml_check() -> None:
    try:
        xml_extractor.extract_periodically()
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Error while extracting XML data... :: {exc}"
        )


@router.post("/upload_xml_file")
async def upload_xml_file(file: UploadFile = File(...)):
    try:
        with open(
            os.path.join(InternalConfig.ASSETS_DIR_PATH, file.filename), "wb"
        ) as buffer:
            buffer.write(await file.read())
        return {"filename": file.filename}
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Error while uploading XML file... :: {exc}"
        )


@router.get("/fuzzy_keyword_finder")
async def fuzzy_keyword_finder(keyword: str, token: str):
    try:

        result = fuzzy_llm_key_finder.analyze_key(keyword, token)

        return {"result": result}
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Error while extracting XML data... :: {exc}"
        )


@router.get("/llm_xml_parser")
def llm_xml_parser_func(token: str):
    try:
        result = llm_xml_parser.parse_xml(token)
        return {"result": result}
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Error while extracting XML data... :: {exc}"
        )
