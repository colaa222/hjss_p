# hjss_p

카카오톡과 이메일을 단건 또는 엑셀 일괄 방식으로 발송하는 내부용 도구입니다.

현재 리포 기준 주요 기능:

- 카카오톡 1건 발송
- 이메일 1건 발송
- 엑셀 기반 일괄 발송
- 실패건 재발송

## 1. 사용 전 준비

### 카카오톡 발송 시

- Windows 환경에서 실행해야 합니다.
- 카카오톡 PC가 켜져 있고 로그인되어 있어야 합니다.
- 가능하면 카카오톡 메인창이 열려 있고 채팅 목록이 보이는 상태에서 시작합니다.
- 발송 중에는 마우스나 키보드를 건드리지 않는 것이 안전합니다.

### 이메일 발송 시

- 현재 리포는 `app/email_service.py`의 SMTP 설정을 사용합니다.
- 이메일 발송이 필요하면 해당 파일의 발신 계정 설정을 먼저 확인해야 합니다.

### 엑셀 발송 시

- 기본 파일은 루트의 `sample.xlsx`입니다.
- 엑셀 파일이 열려 있으면 저장 충돌이 날 수 있으므로 닫아두는 것이 안전합니다.

## 2. 설치

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install openpyxl
pip install python-dotenv
```

설치 목적:

- `requirements.txt`: FastAPI 웹 서버, 템플릿, 카카오톡 자동화
- `openpyxl`: 엑셀 읽기/쓰기

## 3. 사용 방법

### 웹으로 실행

```powershell
uvicorn main:app --reload
```

브라우저 접속:

```text
http://127.0.0.1:8000
```

웹 화면에서 할 수 있는 작업:

- 카카오톡 1건 발송
- 이메일 1건 발송
- 엑셀 전체 발송
- 실패건 재발송

권장 순서:

1. 카카오톡을 채팅 목록 화면으로 맞춥니다.
2. 서버를 실행합니다.
3. 브라우저에서 `http://127.0.0.1:8000`에 접속합니다.
4. 필요한 발송 방식 버튼을 실행합니다.
5. 화면의 요약 결과와 상세 로그를 확인합니다.

### 로컬 스크립트로 실행

```powershell
python scripts\test_excel_send.py
```

이 스크립트는 `sample.xlsx`를 읽어 행별로 발송합니다.  
엑셀의 `channel` 값에 따라 카카오톡 또는 이메일로 분기됩니다.

권장 순서:

1. 카카오톡을 채팅 목록 화면으로 맞춥니다.
2. `sample.xlsx`를 작성합니다.
3. 스크립트를 실행합니다.
4. 발송 후 엑셀의 결과 컬럼을 확인합니다.

## 4. 엑셀 컬럼 사용법

현재 코드 기준 컬럼은 아래 순서입니다.

- `A열 channel`: 발송 채널
- `B열 target`: 카카오톡 채팅방 이름
- `C열 to_email`: 이메일 수신 주소
- `D열 subject`: 이메일 제목
- `E열 message`: 발송 본문
- `F열 send_status`: 발송 결과 상태
- `G열 detail`: 상세 결과 메시지

### channel 값 규칙

- `kakao`: 카카오톡 발송
- `email`: 이메일 발송

### 컬럼별 입력 규칙

- `channel`
  - 반드시 `kakao` 또는 `email` 중 하나를 넣습니다.
- `target`
  - `channel=kakao`일 때 사용합니다.
  - 카카오톡에서 검색 가능한 채팅방 이름을 넣습니다.
- `to_email`
  - `channel=email`일 때 사용합니다.
  - 받는 사람 이메일 주소를 넣습니다.
- `subject`
  - `channel=email`일 때 사용합니다.
  - 메일 제목을 넣습니다.
- `message`
  - 두 채널 모두 사용합니다.
  - 실제 발송할 본문입니다.
- `send_status`
  - 실행 후 코드가 기록합니다.
  - `1`은 성공, `0`은 실패입니다.
- `detail`
  - 실행 후 코드가 기록합니다.
  - 실패 단계와 상세 사유가 들어갑니다.

### 채널별 필수 입력

`channel=kakao`

- `target` 필수
- `message` 필수
- `to_email`, `subject`는 비워도 됩니다.

`channel=email`

- `to_email` 필수
- `subject` 필수
- `message` 필수
- `target`은 비워도 됩니다.

### 예시

| channel | target | to_email | subject | message |
| --- | --- | --- | --- | --- |
| kakao | 임상민 |  |  | 테스트 메시지 |
| email |  | user@example.com | 안내 메일 | 안녕하세요 |

빈 행은 건너뜁니다.  
현재 코드는 2행부터 끝까지 읽고, `channel/target/to_email/subject/message`가 모두 비어 있는 행만 스킵합니다.

## 5. 결과 확인 방법

발송 후 결과는 아래에 기록됩니다.

- `F열(send_status)`: 성공이면 `1`, 실패면 `0`
- `G열(detail)`: 실패 단계와 상세 메시지

웹으로 실행하면 화면에도 아래 정보가 같이 보입니다.

- `request_id`
- `total`
- `success`
- `fail`
- `results`

## 6. 실패건 재발송 방법

웹 화면의 `실패건 재발송` 버튼은 `F열(send_status)`가 `0`인 행만 다시 발송합니다.

재발송 순서:

1. 이전 실행 결과에서 실패한 행의 `F열` 값이 `0`인지 확인합니다.
2. 카카오톡을 다시 채팅 목록 상태로 맞춥니다.
3. 웹 화면에서 `실패건 재발송`을 누릅니다.
4. 결과 요약과 상세 로그를 확인합니다.

## 7. 자주 보는 실패 원인

- 카카오톡이 꺼져 있음
- 카카오톡이 로그인되지 않았음
- 카카오톡이 채팅 목록 상태가 아님
- 카카오 채팅방 이름이 검색되지 않음
- `channel` 값이 `kakao` 또는 `email`이 아님
- `kakao`인데 `target` 또는 `message`가 비어 있음
- `email`인데 `to_email`, `subject`, `message` 중 하나가 비어 있음
- 최근 5초 내 동일 요청이라 중복 발송 방지(`dedup_skip`)가 걸림

## 8. 주요 파일

- `main.py`: FastAPI 엔트리
- `templates/index.html`: 웹 UI
- `app/kakao_win.py`: 카카오톡 자동화
- `app/email_service.py`: 이메일 발송
- `app/excel_service.py`: 엑셀 읽기/쓰기
- `app/sender.py`: 채널 분기, 중복 방지, 다건 발송
- `scripts/test_excel_send.py`: 로컬 일괄 발송 스크립트

## 9. 주의

- 카카오톡 자동화는 사실상 Windows 전용입니다.
- 카카오톡 UI가 바뀌면 자동화가 깨질 수 있습니다.
- 이메일 발송 설정은 현재 코드에 직접 들어 있으므로 운영 전 확인이 필요합니다.
