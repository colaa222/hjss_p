import time
import random

from app.kakao_win import send_one_kakao
from app.email_service import send_one_email

DEDUP_SECONDS = 5.0
_RECENT_SEND_CACHE: dict[tuple[str, str, str], float] = {}


def _cleanup_recent_cache(now: float) -> None:
    expired_keys = [
        key
        for key, ts in _RECENT_SEND_CACHE.items()
        if (now - ts) > DEDUP_SECONDS
    ]
    for key in expired_keys:
        _RECENT_SEND_CACHE.pop(key, None)


def is_duplicate_send(channel: str, unique_target: str, message: str) -> bool:
    now = time.time()
    key = (
        channel.strip().lower(),
        unique_target.strip(),
        message.strip(),
    )

    _cleanup_recent_cache(now)

    last_sent_at = _RECENT_SEND_CACHE.get(key)
    if last_sent_at is not None and (now - last_sent_at) < DEDUP_SECONDS:
        return True

    _RECENT_SEND_CACHE[key] = now
    return False


def send_many(
    rows: list[dict],
    min_delay_seconds: float = 2.5,
    max_delay_seconds: float = 4.5,
) -> list[dict]:
    """
    rows 예시:
    [
        {
            "excel_row": 2,
            "channel": "kakao",
            "target": "다솜이",
            "message": "안녕하세요"
        },
        {
            "excel_row": 3,
            "channel": "email",
            "to_email": "test@naver.com",
            "subject": "테스트",
            "message": "안녕하세요"
        },
    ]
    """
    results = []

    for idx, row in enumerate(rows):
        excel_row = row.get("excel_row")
        channel = str(row.get("channel", "")).strip().lower()
        target = str(row.get("target", "")).strip()
        to_email = str(row.get("to_email", "")).strip()
        subject = str(row.get("subject", "")).strip()
        message = str(row.get("message", "")).strip()

        if channel == "kakao":
            if not target or not message:
                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "target": target,
                        "message": message,
                        "ok": False,
                        "step": "validate_row",
                        "message_detail": "kakao는 target, message가 필요합니다.",
                    }
                )
            elif is_duplicate_send(channel, target, message):
                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "target": target,
                        "message": message,
                        "ok": False,
                        "step": "dedup_skip",
                        "message_detail": "최근 5초 내 동일 카카오 요청으로 발송을 건너뜁니다.",
                    }
                )
            else:
                result = send_one_kakao(target, message)

                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "target": target,
                        "message": message,
                        "ok": result.get("ok", False),
                        "step": result.get("step"),
                        "message_detail": result.get("message"),
                        "raw_result": result,
                    }
                )

        elif channel == "email":
            if not to_email or not subject or not message:
                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "to_email": to_email,
                        "subject": subject,
                        "message": message,
                        "ok": False,
                        "step": "validate_row",
                        "message_detail": "email은 to_email, subject, message가 필요합니다.",
                    }
                )
            elif is_duplicate_send(channel, to_email, message):
                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "to_email": to_email,
                        "subject": subject,
                        "message": message,
                        "ok": False,
                        "step": "dedup_skip",
                        "message_detail": "최근 5초 내 동일 이메일 요청으로 발송을 건너뜁니다.",
                    }
                )
            else:
                result = send_one_email(to_email, subject, message)

                results.append(
                    {
                        "excel_row": excel_row,
                        "channel": channel,
                        "to_email": to_email,
                        "subject": subject,
                        "message": message,
                        "ok": result.get("ok", False),
                        "step": result.get("step"),
                        "message_detail": result.get("message"),
                        "raw_result": result,
                    }
                )

        else:
            results.append(
                {
                    "excel_row": excel_row,
                    "channel": channel,
                    "ok": False,
                    "step": "validate_row",
                    "message_detail": "channel은 kakao 또는 email이어야 합니다.",
                }
            )

        if idx < len(rows) - 1:
            delay = random.uniform(min_delay_seconds, max_delay_seconds)
            time.sleep(delay)

    return results


# 랜덤 딜레이 버전 

# app/sender.py


# import time
# import random

# from app.kakao_win import send_one_kakao

# DEDUP_SECONDS = 5.0
# _RECENT_SEND_CACHE: dict[tuple[str, str], float] = {}


# def _cleanup_recent_cache(now: float) -> None:
#     expired_keys = [
#         key
#         for key, ts in _RECENT_SEND_CACHE.items()
#         if (now - ts) > DEDUP_SECONDS
#     ]
#     for key in expired_keys:
#         _RECENT_SEND_CACHE.pop(key, None)


# def is_duplicate_send(target: str, message: str) -> bool:
#     now = time.time()
#     key = (target.strip(), message.strip())

#     _cleanup_recent_cache(now)

#     last_sent_at = _RECENT_SEND_CACHE.get(key)
#     if last_sent_at is not None and (now - last_sent_at) < DEDUP_SECONDS:
#         return True

#     _RECENT_SEND_CACHE[key] = now
#     return False


# def send_many(
#     rows: list[dict],
#     min_delay_seconds: float = 2.5,
#     max_delay_seconds: float = 4.5,
# ) -> list[dict]:
#     """
#     rows 예시:
#     [
#         {"excel_row": 2, "target": "다솜이", "message": "안녕하세요"},
#         {"excel_row": 3, "target": "임상민", "message": "테스트"},
#     ]
#     """
#     results = []

#     for idx, row in enumerate(rows):
#         excel_row = row.get("excel_row")
#         target = str(row.get("target", "")).strip()
#         message = str(row.get("message", "")).strip()

#         if not target or not message:
#             results.append(
#                 {
#                     "excel_row": excel_row,
#                     "target": target,
#                     "message": message,
#                     "ok": False,
#                     "step": "validate_row",
#                     "message_detail": "target 또는 message가 비어 있습니다.",
#                 }
#             )
#         elif is_duplicate_send(target, message):
#             results.append(
#                 {
#                     "excel_row": excel_row,
#                     "target": target,
#                     "message": message,
#                     "ok": False,
#                     "step": "dedup_skip",
#                     "message_detail": "최근 5초 내 동일 요청으로 발송을 건너뜁니다.",
#                 }
#             )
#         else:
#             result = send_one_kakao(target, message)

#             results.append(
#                 {
#                     "excel_row": excel_row,
#                     "target": target,
#                     "message": message,
#                     "ok": result.get("ok", False),
#                     "step": result.get("step"),
#                     "message_detail": result.get("message"),
#                     "raw_result": result,
#                 }
#             )

#         if idx < len(rows) - 1:
#             delay = random.uniform(
#                 min_delay_seconds,
#                 max_delay_seconds,
#             )
#             time.sleep(delay)

#     return results