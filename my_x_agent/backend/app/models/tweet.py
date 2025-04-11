from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    username: str
    display_name: str
    profile_image_url: Optional[str] = None
    description: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0

class Tweet(BaseModel):
    id: str
    text: str
    created_at: datetime
    likes_count: int = 0
    retweets_count: int = 0
    replies_count: int = 0
    author: UserProfile
    
class TweetSuggestion(BaseModel):
    id: str = Field(default_factory=lambda: f"suggestion_{int(datetime.now().timestamp())}")
    text: str
    topics: List[str] = []
    confidence: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)

class TweetAnalysis(BaseModel):
    sentiment: str  # positive, negative, neutral
    topics: List[str] = []
    engagement_estimate: float = 0.0
    engagement_reason: str = ""
    risk_level: str = "low"  # low, medium, high
    risk_reason: str = ""

class ReplyOption(BaseModel):
    id: str = Field(default_factory=lambda: f"reply_{int(datetime.now().timestamp())}")
    text: str
    stance: str  # supportive, against, neutral
    confidence: float = 0.0
    is_for_mention: bool = False
    is_for_trending: bool = False

class TrendingTopic(BaseModel):
    name: str
    tweet_volume: Optional[int] = None
    location: Optional[str] = None
