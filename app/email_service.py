import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


def send_one_email(to_email: str, subject: str, body: str) -> dict:
    try:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            return {
                "ok": False,
                "step": "env_validate",
                "message": "EMAIL_ADDRESS 또는 EMAIL_PASSWORD 환경변수가 비어 있습니다.",
            }

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        return {
            "ok": True,
            "step": "send_email",
            "message": "이메일 발송 완료",
            "to_email": to_email,
            "subject": subject,
        }

    except Exception as e:
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