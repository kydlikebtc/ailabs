from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.platforms.base import PlatformMessage, PlatformReply

class BasePlatformService(ABC):
    @abstractmethod
    async def get_messages(self, user_id: str, count: int = 10) -> List[PlatformMessage]:
        """获取消息"""
        pass
        
    @abstractmethod
    async def send_reply(self, message_id: str, text: str) -> PlatformReply:
        """发送回复"""
        pass
        
    @abstractmethod
    async def connect_account(self, user_id: str, credentials: dict) -> bool:
        """连接账户"""
        pass
