import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """
    Service for AI-powered text generation and analysis
    In a production environment, this would integrate with DeepSeek or GPT-4o
    """
    
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY", "")
        self.model = os.getenv("AI_MODEL", "gpt-4o")
    
    def analyze_tweet_sentiment(self, tweet_text: str) -> str:
        """
        Analyze the sentiment of a tweet
        Returns: "positive", "negative", or "neutral"
        """
        positive_words = ["good", "great", "excellent", "amazing", "love", "happy", "excited"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "disappointed"]
        
        tweet_lower = tweet_text.lower()
        positive_count = sum(1 for word in positive_words if word in tweet_lower)
        negative_count = sum(1 for word in negative_words if word in tweet_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def extract_topics(self, tweet_text: str) -> List[str]:
        """
        Extract topics from a tweet
        """
        hashtags = [word.strip('#') for word in tweet_text.split() if word.startswith('#')]
        
        if not hashtags:
            tech_keywords = ["ai", "tech", "technology", "code", "programming", "software", "data"]
            crypto_keywords = ["crypto", "bitcoin", "ethereum", "blockchain", "web3", "nft"]
            
            tweet_lower = tweet_text.lower()
            topics = []
            
            if any(keyword in tweet_lower for keyword in tech_keywords):
                topics.append("Technology")
            if any(keyword in tweet_lower for keyword in crypto_keywords):
                topics.append("Crypto")
            
            if not topics:
                topics.append("General")
                
            return topics
        
        return hashtags
    
    def estimate_engagement(self, tweet_text: str) -> tuple:
        """
        Estimate the engagement potential of a tweet
        Returns: (engagement_score, reason)
        """
        
        score = 0.5  # Default score
        reasons = []
        
        if 80 <= len(tweet_text) <= 200:
            score += 0.1
            reasons.append("Optimal length")
        
        hashtags = [word for word in tweet_text.split() if word.startswith('#')]
        if 1 <= len(hashtags) <= 3:
            score += 0.1
            reasons.append("Good hashtag usage")
        elif len(hashtags) > 3:
            score -= 0.05
            reasons.append("Too many hashtags")
        
        if '?' in tweet_text:
            score += 0.05
            reasons.append("Contains a question")
        
        if 'http' in tweet_text:
            score += 0.05
            reasons.append("Contains a link")
        
        emojis = ['😀', '👍', '🔥', '❤️', '😂', '🚀', '💯']
        if any(emoji in tweet_text for emoji in emojis):
            score += 0.05
            reasons.append("Contains emojis")
        
        score = min(score, 0.95)
        
        reason = "Based on " + ", ".join(reasons) if reasons else "Average engagement expected"
        
        return (score, reason)
    
    def assess_risk(self, tweet_text: str) -> tuple:
        """
        Assess the risk level of a tweet
        Returns: (risk_level, reason)
        """
        
        risk_level = "low"
        reasons = []
        
        sensitive_words = [
            "controversial", "scandal", "fired", "lawsuit", "politics", 
            "religion", "offensive", "attack", "hate", "angry"
        ]
        
        tweet_lower = tweet_text.lower()
        found_sensitive = [word for word in sensitive_words if word in tweet_lower]
        
        if found_sensitive:
            if len(found_sensitive) > 2:
                risk_level = "high"
                reasons.append(f"Contains multiple sensitive topics: {', '.join(found_sensitive)}")
            else:
                risk_level = "medium"
                reasons.append(f"Contains sensitive topics: {', '.join(found_sensitive)}")
        
        words = tweet_text.split()
        caps_words = [word for word in words if word.isupper() and len(word) > 2]
        if len(caps_words) > 2:
            risk_level = max(risk_level, "medium")
            reasons.append("Contains excessive capitalization")
        
        if tweet_text.count('!') > 3 or tweet_text.count('?') > 3:
            risk_level = max(risk_level, "medium")
            reasons.append("Contains excessive punctuation")
        
        reason = ", ".join(reasons) if reasons else "No risk factors detected"
        
        return (risk_level, reason)
    
    def generate_tweet_suggestions(self, 
                                  user_tweets: List[str], 
                                  trending_topics: Optional[List[str]] = None, 
                                  count: int = 3) -> List[dict]:
        """
        Generate tweet suggestions based on user's previous tweets and trending topics
        """
        
        suggestions = []
        topics = trending_topics or ["AI", "Technology", "Innovation"]
        
        for i in range(count):
            topic = topics[i % len(topics)]
            confidence = 0.9 - (i * 0.1)
            
            if i == 0:
                text = f"Just explored the latest advancements in {topic}. The potential for innovation is more exciting than ever! #{topic} #Tech"
            elif i == 1:
                text = f"Interesting developments in {topic} today. What are your thoughts on how this will shape the future? #{topic} #Future"
            else:
                text = f"Working on a new project related to {topic}. Can't wait to share more details soon! #{topic} #Innovation"
            
            suggestions.append({
                "text": text,
                "topics": [topic, "Technology"],
                "confidence": confidence
            })
        
        return suggestions
    
    def generate_reply_options(self, tweet_text: str, count: int = 3, is_mention: bool = False, trending_score: float = 0.0) -> List[dict]:
        """
        Generate reply options for a given tweet
        
        Parameters:
        - tweet_text: The text of the tweet to reply to
        - count: Number of reply options to generate
        - is_mention: Whether this tweet is mentioning the user's account
        - trending_score: If not a mention, the trending score of the tweet (0.0-1.0)
        """
        
        sentiment = self.analyze_tweet_sentiment(tweet_text)
        topics = self.extract_topics(tweet_text)
        
        supportive_replies = [
            f"Great point about {topics[0] if topics else 'this'}! I completely agree.",
            f"This is exactly what I've been thinking about {topics[0] if topics else 'lately'}!",
            f"You've articulated this perfectly. Especially the part about {topics[0] if topics else 'the main point'}."
        ]
        
        neutral_replies = [
            f"Interesting perspective on {topics[0] if topics else 'this topic'}. Have you considered the alternative view?",
            f"I see your point, though I think there's more nuance to {topics[0] if topics else 'this discussion'}.",
            f"Thanks for sharing your thoughts on {topics[0] if topics else 'this'}. It's a complex issue."
        ]
        
        against_replies = [
            f"I respectfully disagree about {topics[0] if topics else 'this'}. Here's why...",
            f"While I see your point, I think there's a different way to look at {topics[0] if topics else 'this issue'}.",
            f"I have a different perspective on {topics[0] if topics else 'this'} that I'd like to share."
        ]
        
        mention_replies = [
            f"感谢提及我！关于{topics[0] if topics else '这个话题'}，我认为...",
            f"谢谢标记我！我对{topics[0] if topics else '这个'}的看法是...",
            f"感谢将我加入关于{topics[0] if topics else '这个话题'}的对话！"
        ]
        
        trending_replies = [
            f"这条推文正在获得很多关注，我认为{topics[0] if topics else '这个话题'}值得讨论！",
            f"看到这个热门话题 - {topics[0] if topics else '这个'}确实是当前的热点。",
            f"当大家都在讨论{topics[0] if topics else '这个热门话题'}时，我想补充..."
        ]
        
        options = []
        stances = ["supportive", "neutral", "against"]
        
        for i in range(count):
            stance = stances[i % len(stances)]
            confidence = 0.9 - (i * 0.1)
            
            if stance == "supportive":
                if is_mention:
                    text = mention_replies[i % len(mention_replies)]
                elif trending_score > 0.7:
                    text = trending_replies[i % len(trending_replies)]
                else:
                    text = supportive_replies[i % len(supportive_replies)]
            elif stance == "neutral":
                text = neutral_replies[i % len(neutral_replies)]
            else:
                text = against_replies[i % len(against_replies)]
            
            options.append({
                "text": text,
                "stance": stance,
                "confidence": confidence,
                "is_for_mention": is_mention,
                "is_for_trending": not is_mention and trending_score > 0.5
            })
        
        return options
