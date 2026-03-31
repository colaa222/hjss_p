# hjss_p

윈도우 환경에서 카카오톡 PC를 자동화해 메시지를 보내는 내부용 테스트 프로젝트입니다.

현재 리포에는 실행 방식이 두 가지 있습니다.

- 웹 방식: FastAPI + HTML 화면에서 1건 발송
- 로컬 방식: 엑셀 파일을 읽어 여러 건 발송

## 전제 조건

- Windows 환경
- Python 3.11 이상 권장
- 카카오톡 PC가 설치되어 있고 로그인된 상태
- 발송 대상 채팅방을 카카오톡에서 검색 가능한 상태

## 설치

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install openpyxl
```

`requirements.txt`에는 웹 실행에 필요한 패키지가 들어 있습니다.  
로컬 엑셀 방식은 `openpyxl`을 추가로 사용하므로 별도 설치가 필요합니다.

## 웹 방식 실행

웹 방식은 브라우저에서 대상 이름과 메시지를 입력해 1건 발송하는 흐름입니다.

```powershell
uvicorn main:app --reload
```

실행 후 브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000
```

사용 순서:

1. 카카오톡 PC를 실행하고 로그인합니다.
2. 위 명령으로 FastAPI 서버를 실행합니다.
3. 브라우저에서 `http://127.0.0.1:8000`에 접속합니다.
4. 대상 이름과 메시지를 입력합니다.
5. 전송 버튼을 눌러 결과 JSON을 확인합니다.

## 로컬 방식 실행

로컬 방식은 엑셀 파일을 읽어서 여러 건을 순차 발송하는 흐름입니다.

실행 스크립트:

```powershell
python scripts\test_excel_send.py
```

기본 입력 파일은 루트의 `sample.xlsx`입니다.

엑셀 컬럼 규칙:

- A열: 대상 이름
- B열: 메시지
- C열: 발송 성공 여부가 기록됨 (`1` 또는 `0`)
- D열: 상세 결과 메시지가 기록됨

사용 순서:

1. 카카오톡 PC를 실행하고 로그인합니다.
2. `sample.xlsx`의 A열과 B열에 대상 이름과 메시지를 입력합니다.
3. 위 스크립트를 실행합니다.
4. 실행이 끝나면 같은 엑셀 파일의 C열, D열에서 결과를 확인합니다.

## 주요 파일

- `main.py`: 웹 서버 엔트리
- `templates/index.html`: 웹 입력 화면
- `app/kakao_win.py`: 카카오톡 윈도우 자동화 로직
- `app/excel_service.py`: 엑셀 읽기/쓰기
- `app/sender.py`: 다건 발송 처리
- `scripts/test_excel_send.py`: 로컬 배치 실행 스크립트

## 주의

- 이 프로젝트는 `pywin32` 기반이라 사실상 Windows 전용입니다.
- 카카오톡 UI 구조 변경에 따라 자동화가 깨질 수 있습니다.
- 웹 방식이든 로컬 방식이든 실제 발송은 로컬 PC의 카카오톡 앱을 조작하는 방식입니다.
