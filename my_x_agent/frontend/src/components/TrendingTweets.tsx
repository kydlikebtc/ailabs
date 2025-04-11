import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Tweet } from '../types';
import { MessageSquare, Repeat, Heart, BarChart2 } from 'lucide-react';

export function TrendingTweets() {
  const [trendingTweets, setTrendingTweets] = useState<Tweet[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTrendingTweets = () => {
      setIsLoading(true);
      
      setTimeout(() => {
        const mockTweets: Tweet[] = [
          {
            id: '1',
            text: 'Just announced our new AI model that can generate code 10x faster than previous versions. This is going to revolutionize software development! #AI #Coding #Tech',
            createdAt: new Date(Date.now() - 3600000).toISOString(),
            likes: 1245,
            retweets: 532,
            replies: 89,
            author: {
              username: 'techguru',
              displayName: 'Tech Guru',
              profileImageUrl: 'https://i.pravatar.cc/150?img=1'
            }
          },
          {
            id: '2',
            text: 'The latest cryptocurrency market trends show a significant shift towards sustainable blockchain solutions. What are your thoughts on eco-friendly mining? #Crypto #Blockchain #Sustainability',
            createdAt: new Date(Date.now() - 7200000).toISOString(),
            likes: 876,
            retweets: 321,
            replies: 154,
            author: {
              username: 'cryptoanalyst',
              displayName: 'Crypto Analyst',
              profileImageUrl: 'https://i.pravatar.cc/150?img=2'
            }
          },
          {
            id: '3',
            text: 'Our research team just published a groundbreaking paper on quantum computing applications in healthcare. This could transform how we approach disease modeling and drug discovery. #QuantumComputing #Healthcare #Science',
            createdAt: new Date(Date.now() - 10800000).toISOString(),
            likes: 2134,
            retweets: 987,
            replies: 203,
            author: {
              username: 'quantumlab',
              displayName: 'Quantum Research Lab',
              profileImageUrl: 'https://i.pravatar.cc/150?img=3'
            }
          },
          {
            id: '4',
            text: 'Just released our 2025 Tech Trends Report. The convergence of AI, IoT, and edge computing is creating unprecedented opportunities for innovation. Download the full report at the link below. #TechTrends #Innovation',
            createdAt: new Date(Date.now() - 14400000).toISOString(),
            likes: 1567,
            retweets: 743,
            replies: 112,
            author: {
              username: 'techresearch',
              displayName: 'Tech Research Institute',
              profileImageUrl: 'https://i.pravatar.cc/150?img=4'
            }
          }
        ];
        
        setTrendingTweets(mockTweets);
        setIsLoading(false);
      }, 1000);
    };
    
    fetchTrendingTweets();
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const handleRetweet = (tweetId: string) => {
    alert(`Preparing to retweet tweet ${tweetId}`);
  };

  const handleQuote = (tweetId: string) => {
    alert(`Preparing to quote tweet ${tweetId}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Trending Tweets</h1>
        <Button variant="outline" onClick={() => setIsLoading(true)}>
          <BarChart2 className="mr-2 h-4 w-4" />
          Refresh Trends
        </Button>
      </div>

      <Tabs defaultValue="engagement">
        <TabsList>
          <TabsTrigger value="engagement">Highest Engagement</TabsTrigger>
          <TabsTrigger value="tech">Tech</TabsTrigger>
          <TabsTrigger value="crypto">Crypto</TabsTrigger>
        </TabsList>
        
        <TabsContent value="engagement" className="mt-6">
          {isLoading ? (
            <div className="flex justify-center py-10">
              <p>Loading trending tweets...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {trendingTweets.map((tweet) => (
                <Card key={tweet.id}>
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-4">
                      <div className="h-10 w-10 rounded-full overflow-hidden">
                        <img 
                          src={tweet.author.profileImageUrl} 
                          alt={tweet.author.displayName} 
                          className="h-full w-full object-cover"
                        />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold">{tweet.author.displayName}</span>
                          <span className="text-gray-500">@{tweet.author.username}</span>
                          <span className="text-gray-500 text-xs ml-auto">
                            {formatDate(tweet.createdAt)}
                          </span>
                        </div>
                        <p className="mt-2">{tweet.text}</p>
                        <div className="flex items-center gap-6 mt-4">
                          <div className="flex items-center gap-1 text-gray-500">
                            <MessageSquare className="h-4 w-4" />
                            <span className="text-xs">{tweet.replies}</span>
                          </div>
                          <div className="flex items-center gap-1 text-gray-500">
                            <Repeat className="h-4 w-4" />
                            <span className="text-xs">{tweet.retweets}</span>
                          </div>
                          <div className="flex items-center gap-1 text-gray-500">
                            <Heart className="h-4 w-4" />
                            <span className="text-xs">{tweet.likes}</span>
                          </div>
                          <div className="ml-auto flex gap-2">
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => handleRetweet(tweet.id)}
                            >
                              Retweet
                            </Button>
                            <Button 
                              variant="default" 
                              size="sm"
                              onClick={() => handleQuote(tweet.id)}
                            >
                              Quote
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="tech" className="mt-6">
          {isLoading ? (
            <div className="flex justify-center py-10">
              <p>Loading tech tweets...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {trendingTweets
                .filter(tweet => tweet.text.toLowerCase().includes('ai') || 
                                tweet.text.toLowerCase().includes('tech') ||
                                tweet.text.toLowerCase().includes('quantum'))
                .map((tweet) => (
                  <Card key={tweet.id}>
                    <CardContent className="pt-6">
                      <div className="flex items-start gap-4">
                        <div className="h-10 w-10 rounded-full overflow-hidden">
                          <img 
                            src={tweet.author.profileImageUrl} 
                            alt={tweet.author.displayName} 
                            className="h-full w-full object-cover"
                          />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold">{tweet.author.displayName}</span>
                            <span className="text-gray-500">@{tweet.author.username}</span>
                            <span className="text-gray-500 text-xs ml-auto">
                              {formatDate(tweet.createdAt)}
                            </span>
                          </div>
                          <p className="mt-2">{tweet.text}</p>
                          <div className="flex items-center gap-6 mt-4">
                            <div className="flex items-center gap-1 text-gray-500">
                              <MessageSquare className="h-4 w-4" />
                              <span className="text-xs">{tweet.replies}</span>
                            </div>
                            <div className="flex items-center gap-1 text-gray-500">
                              <Repeat className="h-4 w-4" />
                              <span className="text-xs">{tweet.retweets}</span>
                            </div>
                            <div className="flex items-center gap-1 text-gray-500">
                              <Heart className="h-4 w-4" />
                              <span className="text-xs">{tweet.likes}</span>
                            </div>
                            <div className="ml-auto flex gap-2">
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => handleRetweet(tweet.id)}
                              >
                                Retweet
                              </Button>
                              <Button 
                                variant="default" 
                                size="sm"
                                onClick={() => handleQuote(tweet.id)}
                              >
                                Quote
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
              ))}
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="crypto" className="mt-6">
          {isLoading ? (
            <div className="flex justify-center py-10">
              <p>Loading crypto tweets...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {trendingTweets
                .filter(tweet => tweet.text.toLowerCase().includes('crypto') || 
                                tweet.text.toLowerCase().includes('blockchain'))
                .map((tweet) => (
                  <Card key={tweet.id}>
                    <CardContent className="pt-6">
                      <div className="flex items-start gap-4">
                        <div className="h-10 w-10 rounded-full overflow-hidden">
                          <img 
                            src={tweet.author.profileImageUrl} 
                            alt={tweet.author.displayName} 
                            className="h-full w-full object-cover"
                          />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold">{tweet.author.displayName}</span>
                            <span className="text-gray-500">@{tweet.author.username}</span>
                            <span className="text-gray-500 text-xs ml-auto">
                              {formatDate(tweet.createdAt)}
                            </span>
                          </div>
                          <p className="mt-2">{tweet.text}</p>
                          <div className="flex items-center gap-6 mt-4">
                            <div className="flex items-center gap-1 text-gray-500">
                              <MessageSquare className="h-4 w-4" />
                              <span className="text-xs">{tweet.replies}</span>
                            </div>
                            <div className="flex items-center gap-1 text-gray-500">
                              <Repeat className="h-4 w-4" />
                              <span className="text-xs">{tweet.retweets}</span>
                            </div>
                            <div className="flex items-center gap-1 text-gray-500">
                              <Heart className="h-4 w-4" />
                              <span className="text-xs">{tweet.likes}</span>
                            </div>
                            <div className="ml-auto flex gap-2">
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => handleRetweet(tweet.id)}
                              >
                                Retweet
                              </Button>
                              <Button 
                                variant="default" 
                                size="sm"
                                onClick={() => handleQuote(tweet.id)}
                              >
                                Quote
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
