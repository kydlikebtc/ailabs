import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from app.models.user import UserInDB, User, TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.users_db = {}
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Hash a password
        """
        return pwd_context.hash(password)
    
    def get_user(self, email: str) -> Optional[UserInDB]:
        """
        Get a user by email
        """
        if email in self.users_db:
            return UserInDB(**self.users_db[email])
        return None
    
    def create_user(self, email: str, username: str, password: str) -> UserInDB:
        """
        Create a new user
        """
        if email in self.users_db:
            raise ValueError("Email already registered")
        
        hashed_password = self.get_password_hash(password)
        user_data = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "subscription_tier": "free",
            "suggestions_remaining": 5
        }
        
        user = UserInDB(**user_data)
        self.users_db[email] = user.dict()
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """
        Authenticate a user
        """
        user = self.get_user(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_current_user(self, token: str) -> Optional[User]:
        """
        Get the current user from a JWT token
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            
            if email is None:
                return None
                
            token_data = TokenData(email=email, user_id=user_id)
        except JWTError:
            return None
            
        user = self.get_user(token_data.email)
        if user is None:
            return None
            
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
    
    def update_user_subscription(self, email: str, tier: str) -> Optional[User]:
        """
        Update a user's subscription tier
        """
        user = self.get_user(email)
        if not user:
            return None
            
        user_dict = self.users_db[email]
        user_dict["subscription_tier"] = tier
        user_dict["updated_at"] = datetime.now()
        
        if tier == "pro":
            user_dict["suggestions_remaining"] = 999999
        
        self.users_db[email] = user_dict
        updated_user = UserInDB(**user_dict)
        
        return User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            subscription_tier=updated_user.subscription_tier,
            suggestions_remaining=updated_user.suggestions_remaining,
            x_username=updated_user.x_username
        )
    
    def update_suggestions_remaining(self, email: str, count: int) -> Optional[User]:
        """
        Update a user's remaining suggestions count
        """
        user = self.get_user(email)
        if not user:
            return None
            
        user_dict = self.users_db[email]
        user_dict["suggestions_remaining"] = count
        user_dict["updated_at"] = datetime.now()
        
        self.users_db[email] = user_dict
        updated_user = UserInDB(**user_dict)
        
        return User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            subscription_tier=updated_user.subscription_tier,
            suggestions_remaining=updated_user.suggestions_remaining,
            x_username=updated_user.x_username
        )
    
    def connect_x_account(self, email: str, x_username: str, access_token: str, access_token_secret: str) -> Optional[User]:
        """
        Connect a user's X account
        """
        user = self.get_user(email)
        if not user:
            return None
            
        user_dict = self.users_db[email]
        user_dict["x_username"] = x_username
        user_dict["x_access_token"] = access_token
        user_dict["x_access_token_secret"] = access_token_secret
        user_dict["updated_at"] = datetime.now()
        
        self.users_db[email] = user_dict
        updated_user = UserInDB(**user_dict)
        
        return User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            subscription_tier=updated_user.subscription_tier,
            suggestions_remaining=updated_user.suggestions_remaining,
            x_username=updated_user.x_username
        )
        
    def add_suggestions_to_user(self, email: str, quantity: int) -> Optional[User]:
        """
        增加用户可用的推文建议数量
        """
        user = self.get_user(email)
        if not user:
            return None
            
        user_dict = self.users_db[email]
        current_suggestions = user_dict.get("suggestions_remaining", 0)
        user_dict["suggestions_remaining"] = current_suggestions + quantity
        user_dict["updated_at"] = datetime.now()
        
        self.users_db[email] = user_dict
        updated_user = UserInDB(**user_dict)
        
        return User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            subscription_tier=updated_user.subscription_tier,
            suggestions_remaining=updated_user.suggestions_remaining,
            x_username=updated_user.x_username
        )
        
    def update_user_wallet(self, email: str, tx_hash: str) -> Optional[User]:
        """
        更新用户钱包信息
        """
        user = self.get_user(email)
        if not user:
            return None
            
        user_dict = self.users_db[email]
        user_dict["last_payment_txid"] = tx_hash
        user_dict["updated_at"] = datetime.now()
        
        self.users_db[email] = user_dict
        updated_user = UserInDB(**user_dict)
        
        return User(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            subscription_tier=updated_user.subscription_tier,
            suggestions_remaining=updated_user.suggestions_remaining,
            x_username=updated_user.x_username,
            wallet_address=updated_user.wallet_address
        )
