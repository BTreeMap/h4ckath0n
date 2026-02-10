"""Pydantic schemas for auth endpoints."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    device_public_key_jwk: dict | None = None
    device_label: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_public_key_jwk: dict | None = None
    device_label: str | None = None


class DeviceBindingResponse(BaseModel):
    user_id: str
    device_id: str
    role: str


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetConfirmSchema(BaseModel):
    token: str
    new_password: str
    device_public_key_jwk: dict | None = None
    device_label: str | None = None


class MessageResponse(BaseModel):
    message: str
