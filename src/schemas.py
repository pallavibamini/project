"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# Product schemas
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    sku: Optional[str] = Field(None, max_length=100)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    sku: Optional[str] = Field(None, max_length=100)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    sku: Optional[str]

    class Config:
        from_attributes = True


# Order Item schemas
class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


# Order schemas
class OrderCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    items: List[OrderItemCreate] = Field(..., min_items=1)
    status: Optional[str] = Field("pending", max_length=50)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
