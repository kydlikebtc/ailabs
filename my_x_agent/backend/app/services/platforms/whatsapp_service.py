import os
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime

from app.models.platforms.base import PlatformMessage, PlatformReply
from app.models.platforms.whatsapp import WhatsAppMessage, WhatsAppReply, WhatsAppUser
from .base_service import BasePlatformService

load_dotenv()

class WhatsAppService(BasePlatformService):
    def __init__(self):
        self.api_token = os.getenv("WHATSAPP_API_TOKEN", "")
        
    async def get_messages(self, user_id: str, count: int = 10) -> List[PlatformMessage]:
        """获取WhatsApp消息"""
        messages = []
        for i in range(count):
            messages.append(
                WhatsAppMessage(
                    id=f"whatsapp_msg_{i}",
                    text=f"这是一条来自WhatsApp的示例消息 #{i}",
                    created_at=datetime.now(),
                    platform="whatsapp",
                    source_id=f"phone_{i}",
                    source_user_id="whatsapp_user_1",
                    source_username="whatsapp_user",
                    phone_number="+1234567890",
                    is_group=False
                )
            )
        return messages
        
    async def send_reply(self, message_id: str, text: str) -> PlatformReply:
        """发送WhatsApp回复"""
        return WhatsAppReply(
            id=f"whatsapp_reply_{int(datetime.now().timestamp())}",
            text=text,
            created_at=datetime.now(),
            platform="whatsapp",
            original_message_id=message_id,
            phone_number="+1234567890"
        )
        
    async def connect_account(self, user_id: str, credentials: dict) -> bool:
        """连接WhatsApp账户"""
        return True
