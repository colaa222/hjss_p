from app.kakao_win import send_one_kakao


def send_many(rows: list[dict]) -> list[dict]:
    """
    rows 예시:
    [
        {"excel_row": 2, "target": "다솜이", "message": "안녕하세요"},
        {"excel_row": 3, "target": "임상민", "message": "테스트"},
    ]
    """
    results = []

    for row in rows:
        excel_row = row.get("excel_row")
        target = str(row.get("target", "")).strip()
        message = str(row.get("message", "")).strip()

        if not target or not message:
            results.append(
                {
                    "excel_row": excel_row,
                    "target": target,
                    "message": message,
                    "ok": False,
                    "step": "validate_row",
                    "message_detail": "target 또는 message가 비어 있습니다.",
                }
            )
            continue

        result = send_one_kakao(target, message)

        results.append(
            {
                "excel_row": excel_row,
                "target": target,
                "message": message,
                "ok": result.get("ok", False),
                "step": result.get("step"),
                "message_detail": result.get("message"),
                "raw_result": result,
            }
        )

    return results