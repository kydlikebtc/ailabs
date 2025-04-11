from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlatformMessage(BaseModel):
    id: str
    text: str
    created_at: datetime
    platform: str
    source_id: str
    source_user_id: str
    source_username: str
    
class PlatformReply(BaseModel):
    id: str
    text: str
    created_at: datetime
    platform: str
    original_message_id: str
    
class PlatformUser(BaseModel):
    id: str
    username: str
    platform: str
    display_name: Optional[str] = None
    profile_url: Optional[str] = None
