from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.models.tweet import Tweet, TweetSuggestion, TweetAnalysis, ReplyOption
from app.services.twitter_service import TwitterService
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/twitter",
    tags=["twitter"],
)

@router.post("/analyze", response_model=TweetAnalysis)
async def analyze_tweet(
    text: str,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a tweet for sentiment, topics, engagement potential, and risk level
    """
    twitter_service = TwitterService()
    analysis = twitter_service.analyze_tweet(text)
    return analysis

@router.post("/reply-options", response_model=List[ReplyOption])
async def generate_reply_options(
    text: str,
    count: int = 3,
    is_mention: bool = False,
    trending_score: float = 0.0,
    current_user: User = Depends(get_current_user)
):
    """
    Generate reply options for a given tweet
    
    Parameters:
    - text: The tweet text to generate replies for
    - count: Number of reply options to generate
    - is_mention: Whether this tweet is mentioning the user's account
    - trending_score: If not a mention, the trending score of the tweet (0.0-1.0)
    """
    twitter_service = TwitterService()
    reply_options = twitter_service.generate_reply_options(
        text, 
        count, 
        is_mention, 
        trending_score
    )
    return reply_options

@router.get("/trending", response_model=List[Tweet])
async def get_trending_tweets(
    count: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Get trending tweets
    """
    twitter_service = TwitterService()
    tweets = twitter_service.get_user_tweets("example_user", count)
    return tweets

@router.post("/retweet", response_model=Tweet)
async def retweet_with_comment(
    tweet_id: str,
    text: str,
    current_user: User = Depends(get_current_user)
):
    """
    Retweet with a comment
    """
    twitter_service = TwitterService()
    user_profile = twitter_service.get_user_profile(current_user.username)
    
    mock_tweet = Tweet(
        id=f"retweet_{tweet_id}",
        text=text,
        created_at=datetime.now(),
        likes_count=0,
        retweets_count=0,
        replies_count=0,
        author=user_profile
    )
    
    return mock_tweet

@router.post("/reply", response_model=Tweet)
async def reply_to_tweet(
    tweet_id: str,
    text: str,
    current_user: User = Depends(get_current_user)
):
    """
    Reply to a tweet
    """
    twitter_service = TwitterService()
    user_profile = twitter_service.get_user_profile(current_user.username)
    
    mock_tweet = Tweet(
        id=f"reply_{tweet_id}",
        text=text,
        created_at=datetime.now(),
        likes_count=0,
        retweets_count=0,
        replies_count=0,
        author=user_profile
    )
    
    return mock_tweet
