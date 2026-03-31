import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "colaa222@gmail.com" # Google Email
EMAIL_PASSWORD = "svcl xlot tpze rdsy" # 웹 비밀번호 2차 인증 


def send_one_email(to_email: str, subject: str, body: str) -> dict:
    try:
        print("[EMAIL] start")

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        print("[EMAIL] smtp connect")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        print("[EMAIL] starttls")
        server.starttls()

        print("[EMAIL] login")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        print("[EMAIL] sendmail")
        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string(),
        )

        print("[EMAIL] quit")
        server.quit()

        return {
            "ok": True,
            "step": "send_email",
            "message": "이메일 발송 완료",
            "to_email": to_email,
            "subject": subject,
        }

    except Exception as e:
        print("[EMAIL ERROR]", str(e))
        return {
            "ok": False,
            "step": "send_email",
            "message": str(e),
            "to_email": to_email,
            "subject": subject,
        }

def send_one_email(to_email: str, subject: str, body: str) -> dict:
    try:
        print("[EMAIL] start")

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain", "utf-8"))

        print("[EMAIL] smtp connect")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

        print("[EMAIL] starttls")
        server.starttls()

        print("[EMAIL] login")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        print("[EMAIL] sendmail")
        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string(),
        )

        print("[EMAIL] quit")
        server.quit()

        return {"ok": True}

    except Exception as e:
        print("[EMAIL ERROR]", str(e))
        return {
            "ok": False,
            "message": str(e)
        }