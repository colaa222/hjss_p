from openpyxl import load_workbook


def read_targets_from_excel(file_path: str) -> list[dict]:
    wb = load_workbook(file_path)
    ws = wb.active

    rows = []

    for row_idx in range(2, ws.max_row + 1):
        channel = ws[f"A{row_idx}"].value
        target = ws[f"B{row_idx}"].value
        to_email = ws[f"C{row_idx}"].value
        subject = ws[f"D{row_idx}"].value
        message = ws[f"E{row_idx}"].value
        send_status = ws[f"F{row_idx}"].value
        detail = ws[f"G{row_idx}"].value

        # 완전히 빈 행은 스킵
        if not any([channel, target, to_email, subject, message]):
            continue

        rows.append(
            {
                "excel_row": row_idx,
                "channel": str(channel).strip() if channel is not None else "",
                "target": str(target).strip() if target is not None else "",
                "to_email": str(to_email).strip() if to_email is not None else "",
                "subject": str(subject).strip() if subject is not None else "",
                "message": str(message).strip() if message is not None else "",
                "send_status": send_status,
                "detail": str(detail).strip() if detail is not None else "",
            }
        )

    return rows


def write_results_to_excel(file_path: str, results: list[dict]) -> str:
    wb = load_workbook(file_path)
    ws = wb.active

    for result in results:
        row_idx = result.get("excel_row")
        if not row_idx:
            continue

        ok = result.get("ok", False)
        step = result.get("step", "")
        message_detail = result.get("message_detail", "")

        ws[f"F{row_idx}"] = 1 if ok else 0
        ws[f"G{row_idx}"] = f"{step}: {message_detail}" if step else message_detail

    wb.save(file_path)
    return file_path