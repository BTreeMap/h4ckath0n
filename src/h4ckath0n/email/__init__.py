"""Email integration – file backend for dev, SMTP for production."""

from h4ckath0n.email.sender import send_email

__all__ = ["send_email"]
