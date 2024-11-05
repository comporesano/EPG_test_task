from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Здесь вы можете сохранить файл или обработать его
    with open(file.filename, "wb") as f:
        f.write(contents)
    return {"filename": file.filename}
