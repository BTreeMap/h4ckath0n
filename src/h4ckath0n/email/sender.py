"""Email sending abstraction."""

from __future__ import annotations

import asyncio
import logging
import os
import smtplib
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


async def send_email(
    *,
    to: str,
    subject: str,
    body_text: str,
    body_html: str | None = None,
    backend: str = "file",
    email_from: str = "noreply@localhost",
    outbox_dir: str = "./.h4ckath0n_email_outbox",
    smtp_host: str = "",
    smtp_port: int = 587,
    smtp_username: str = "",
    smtp_password: str = "",
    smtp_starttls: bool = True,
    smtp_ssl: bool = False,
) -> None:
    """Send an email using the configured backend."""
    if backend == "file":
        await _send_file(
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            email_from=email_from,
            outbox_dir=outbox_dir,
        )
    elif backend == "smtp":
        await _send_smtp(
            to=to,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            email_from=email_from,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password=smtp_password,
            smtp_starttls=smtp_starttls,
            smtp_ssl=smtp_ssl,
        )
    else:
        raise ValueError(f"Unknown email backend: {backend}")


async def _send_file(
    *,
    to: str,
    subject: str,
    body_text: str,
    body_html: str | None,
    email_from: str,
    outbox_dir: str,
) -> None:
    """Write email to a file in the outbox directory."""
    os.makedirs(outbox_dir, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S_%f")
    safe_to = to.replace("@", "_at_").replace(".", "_")[:50]
    filename = f"{timestamp}_{safe_to}.eml"
    filepath = os.path.join(outbox_dir, filename)

    content = f"""From: {email_from}
To: {to}
Subject: {subject}
Date: {datetime.now(UTC).isoformat()}
Content-Type: text/plain; charset=utf-8

{body_text}
"""
    if body_html:
        content += f"\n---HTML VERSION---\n{body_html}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("Email written to %s", filepath)


async def _send_smtp(
    *,
    to: str,
    subject: str,
    body_text: str,
    body_html: str | None,
    email_from: str,
    smtp_host: str,
    smtp_port: int,
    smtp_username: str,
    smtp_password: str,
    smtp_starttls: bool,
    smtp_ssl: bool,
) -> None:
    """Send email via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = email_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body_text, "plain"))
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    def _do_send() -> None:
        server: smtplib.SMTP
        if smtp_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
        try:
            if smtp_starttls and not smtp_ssl:
                server.starttls()
            if smtp_username:
                server.login(smtp_username, smtp_password)
            server.sendmail(email_from, [to], msg.as_string())
        finally:
            server.quit()

    await asyncio.to_thread(_do_send)
    logger.info("Email sent via SMTP to %s", to)
