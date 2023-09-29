from typing import Dict

from fastapi import FastAPI, File, UploadFile, Query, Path
from fastapi.responses import FileResponse

from excel_file import read_excel
from database import add_file, add_data, init_db, download_data, \
    get_diagram_data

app = FastAPI()


@app.on_event('startup')
def init() -> Dict[str, bool]:
    init_db()
    return {'result': True}


@app.get('/route_for_test')
def route_for_test():
    return {'result': True}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)) -> Dict[str, bool]:
    version = add_file(name=file.filename)
    data = read_excel(file)
    add_data(data, version)
    return {'result': True}


@app.get('/download/{version}')
async def download(version: int = Path(
    ...,
    title='Download file with required version of uploaded file.'
)) -> FileResponse:
    download_data(version)
    return FileResponse(path='test.xlsx', filename='excel.xlsx',
                        media_type='multipart/form-data')


@app.get('/diagram/')
def get_diagram_json(
        version: int = Query(
            1,
            title='Version of downloaded file',
        ),
        year: int = Query(
            2022,
            title='Year of required data',
        ),
        kind: str = Query(
            'plan',
            title='Kind of value: plan or fact',
        )) -> Dict[str, str]:
    return get_diagram_data(version, year, kind)
