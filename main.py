# main.py

import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.schemas import SendRequest
from app.kakao_win import send_one_kakao
from app.excel_service import (
    read_targets_from_excel,
    write_results_to_excel,
)
from app.sender import send_many, is_duplicate_send

app = FastAPI(title="Kakao Internal Tool")
templates = Jinja2Templates(directory="templates")

#--- email ---

from pydantic import BaseModel
from app.email_service import send_one_email


class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str


@app.post("/api/send-email")
def api_send_email(payload: EmailRequest):
    result = send_one_email(
        payload.to_email.strip(),
        payload.subject.strip(),
        payload.body.strip(),
    )

    status_code = 200 if result.get("ok") else 500
    return JSONResponse(status_code=status_code, content=result)

#--- end ---

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.post("/api/send")
def api_send(payload: SendRequest):
    request_id = str(uuid.uuid4())

    target = payload.target.strip()
    message = payload.message.strip()

    print(
        f"[SEND REQUEST] request_id={request_id} "
        f"target={target} message_len={len(message)}"
    )

    if not target:
        return JSONResponse(
            status_code=400,
            content={
                "request_id": request_id,
                "ok": False,
                "message": "대상 이름을 입력하세요.",
            },
        )

    if not message:
        return JSONResponse(
            status_code=400,
            content={
                "request_id": request_id,
                "ok": False,
                "message": "메시지를 입력하세요.",
            },
        )

    if is_duplicate_send(target, message):
        return JSONResponse(
            status_code=409,
            content={
                "request_id": request_id,
                "ok": False,
                "step": "dedup_skip",
                "message": "최근 5초 내 동일 요청으로 발송을 건너뜁니다.",
                "target": target,
            },
        )

    result = send_one_kakao(target, message)
    result["request_id"] = request_id

    status_code = 200 if result.get("ok") else 500
    return JSONResponse(status_code=status_code, content=result)


@app.post("/api/send-excel")
def api_send_excel():
    request_id = str(uuid.uuid4())
    file_path = "sample.xlsx"

    print(f"[SEND EXCEL REQUEST] request_id={request_id} file_path={file_path}")

    rows = read_targets_from_excel(file_path)
    results = send_many(rows)
    write_results_to_excel(file_path, results)

    success_count = sum(1 for r in results if r.get("ok"))
    fail_count = len(results) - success_count

    return {
        "request_id": request_id,
        "ok": True,
        "file_path": file_path,
        "total": len(results),
        "success": success_count,
        "fail": fail_count,
        "results": results,
    }


@app.post("/api/resend-failed")
def api_resend_failed():
    request_id = str(uuid.uuid4())
    file_path = "sample.xlsx"

    print(f"[RESEND FAILED REQUEST] request_id={request_id} file_path={file_path}")

    rows = read_targets_from_excel(file_path)

    failed_rows = [
        row for row in rows
        if row.get("send_status") == 0
    ]

    results = send_many(failed_rows)
    write_results_to_excel(file_path, results)

    success_count = sum(1 for r in results if r.get("ok"))
    fail_count = len(results) - success_count

    return {
        "request_id": request_id,
        "ok": True,
        "mode": "failed_only",
        "file_path": file_path,
        "total": len(results),
        "success": success_count,
        "fail": fail_count,
        "results": results,
    }