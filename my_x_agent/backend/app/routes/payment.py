from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, List, Optional
from app.models.user import User
from app.routes.auth import get_current_user
from app.services.payment_service import PaymentService
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/payment",
    tags=["payment"],
)

@router.post("/request")
async def create_payment_request(
    item_type: str = Body(...),
    quantity: int = Body(1),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """创建BNB支付请求"""
    payment_service = PaymentService()
    
    if item_type == "tweet_suggestion":
        amount = payment_service.calculate_price(item_type, quantity)
    else:
        raise HTTPException(status_code=400, detail="不支持的商品类型")
    
    payment_request = payment_service.generate_payment_request(
        current_user.id,
        amount,
        item_type
    )
    
    return payment_request

@router.post("/verify")
async def verify_payment(
    tx_id: str = Body(...),
    tx_hash: str = Body(...),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """验证BNB支付"""
    payment_service = PaymentService()
    auth_service = AuthService()
    
    verification = payment_service.verify_payment(tx_id, tx_hash)
    
    if verification["status"] == "completed":
        payment_data = payment_service.get_payment_status(tx_id)
        
        if payment_data["item_type"] == "tweet_suggestion":
            quantity = int(payment_data["amount"] / 0.015)  # 每条0.015 BNB
            auth_service.add_suggestions_to_user(current_user.email, quantity)
            auth_service.update_user_wallet(current_user.email, tx_hash)
    
    return verification

@router.get("/status/{tx_id}")
async def get_payment_status(
    tx_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """获取支付状态"""
    payment_service = PaymentService()
    return payment_service.get_payment_status(tx_id)

@router.get("/history")
async def get_payment_history(
    current_user: User = Depends(get_current_user)
) -> List[Dict]:
    """获取支付历史"""
    payment_service = PaymentService()
    return payment_service.get_user_transactions(current_user.id)
