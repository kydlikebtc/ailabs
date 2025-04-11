import os
from typing import List, Optional
from dotenv import load_dotenv
from datetime import datetime

from app.models.platforms.base import PlatformMessage, PlatformReply
from app.models.platforms.reachme import ReachmeMessage, ReachmeReply, ReachmeUser
from .base_service import BasePlatformService

load_dotenv()

class ReachmeService(BasePlatformService):
    def __init__(self):
        self.api_token = os.getenv("REACHME_API_TOKEN", "")
        
    async def get_messages(self, user_id: str, count: int = 10) -> List[PlatformMessage]:
        """获取Reachme.io消息"""
        messages = []
        for i in range(count):
            messages.append(
                ReachmeMessage(
                    id=f"reachme_msg_{i}",
                    text=f"这是一条来自Reachme.io的示例消息 #{i}",
                    created_at=datetime.now(),
                    platform="reachme",
                    source_id=f"channel_{i}",
                    source_user_id="reachme_user_1",
                    source_username="reachme_user",
                    channel_id=f"channel_{i}",
                    is_group=False
                )
            )
        return messages
        
    async def send_reply(self, message_id: str, text: str) -> PlatformReply:
        """发送Reachme.io回复"""
        return ReachmeReply(
            id=f"reachme_reply_{int(datetime.now().timestamp())}",
            text=text,
            created_at=datetime.now(),
            platform="reachme",
            original_message_id=message_id,
            channel_id=f"channel_1"
        )
        
    async def connect_account(self, user_id: str, credentials: dict) -> bool:
        """连接Reachme.io账户"""
        return True
