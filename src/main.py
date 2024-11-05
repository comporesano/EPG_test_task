from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

from schemas import UserCreateScheme

from api import all_routers

app = FastAPI(title="EPG Test Task", summary="Clients operation API")

for router in all_routers:
    app.include_router(router=router, prefix="/api")

# @app.post("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     # Здесь вы можете сохранить файл или обработать его
#     with open(file.filename, "wb") as f:
#         f.write(contents)
#     return {"filename": file.filename}
