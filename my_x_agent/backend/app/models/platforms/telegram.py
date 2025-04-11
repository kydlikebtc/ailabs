from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import PlatformMessage, PlatformReply, PlatformUser

class TelegramMessage(PlatformMessage):
    chat_id: str
    is_group: bool = False
    
class TelegramReply(PlatformReply):
    chat_id: str
    
class TelegramUser(PlatformUser):
    chat_id: str
