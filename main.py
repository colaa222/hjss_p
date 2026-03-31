from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.schemas import SendRequest
from app.kakao_win import send_one_kakao

app = FastAPI(title="Kakao Internal Tool")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.post("/api/send")
def api_send(payload: SendRequest):
    target = payload.target.strip()
    message = payload.message.strip()

    if not target:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "message": "대상 이름을 입력하세요."},
        )

    if not message:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "message": "메시지를 입력하세요."},
        )

    result = send_one_kakao(target, message)
    status_code = 200 if result.get("ok") else 500
    return JSONResponse(status_code=status_code, content=result)
