from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import PlatformMessage, PlatformReply, PlatformUser

class WhatsAppMessage(PlatformMessage):
    phone_number: str
    is_group: bool = False
    group_id: Optional[str] = None
    
class WhatsAppReply(PlatformReply):
    phone_number: str
    
class WhatsAppUser(PlatformUser):
    phone_number: str
