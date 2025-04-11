from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str = Field(default_factory=lambda: f"user_{int(datetime.now().timestamp())}")
    email: EmailStr
    username: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    suggestions_remaining: int = 5
    
    x_username: Optional[str] = None
    x_access_token: Optional[str] = None
    x_access_token_secret: Optional[str] = None
    
    telegram_username: Optional[str] = None
    telegram_access_token: Optional[str] = None
    
    whatsapp_phone: Optional[str] = None
    whatsapp_access_token: Optional[str] = None
    
    signal_phone: Optional[str] = None
    signal_access_token: Optional[str] = None
    
    reachme_username: Optional[str] = None
    reachme_access_token: Optional[str] = None
    
    wallet_address: Optional[str] = None
    last_payment_txid: Optional[str] = None

class User(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime
    subscription_tier: SubscriptionTier
    suggestions_remaining: int
    x_username: Optional[str] = None
    telegram_username: Optional[str] = None
    whatsapp_phone: Optional[str] = None
    signal_phone: Optional[str] = None
    reachme_username: Optional[str] = None
    wallet_address: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
