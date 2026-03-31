from openpyxl import load_workbook
from pathlib import Path
from datetime import datetime


def read_targets_from_excel(file_path: str, sheet_name: str | None = None) -> list[dict]:
    wb = load_workbook(file_path)
    ws = wb[sheet_name] if sheet_name else wb.active

    rows = []
    row_no = 2

    while True:
        target = ws[f"A{row_no}"].value
        message = ws[f"B{row_no}"].value
        send_status = ws[f"C{row_no}"].value

        if target is None and message is None:
            break

        rows.append(
            {
                "excel_row": row_no,
                "target": "" if target is None else str(target).strip(),
                "message": "" if message is None else str(message).strip(),
                "send_status": send_status,
            }
        )

        row_no += 1

    return rows


def write_results_to_excel(
    file_path: str,
    results: list[dict],
    status_col: str = "C",
    detail_col: str = "D",
    sheet_name: str | None = None,
) -> str:
    wb = load_workbook(file_path)
    ws = wb[sheet_name] if sheet_name else wb.active

    for item in results:
        row_no = item.get("excel_row")
        if not row_no:
            continue

        ws[f"{status_col}{row_no}"] = 1 if item.get("ok") else 0
        ws[f"{detail_col}{row_no}"] = item.get("message_detail", "")

    try:
        wb.save(file_path)
        return file_path

    except PermissionError:
        path = Path(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        new_file = (
            path.parent
            / f"{path.stem}_result_{timestamp}{path.suffix}"
        )

        wb.save(str(new_file))
        return str(new_file)