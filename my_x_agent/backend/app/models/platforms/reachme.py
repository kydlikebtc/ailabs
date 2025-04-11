from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import PlatformMessage, PlatformReply, PlatformUser

class ReachmeMessage(PlatformMessage):
    channel_id: str
    is_group: bool = False
    
class ReachmeReply(PlatformReply):
    channel_id: str
    
class ReachmeUser(PlatformUser):
    channel_id: str
