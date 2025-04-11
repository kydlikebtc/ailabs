import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { AlertTriangle, ThumbsUp, ThumbsDown, Minus } from 'lucide-react';
import { TweetAnalysis as TweetAnalysisType, ReplyOption } from '../types';

export function TweetAnalysis() {
  const [tweetText, setTweetText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState<TweetAnalysisType | null>(null);
  const [replyOptions, setReplyOptions] = useState<ReplyOption[]>([]);

  const handleAnalyzeTweet = async () => {
    if (!tweetText.trim()) return;
    
    setIsAnalyzing(true);
    
    setTimeout(() => {
      const mockAnalysis: TweetAnalysisType = {
        sentiment: Math.random() > 0.6 ? 'positive' : Math.random() > 0.3 ? 'neutral' : 'negative',
        topics: ['Technology', 'AI'],
        engagement: {
          estimated: 0.75,
          reason: 'Good hashtag usage, optimal length, contains a question'
        },
        riskAssessment: {
          level: 'low',
          reason: 'No risk factors detected'
        }
      };
      
      const mockReplyOptions: ReplyOption[] = [
        {
          id: '1',
          text: 'Great point about Technology! I completely agree with your perspective.',
          stance: 'supportive',
          confidence: 0.85
        },
        {
          id: '2',
          text: 'Interesting perspective on AI. Have you considered how this might impact privacy concerns?',
          stance: 'neutral',
          confidence: 0.78
        },
        {
          id: '3',
          text: 'I respectfully disagree about this. Here\'s why I think there\'s more to consider...',
          stance: 'against',
          confidence: 0.65
        }
      ];
      
      setAnalysis(mockAnalysis);
      setReplyOptions(mockReplyOptions);
      setIsAnalyzing(false);
    }, 1500);
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'negative':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      default:
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    }
  };

  const getStanceIcon = (stance: string) => {
    switch (stance) {
      case 'supportive':
        return <ThumbsUp className="h-4 w-4 text-green-500" />;
      case 'against':
        return <ThumbsDown className="h-4 w-4 text-red-500" />;
      default:
        return <Minus className="h-4 w-4 text-blue-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tweet Analysis</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Analyze a Tweet</CardTitle>
          <CardDescription>
            Enter a tweet to analyze its sentiment, engagement potential, and risk level
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Textarea
              placeholder="Enter a tweet to analyze..."
              value={tweetText}
              onChange={(e) => setTweetText(e.target.value)}
              className="min-h-[100px]"
            />
            <Button 
              onClick={handleAnalyzeTweet} 
              disabled={isAnalyzing || !tweetText.trim()}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze Tweet'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {analysis && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="text-sm font-medium mb-2">Sentiment</h3>
                <Badge className={getSentimentColor(analysis.sentiment)}>
                  {analysis.sentiment.charAt(0).toUpperCase() + analysis.sentiment.slice(1)}
                </Badge>
              </div>
              
              <div>
                <h3 className="text-sm font-medium mb-2">Topics</h3>
                <div className="flex flex-wrap gap-2">
                  {analysis.topics.map((topic, index) => (
                    <Badge key={index} variant="outline">{topic}</Badge>
                  ))}
                </div>
              </div>
              
              <div>
                <h3 className="text-sm font-medium mb-2">Engagement Potential</h3>
                <div className="space-y-2">
                  <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                    <div 
                      className="bg-blue-600 h-2.5 rounded-full" 
                      style={{ width: `${analysis.engagement.estimated * 100}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {analysis.engagement.reason}
                  </p>
                </div>
              </div>
              
              <div>
                <h3 className="text-sm font-medium mb-2">Risk Assessment</h3>
                <div className="flex items-center gap-2">
                  <AlertTriangle className={`h-4 w-4 ${
                    analysis.riskAssessment.level === 'high' ? 'text-red-500' : 
                    analysis.riskAssessment.level === 'medium' ? 'text-yellow-500' : 'text-green-500'
                  }`} />
                  <Badge className={getRiskLevelColor(analysis.riskAssessment.level)}>
                    {analysis.riskAssessment.level.charAt(0).toUpperCase() + analysis.riskAssessment.level.slice(1)}
                  </Badge>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  {analysis.riskAssessment.reason}
                </p>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Reply Options</CardTitle>
              <CardDescription>
                Choose from these AI-generated replies
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {replyOptions.map((option) => (
                  <div key={option.id} className="border rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      {getStanceIcon(option.stance)}
                      <Badge variant="outline">
                        {option.stance.charAt(0).toUpperCase() + option.stance.slice(1)}
                      </Badge>
                      <span className="text-xs text-gray-500 ml-auto">
                        {Math.round(option.confidence * 100)}% confidence
                      </span>
                    </div>
                    <p className="text-sm">{option.text}</p>
                    <div className="flex justify-end mt-2">
                      <Button variant="outline" size="sm">Use This Reply</Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
