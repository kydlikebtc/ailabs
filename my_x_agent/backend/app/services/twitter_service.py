import os
import tweepy
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv

from app.models.tweet import Tweet, UserProfile, TweetSuggestion, TweetAnalysis, TrendingTopic, ReplyOption
from app.utils.ai_service import AIService

load_dotenv()

class TwitterService:
    def __init__(self):
        self.api_key = os.getenv("TWITTER_API_KEY", "")
        self.api_secret = os.getenv("TWITTER_API_SECRET", "")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
        
        self.client = None
        if self.bearer_token:
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )
            
        self.ai_service = AIService()
    
    def authenticate_user(self, auth_token: str, auth_verifier: str) -> dict:
        """
        Authenticate a user with OAuth tokens from X
        """
        return {
            "access_token": "mock_access_token",
            "access_token_secret": "mock_access_token_secret",
            "user_id": "12345",
            "screen_name": "example_user"
        }
    
    def get_user_profile(self, username: str) -> Optional[UserProfile]:
        """
        Get a user's profile information
        """
        if not self.client:
            return UserProfile(
                id="12345",
                username=username,
                display_name=f"{username.capitalize()} User",
                profile_image_url="https://example.com/profile.jpg",
                description="This is a mock user profile for demonstration purposes.",
                followers_count=1000,
                following_count=500
            )
            
        try:
            user = self.client.get_user(
                username=username,
                user_fields=["profile_image_url", "description", "public_metrics"]
            )
            
            if user.data:
                return UserProfile(
                    id=user.data.id,
                    username=user.data.username,
                    display_name=user.data.name,
                    profile_image_url=user.data.profile_image_url,
                    description=user.data.description,
                    followers_count=user.data.public_metrics["followers_count"],
                    following_count=user.data.public_metrics["following_count"]
                )
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def get_user_tweets(self, username: str, count: int = 10) -> List[Tweet]:
        """
        Get a user's recent tweets
        """
        if not self.client:
            mock_tweets = []
            for i in range(count):
                mock_tweets.append(
                    Tweet(
                        id=f"tweet_{i}",
                        text=f"This is a mock tweet #{i} for demonstration purposes. #AI #Tech",
                        created_at=datetime.now(),
                        likes_count=i * 10,
                        retweets_count=i * 5,
                        replies_count=i * 2,
                        author=UserProfile(
                            id="12345",
                            username=username,
                            display_name=f"{username.capitalize()} User"
                        )
                    )
                )
            return mock_tweets
            
        try:
            tweets = self.client.get_users_tweets(
                username=username,
                max_results=count,
                tweet_fields=["created_at", "public_metrics"]
            )
            
            result = []
            if tweets.data:
                user_profile = self.get_user_profile(username)
                for tweet in tweets.data:
                    result.append(
                        Tweet(
                            id=tweet.id,
                            text=tweet.text,
                            created_at=tweet.created_at,
                            likes_count=tweet.public_metrics["like_count"],
                            retweets_count=tweet.public_metrics["retweet_count"],
                            replies_count=tweet.public_metrics["reply_count"],
                            author=user_profile
                        )
                    )
            return result
        except Exception as e:
            print(f"Error getting user tweets: {e}")
            return []
    
    def get_trending_topics(self, location_id: str = "1") -> List[TrendingTopic]:
        """
        Get trending topics, default to worldwide (woeid=1)
        """
        if not self.client:
            mock_trends = [
                TrendingTopic(name="#AI", tweet_volume=52000),
                TrendingTopic(name="#MachineLearning", tweet_volume=35000),
                TrendingTopic(name="#Python", tweet_volume=28000),
                TrendingTopic(name="#Blockchain", tweet_volume=22000),
                TrendingTopic(name="#Crypto", tweet_volume=18000),
            ]
            return mock_trends
            
        try:
            auth = tweepy.OAuth1UserHandler(
                self.api_key, self.api_secret,
                self.access_token, self.access_token_secret
            )
            api = tweepy.API(auth)
            trends = api.get_place_trends(location_id)
            
            result = []
            for trend in trends[0]["trends"]:
                result.append(
                    TrendingTopic(
                        name=trend["name"],
                        tweet_volume=trend["tweet_volume"]
                    )
                )
            return result
        except Exception as e:
            print(f"Error getting trending topics: {e}")
            mock_trends = [
                TrendingTopic(name="#AI", tweet_volume=52000),
                TrendingTopic(name="#MachineLearning", tweet_volume=35000),
                TrendingTopic(name="#Python", tweet_volume=28000),
                TrendingTopic(name="#Blockchain", tweet_volume=22000),
                TrendingTopic(name="#Crypto", tweet_volume=18000),
            ]
            return mock_trends
            
    def analyze_tweet(self, tweet_text: str) -> TweetAnalysis:
        """
        Analyze a tweet for sentiment, topics, and engagement potential
        """
        sentiment = self.ai_service.analyze_tweet_sentiment(tweet_text)
        topics = self.ai_service.extract_topics(tweet_text)
        engagement_score, engagement_reason = self.ai_service.estimate_engagement(tweet_text)
        risk_level, risk_reason = self.ai_service.assess_risk(tweet_text)
        
        return TweetAnalysis(
            sentiment=sentiment,
            topics=topics,
            engagement_estimate=engagement_score,
            engagement_reason=engagement_reason,
            risk_level=risk_level,
            risk_reason=risk_reason
        )
    
    def generate_tweet_suggestions(self, username: str, count: int = 3, topics: Optional[List[str]] = None) -> List[TweetSuggestion]:
        """
        Generate tweet suggestions based on user's previous tweets and optionally specific topics
        """
        user_tweets = self.get_user_tweets(username, count=10)
        tweet_texts = [tweet.text for tweet in user_tweets]
        
        if not topics:
            trending = self.get_trending_topics()
            trending_topics = [topic.name.strip('#') for topic in trending]
        else:
            trending_topics = topics
        
        suggestions_data = self.ai_service.generate_tweet_suggestions(
            user_tweets=tweet_texts,
            trending_topics=trending_topics,
            count=count
        )
        
        suggestions = []
        for suggestion in suggestions_data:
            suggestions.append(
                TweetSuggestion(
                    text=suggestion["text"],
                    topics=suggestion["topics"],
                    confidence=suggestion["confidence"]
                )
            )
        
        return suggestions
    
    def generate_reply_options(self, tweet_text: str, count: int = 3, is_mention: bool = False, trending_score: float = 0.0) -> List[ReplyOption]:
        """
        Generate reply options for a given tweet
        
        Parameters:
        - tweet_text: The text of the tweet to reply to
        - count: Number of reply options to generate
        - is_mention: Whether this tweet is mentioning the user's account
        - trending_score: If not a mention, the trending score of the tweet (0.0-1.0)
        """
        replies_data = self.ai_service.generate_reply_options(
            tweet_text, 
            count, 
            is_mention, 
            trending_score
        )
        
        replies = []
        for reply in replies_data:
            replies.append(
                ReplyOption(
                    text=reply["text"],
                    stance=reply["stance"],
                    confidence=reply["confidence"],
                    is_for_mention=reply.get("is_for_mention", False),
                    is_for_trending=reply.get("is_for_trending", False)
                )
            )
        
        return replies
