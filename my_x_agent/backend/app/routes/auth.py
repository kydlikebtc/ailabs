from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from app.models.user import User, UserCreate, Token
from app.services.auth_service import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the token
    """
    user = auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    """
    Register a new user
    """
    try:
        user = auth_service.create_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )
        return User(
            id=user.id,
            email=user.email,
            username=user.username,
            created_at=user.created_at,
            updated_at=user.updated_at,
            subscription_tier=user.subscription_tier,
            suggestions_remaining=user.suggestions_remaining,
            x_username=user.x_username
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token for a user
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current user's information
    """
    return current_user

@router.post("/connect-x", response_model=User)
async def connect_x_account(
    x_username: str,
    access_token: str,
    access_token_secret: str,
    current_user: User = Depends(get_current_user)
):
    """
    Connect a user's X account
    """
    updated_user = auth_service.connect_x_account(
        email=current_user.email,
        x_username=x_username,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user

@router.post("/subscription", response_model=User)
async def update_subscription(
    tier: str,
    current_user: User = Depends(get_current_user)
):
    """
    Update a user's subscription tier
    """
    if tier not in ["free", "pro"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subscription tier"
        )
    
    updated_user = auth_service.update_user_subscription(
        email=current_user.email,
        tier=tier
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user
