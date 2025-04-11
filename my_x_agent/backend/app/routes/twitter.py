from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional
from app.services.twitter_service import TwitterService
from app.models.tweet import Tweet, UserProfile, TweetSuggestion, TweetAnalysis, TrendingTopic, ReplyOption

router = APIRouter(prefix="/api/twitter", tags=["twitter"])
twitter_service = TwitterService()

@router.get("/auth/callback")
async def twitter_auth_callback(oauth_token: str, oauth_verifier: str):
    """
    Handle Twitter OAuth callback
    """
    try:
        auth_result = twitter_service.authenticate_user(oauth_token, oauth_verifier)
        return auth_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/user/{username}", response_model=UserProfile)
async def get_user_profile(username: str):
    """
    Get a user's profile information
    """
    profile = twitter_service.get_user_profile(username)
    if not profile:
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    return profile

@router.get("/user/{username}/tweets", response_model=List[Tweet])
async def get_user_tweets(username: str, count: int = Query(10, ge=1, le=100)):
    """
    Get a user's recent tweets
    """
    tweets = twitter_service.get_user_tweets(username, count)
    return tweets

@router.get("/trending", response_model=List[TrendingTopic])
async def get_trending_topics(location_id: str = "1"):
    """
    Get trending topics, default to worldwide (woeid=1)
    """
    trends = twitter_service.get_trending_topics(location_id)
    return trends

@router.post("/suggest", response_model=List[TweetSuggestion])
async def generate_tweet_suggestions(
    username: str, 
    count: int = Query(3, ge=1, le=10),
    topics: Optional[List[str]] = None
):
    """
    Generate tweet suggestions based on user's previous tweets and optionally specific topics
    """
    return twitter_service.generate_tweet_suggestions(username, count, topics)

@router.post("/analyze", response_model=TweetAnalysis)
async def analyze_tweet(tweet_text: str = Body(..., embed=True)):
    """
    Analyze a tweet for sentiment, topics, and engagement potential
    """
    return twitter_service.analyze_tweet(tweet_text)

@router.post("/reply-options", response_model=List[ReplyOption])
async def generate_reply_options(
    tweet_id: str,
    tweet_text: str,
    count: int = Query(3, ge=1, le=5)
):
    """
    Generate reply options for a given tweet
    """
    return twitter_service.generate_reply_options(tweet_text, count)
