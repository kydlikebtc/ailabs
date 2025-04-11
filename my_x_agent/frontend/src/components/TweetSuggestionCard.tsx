import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { ThumbsUp, ThumbsDown, Clock } from 'lucide-react';
import { TweetSuggestion } from '../types';

interface TweetSuggestionCardProps {
  suggestion: TweetSuggestion;
  onApprove: (suggestion: TweetSuggestion) => void;
  onReject: (suggestion: TweetSuggestion) => void;
  onEdit: (suggestion: TweetSuggestion) => void;
}

export function TweetSuggestionCard({ suggestion, onApprove, onReject, onEdit }: TweetSuggestionCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-lg">Tweet Suggestion</CardTitle>
        <CardDescription className="flex items-center gap-1">
          <Clock className="h-4 w-4" />
          <span>{formatDate(suggestion.createdAt)}</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-base mb-4">{suggestion.text}</p>
        <div className="flex flex-wrap gap-2 mb-4">
          {suggestion.topics.map((topic, index) => (
            <Badge key={index} variant="secondary">{topic}</Badge>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">Confidence:</span>
          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: `${suggestion.confidence * 100}%` }}
            ></div>
          </div>
          <span className="text-sm">{Math.round(suggestion.confidence * 100)}%</span>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline" size="sm" onClick={() => onReject(suggestion)}>
          <ThumbsDown className="h-4 w-4 mr-2" />
          Reject
        </Button>
        <Button variant="outline" size="sm" onClick={() => onEdit(suggestion)}>
          Edit
        </Button>
        <Button variant="default" size="sm" onClick={() => onApprove(suggestion)}>
          <ThumbsUp className="h-4 w-4 mr-2" />
          Approve
        </Button>
      </CardFooter>
    </Card>
  );
}
