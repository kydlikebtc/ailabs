import os
from typing import Dict, List, Optional
from datetime import datetime
from web3 import Web3
from dotenv import load_dotenv
import uuid

load_dotenv()

class PaymentService:
    def __init__(self):
        self.bnb_rpc_url = os.getenv("BNB_RPC_URL", "https://bsc-dataseed.binance.org/")
        self.contract_address = os.getenv("CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
        self.web3 = Web3(Web3.HTTPProvider(self.bnb_rpc_url))
        self.transactions = {}  # 模拟存储
        
    def generate_payment_request(self, user_id: str, amount: float, item_type: str) -> Dict:
        """生成支付请求"""
        tx_id = f"tx_{user_id}_{int(datetime.now().timestamp())}"
        
        payment_data = {
            "id": tx_id,
            "user_id": user_id,
            "amount": amount,
            "item_type": item_type,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "payment_address": self.contract_address,
        }
        
        self.transactions[tx_id] = payment_data
        return payment_data
    
    def verify_payment(self, tx_id: str, tx_hash: str) -> Dict:
        """验证支付"""
        if tx_id not in self.transactions:
            return {"status": "failed", "message": "Transaction not found"}
        
        try:
            
            self.transactions[tx_id]["status"] = "completed"
            self.transactions[tx_id]["tx_hash"] = tx_hash
            
            return {
                "status": "completed",
                "tx_id": tx_id,
                "tx_hash": tx_hash
            }
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def get_payment_status(self, tx_id: str) -> Dict:
        """获取支付状态"""
        if tx_id not in self.transactions:
            return {"status": "failed", "message": "Transaction not found"}
        
        return {
            "status": self.transactions[tx_id]["status"],
            "tx_id": tx_id,
            "created_at": self.transactions[tx_id]["created_at"],
            "amount": self.transactions[tx_id]["amount"],
            "item_type": self.transactions[tx_id]["item_type"]
        }
    
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        """获取用户交易历史"""
        user_txs = []
        for tx_id, tx_data in self.transactions.items():
            if tx_data["user_id"] == user_id:
                user_txs.append(tx_data)
        
        return user_txs
    
    def calculate_price(self, item_type: str, quantity: int = 1) -> float:
        """计算价格"""
        if item_type == "tweet_suggestion":
            return 0.015 * quantity  # 0.015 BNB per suggestion
        else:
            return 0.0
