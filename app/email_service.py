import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "colaa222@gmail.com"
EMAIL_PASSWORD = "svcl xlot tpze rdsy"


def send_one_email(to_email: str, subject: str, body: str) -> dict:
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string(),
        )

        server.quit()

        return {
            "ok": True,
            "step": "send_email",
            "message": "이메일 발송 완료",
            "to_email": to_email,
        }

    except Exception as e:
        return {
            "ok": False,
            "step": "send_email",
            "message": str(e),
            "to_email": to_email,
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