from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import PlatformMessage, PlatformReply, PlatformUser

class SignalMessage(PlatformMessage):
    phone_number: str
    is_group: bool = False
    group_id: Optional[str] = None
    
class SignalReply(PlatformReply):
    phone_number: str
    
class SignalUser(PlatformUser):
    phone_number: str
