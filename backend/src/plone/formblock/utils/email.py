from email import policy
from email.message import EmailMessage

import codecs
import os


CTE = os.environ.get("MAIL_CONTENT_TRANSFER_ENCODING", None)


def add_attachaments_to_msg(
    msg: EmailMessage, attachments: dict[str, dict | str]
) -> None:
    for value in attachments.values():
        content_type = "application/octet-stream"
        filename = None
        if isinstance(value, dict):
            file_data = value.get("data", "")
            if not file_data:
                continue
            content_type = value.get("content-type", content_type)
            filename = value.get("filename", filename)
            if isinstance(file_data, str):
                file_data = file_data.encode("utf-8")
            if "encoding" in value:
                file_data = codecs.decode(file_data, value["encoding"])
            if isinstance(file_data, str):
                file_data = file_data.encode("utf-8")
        else:
            file_data = value
        maintype, subtype = content_type.split("/")
        msg.add_attachment(
            file_data,
            maintype=maintype,
            subtype=subtype,
            filename=filename,
        )


def create_message(
    mfrom: str,
    mto: str,
    subject: str,
    body: str,
    body_txt: str,
    reply_to: str = "",
    bcc: str = "",
    headers: dict | None = None,
    attachments: dict[str, dict | str] | None = None,
) -> EmailMessage:
    msg = EmailMessage(policy=policy.SMTP)
    msg.set_content(body_txt, cte=CTE)
    msg.add_alternative(body, subtype="html", cte=CTE)
    msg["Subject"] = subject
    msg["From"] = mfrom
    msg["Reply-To"] = reply_to or mfrom
    msg["To"] = mto.replace(";", ",")
    if bcc:
        msg["Bcc"] = bcc.replace(";", ",")

    headers = headers or {}
    for header, value in headers.items():
        if value:
            msg[header] = value
    attachments = attachments or {}
    add_attachaments_to_msg(msg=msg, attachments=attachments)
    return msg
