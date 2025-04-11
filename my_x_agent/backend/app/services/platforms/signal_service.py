import os
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime

from app.models.platforms.base import PlatformMessage, PlatformReply
from app.models.platforms.signal import SignalMessage, SignalReply, SignalUser
from .base_service import BasePlatformService

load_dotenv()

class SignalService(BasePlatformService):
    def __init__(self):
        self.api_token = os.getenv("SIGNAL_API_TOKEN", "")
        
    async def get_messages(self, user_id: str, count: int = 10) -> List[PlatformMessage]:
        """获取Signal消息"""
        messages = []
        for i in range(count):
            messages.append(
                SignalMessage(
                    id=f"signal_msg_{i}",
                    text=f"这是一条来自Signal的示例消息 #{i}",
                    created_at=datetime.now(),
                    platform="signal",
                    source_id=f"phone_{i}",
                    source_user_id="signal_user_1",
                    source_username="signal_user",
                    phone_number="+1234567890",
                    is_group=False
                )
            )
        return messages
        
    async def send_reply(self, message_id: str, text: str) -> PlatformReply:
        """发送Signal回复"""
        return SignalReply(
            id=f"signal_reply_{int(datetime.now().timestamp())}",
            text=text,
            created_at=datetime.now(),
            platform="signal",
            original_message_id=message_id,
            phone_number="+1234567890"
        )
        
    async def connect_account(self, user_id: str, credentials: dict) -> bool:
        """连接Signal账户"""
        return True
