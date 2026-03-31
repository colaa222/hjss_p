import time
from typing import Any

import win32api
import win32clipboard
import win32con
import win32gui


def _safe_get_window_text(hwnd: int) -> str:
    try:
        return win32gui.GetWindowText(hwnd)
    except Exception:
        return ""


def _safe_get_class_name(hwnd: int) -> str:
    try:
        return win32gui.GetClassName(hwnd)
    except Exception:
        return ""


def find_kakao_main_window() -> int:
    """
    카카오톡 메인 목록창 찾기
    """
    found: list[int] = []

    def enum_handler(hwnd: int, _lparam: Any) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = _safe_get_window_text(hwnd)
        class_name = _safe_get_class_name(hwnd)

        if "EVA_Window_Dblclk" in class_name and (
            "카카오톡" in title or "KakaoTalk" in title
        ):
            found.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return found[0] if found else 0


def wait_for_kakao_main_window(timeout: float = 5.0, interval: float = 0.2) -> int:
    start = time.time()
    while time.time() - start < timeout:
        hwnd = find_kakao_main_window()
        if hwnd:
            return hwnd
        time.sleep(interval)
    return 0


def list_child_windows(parent_hwnd: int, limit: int = 300) -> list[dict]:
    """
    디버깅용 자식 컨트롤 목록
    """
    items: list[dict] = []

    def enum_child(hwnd: int, _lparam: Any) -> None:
        if len(items) >= limit:
            return

        items.append(
            {
                "hwnd": hwnd,
                "class_name": _safe_get_class_name(hwnd),
                "title": _safe_get_window_text(hwnd),
                "parent": win32gui.GetParent(hwnd),
            }
        )

    win32gui.EnumChildWindows(parent_hwnd, enum_child, None)
    return items


def find_first_child_by_title_contains(parent_hwnd: int, keyword: str) -> int:
    """
    title에 keyword가 포함된 첫 자식 찾기
    예: ContactListView, ChatRoomListView
    """
    found = 0

    def enum_child(hwnd: int, _lparam: Any) -> None:
        nonlocal found
        if found:
            return

        title = _safe_get_window_text(hwnd)
        if keyword.lower() in title.lower():
            found = hwnd

    win32gui.EnumChildWindows(parent_hwnd, enum_child, None)
    return found


def find_children_by_class_under_parent(parent_hwnd: int, class_name: str, limit: int = 20) -> list[int]:
    found: list[int] = []

    def enum_child(hwnd: int, _lparam: Any) -> None:
        if len(found) >= limit:
            return

        if _safe_get_class_name(hwnd) == class_name:
            found.append(hwnd)

    win32gui.EnumChildWindows(parent_hwnd, enum_child, None)
    return found


def set_edit_text(hwnd_edit: int, text: str) -> bool:
    """
    WM_SETTEXT로 텍스트 넣기
    """
    try:
        win32gui.SendMessage(hwnd_edit, win32con.WM_SETTEXT, 0, text)
        return True
    except Exception:
        return False


def set_foreground(hwnd: int) -> bool:
    """
    창을 앞으로 가져오기
    """
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        return True
    except Exception:
        return False


def focus_window(hwnd: int) -> bool:
    """
    포커스 시도
    """
    try:
        win32gui.SetFocus(hwnd)
        return True
    except Exception:
        return False


def send_real_enter() -> bool:
    """
    실제 키보드 Enter 입력
    """
    try:
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception:
        return False


def send_real_down() -> bool:
    """
    실제 키보드 ↓ 입력
    """
    try:
        win32api.keybd_event(win32con.VK_DOWN, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(win32con.VK_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception:
        return False


def post_enter(hwnd: int) -> bool:
    """
    PostMessage 방식 엔터
    """
    try:
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        return True
    except Exception:
        return False


def set_clipboard_text(text: str) -> bool:
    """
    클립보드에 유니코드 텍스트 설정
    """
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return True
    except Exception:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass
        return False


def send_real_ctrl_v() -> bool:
    """
    실제 Ctrl+V 입력
    """
    try:
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        time.sleep(0.03)

        win32api.keybd_event(ord("V"), 0, 0, 0)
        time.sleep(0.03)
        win32api.keybd_event(ord("V"), 0, win32con.KEYEVENTF_KEYUP, 0)

        time.sleep(0.03)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception:
        return False


def find_top_window_by_exact_title(title: str) -> int:
    found: list[int] = []

    def enum_handler(hwnd: int, _lparam: Any) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        window_title = _safe_get_window_text(hwnd).strip()
        if window_title == title.strip():
            found.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return found[0] if found else 0


def find_top_window_by_title_contains(keyword: str) -> int:
    found: list[int] = []

    def enum_handler(hwnd: int, _lparam: Any) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        window_title = _safe_get_window_text(hwnd).strip()
        if keyword.strip() and keyword.strip() in window_title:
            found.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return found[0] if found else 0


def inspect_search_controls(main_hwnd: int) -> dict:
    """
    메인창 안에서 친구/채팅방 검색 뷰와 Edit 찾기
    """
    contact_view = find_first_child_by_title_contains(main_hwnd, "ContactListView")
    chatroom_view = find_first_child_by_title_contains(main_hwnd, "ChatRoomListView")

    contact_edits = (
        find_children_by_class_under_parent(contact_view, "Edit") if contact_view else []
    )
    chatroom_edits = (
        find_children_by_class_under_parent(chatroom_view, "Edit") if chatroom_view else []
    )

    return {
        "contact_view": contact_view,
        "chatroom_view": chatroom_view,
        "contact_edits": contact_edits,
        "chatroom_edits": chatroom_edits,
    }


def open_chatroom_by_search(main_hwnd: int, search_edit: int, target: str, wait_sec: float = 2.0) -> dict:
    """
    채팅방 검색 후 엔터로 방 열기
    1차: 실제 엔터
    2차: ↓ + 엔터
    exact / contains 둘 다 검사
    """
    input_ok = set_edit_text(search_edit, target)
    time.sleep(0.5)

    if not input_ok:
        return {
            "ok": False,
            "step": "set_search_text",
            "message": "검색창 텍스트 입력에 실패했습니다.",
        }

    fg_ok = set_foreground(main_hwnd)
    time.sleep(0.2)

    focus_ok = focus_window(search_edit)
    time.sleep(0.2)

    enter_ok = send_real_enter()
    time.sleep(wait_sec)

    chat_hwnd = find_top_window_by_exact_title(target)
    if not chat_hwnd:
        chat_hwnd = find_top_window_by_title_contains(target)

    second_try = False
    if not chat_hwnd:
        send_real_down()
        time.sleep(0.2)
        send_real_enter()
        second_try = True
        time.sleep(wait_sec)

        chat_hwnd = find_top_window_by_exact_title(target)
        if not chat_hwnd:
            chat_hwnd = find_top_window_by_title_contains(target)

    return {
        "ok": bool(chat_hwnd),
        "step": "open_chatroom",
        "message": "검색 후 엔터로 채팅방 열기 테스트 완료",
        "input_ok": input_ok,
        "fg_ok": fg_ok,
        "focus_ok": focus_ok,
        "enter_ok": enter_ok,
        "second_try": second_try,
        "chat_hwnd": chat_hwnd,
    }


def inspect_chatroom_input_controls(chat_hwnd: int) -> dict:
    """
    열린 채팅방 내부에서 입력창 후보 찾기
    """
    children = list_child_windows(chat_hwnd, limit=300)
    edit_candidates = find_children_by_class_under_parent(chat_hwnd, "Edit", limit=50)
    richedit_candidates = find_children_by_class_under_parent(chat_hwnd, "RICHEDIT50W", limit=50)
    richedit_candidates += find_children_by_class_under_parent(chat_hwnd, "RichEdit50W", limit=50)

    richedit_candidates = list(dict.fromkeys(richedit_candidates))

    return {
        "children": children[:80],
        "edit_candidates": edit_candidates,
        "richedit_candidates": richedit_candidates,
    }


def choose_chat_input_hwnd(chat_input_info: dict) -> int:
    """
    우선순위:
    1) RICHEDIT50W / RichEdit50W
    2) Edit
    """
    richedit_candidates = chat_input_info.get("richedit_candidates", [])
    edit_candidates = chat_input_info.get("edit_candidates", [])

    if richedit_candidates:
        return richedit_candidates[0]

    if edit_candidates:
        return edit_candidates[0]

    return 0


def send_chat_text(chat_hwnd: int, input_hwnd: int, message: str) -> dict:
    """
    클립보드 + 실제 Ctrl+V + 실제 Enter 방식
    """
    fg_ok = set_foreground(chat_hwnd)
    time.sleep(0.3)

    focus_ok = focus_window(input_hwnd)
    time.sleep(0.2)

    clip_ok = set_clipboard_text(message)
    time.sleep(0.1)

    if not clip_ok:
        return {
            "ok": False,
            "step": "set_clipboard_text",
            "message": "클립보드에 메시지 설정 실패",
            "chat_hwnd": chat_hwnd,
            "input_hwnd": input_hwnd,
            "fg_ok": fg_ok,
            "focus_ok": focus_ok,
        }

    paste_ok = send_real_ctrl_v()
    time.sleep(0.4)

    if not paste_ok:
        return {
            "ok": False,
            "step": "send_real_ctrl_v",
            "message": "실제 Ctrl+V 붙여넣기 실패",
            "chat_hwnd": chat_hwnd,
            "input_hwnd": input_hwnd,
            "fg_ok": fg_ok,
            "focus_ok": focus_ok,
            "clip_ok": clip_ok,
        }

    # 붙여넣기 후 카카오 UI 반응 대기
    time.sleep(0.5)

    enter_ok = send_real_enter()
    time.sleep(0.5)

    return {
        "ok": enter_ok,
        "step": "send_chat_text",
        "message": "클립보드 붙여넣기 후 엔터 전송 완료",
        "chat_hwnd": chat_hwnd,
        "input_hwnd": input_hwnd,
        "fg_ok": fg_ok,
        "focus_ok": focus_ok,
        "clip_ok": clip_ok,
        "paste_ok": paste_ok,
        "enter_ok": enter_ok,
    }


def send_one_kakao(target: str, message: str) -> dict:
    """
    전체 1건 발송 흐름
    1) 메인창 찾기
    2) 채팅방 검색창 찾기
    3) 검색 후 엔터로 방 열기
    4) 열린 채팅방 입력창 찾기
    5) 클립보드 붙여넣기 후 엔터 전송
    """
    main_hwnd = wait_for_kakao_main_window(timeout=5.0)
    if not main_hwnd:
        return {
            "ok": False,
            "step": "find_kakao_main_window",
            "message": "카카오톡 메인창을 찾지 못했습니다.",
        }

    search_info = inspect_search_controls(main_hwnd)
    chatroom_view = search_info["chatroom_view"]
    chatroom_edits = search_info["chatroom_edits"]

    if not chatroom_view:
        return {
            "ok": False,
            "step": "find_chatroom_view",
            "message": "ChatRoomListView를 찾지 못했습니다.",
            "inspect": search_info,
        }

    if not chatroom_edits:
        return {
            "ok": False,
            "step": "find_chatroom_edit",
            "message": "ChatRoomListView 아래 Edit를 찾지 못했습니다.",
            "inspect": search_info,
        }

    search_edit = chatroom_edits[0]

    open_result = open_chatroom_by_search(
        main_hwnd=main_hwnd,
        search_edit=search_edit,
        target=target,
        wait_sec=2.0,
    )

    if not open_result["ok"]:
        return {
            "ok": False,
            "step": open_result["step"],
            "message": open_result["message"],
            "target": target,
            "text": message,
            "main_hwnd": main_hwnd,
            "chatroom_view": chatroom_view,
            "chatroom_edits": chatroom_edits,
            "selected_search_edit": search_edit,
            "input_ok": open_result.get("input_ok"),
            "fg_ok": open_result.get("fg_ok"),
            "focus_ok": open_result.get("focus_ok"),
            "enter_ok": open_result.get("enter_ok"),
            "second_try": open_result.get("second_try"),
            "chat_hwnd": open_result.get("chat_hwnd"),
        }

    chat_hwnd = open_result["chat_hwnd"]
    chat_input_info = inspect_chatroom_input_controls(chat_hwnd)
    input_hwnd = choose_chat_input_hwnd(chat_input_info)

    if not input_hwnd:
        return {
            "ok": False,
            "step": "choose_chat_input_hwnd",
            "message": "채팅 입력창 후보를 찾지 못했습니다.",
            "target": target,
            "text": message,
            "chat_hwnd": chat_hwnd,
            "chat_children": chat_input_info["children"],
            "chat_edit_candidates": chat_input_info["edit_candidates"],
            "chat_richedit_candidates": chat_input_info["richedit_candidates"],
        }

    send_result = send_chat_text(chat_hwnd, input_hwnd, message)

    return {
        "ok": send_result["ok"],
        "step": send_result["step"],
        "message": send_result["message"],
        "target": target,
        "text": message,
        "main_hwnd": main_hwnd,
        "chatroom_view": chatroom_view,
        "chatroom_edits": chatroom_edits,
        "selected_search_edit": search_edit,
        "input_ok": open_result.get("input_ok"),
        "fg_ok": open_result.get("fg_ok"),
        "focus_ok": open_result.get("focus_ok"),
        "search_enter_ok": open_result.get("enter_ok"),
        "second_try": open_result.get("second_try"),
        "chat_hwnd": chat_hwnd,
        "chat_input_hwnd": input_hwnd,
        "chat_edit_candidates": chat_input_info["edit_candidates"],
        "chat_richedit_candidates": chat_input_info["richedit_candidates"],
        "send_fg_ok": send_result.get("fg_ok"),
        "send_focus_ok": send_result.get("focus_ok"),
        "clip_ok": send_result.get("clip_ok"),
        "paste_ok": send_result.get("paste_ok"),
        "send_enter_ok": send_result.get("enter_ok"),
    }