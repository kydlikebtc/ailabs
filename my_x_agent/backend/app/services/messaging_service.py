from typing import List, Dict, Optional
from app.services.platforms.telegram_service import TelegramService
from app.services.platforms.whatsapp_service import WhatsAppService
from app.services.platforms.signal_service import SignalService
from app.services.platforms.reachme_service import ReachmeService
from app.models.platforms.base import PlatformMessage, PlatformReply

class MessagingService:
    def __init__(self):
        self.services = {
            "telegram": TelegramService(),
            "whatsapp": WhatsAppService(),
            "signal": SignalService(),
            "reachme": ReachmeService()
        }
        
    async def get_messages_from_all_platforms(self, user_id: str, count_per_platform: int = 5) -> Dict[str, List[PlatformMessage]]:
        """获取所有平台的消息"""
        result = {}
        for platform, service in self.services.items():
            result[platform] = await service.get_messages(user_id, count_per_platform)
        return result
        
    async def send_reply(self, platform: str, message_id: str, text: str) -> Optional[PlatformReply]:
        """发送特定平台的回复"""
        if platform not in self.services:
            return None
        return await self.services[platform].send_reply(message_id, text)
        
    async def connect_platform_account(self, platform: str, user_id: str, credentials: dict) -> bool:
        """连接特定平台账户"""
        if platform not in self.services:
            return False
        return await self.services[platform].connect_account(user_id, credentials)
