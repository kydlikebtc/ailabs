import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { TweetSuggestionCard } from './TweetSuggestionCard';
import { TweetSuggestion } from '../types';
import { Plus, RefreshCw } from 'lucide-react';

const mockSuggestions: TweetSuggestion[] = [
  {
    id: '1',
    text: 'Just explored the latest advancements in AI language models. The potential for human-AI collaboration is more exciting than ever! #AI #MachineLearning #Tech',
    topics: ['AI', 'Technology', 'MachineLearning'],
    confidence: 0.92,
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    text: 'Cryptocurrency markets showing interesting patterns today. Always fascinating to watch the interplay between technology adoption and market dynamics. #Crypto #Blockchain #Markets',
    topics: ['Crypto', 'Blockchain', 'Markets'],
    confidence: 0.85,
    createdAt: new Date(Date.now() - 86400000).toISOString() // 1 day ago
  },
  {
    id: '3',
    text: 'Working on a new project that combines AI and social media analytics. Cannot wait to share more details soon! #Innovation #SocialMedia #DataScience',
    topics: ['Innovation', 'SocialMedia', 'DataScience'],
    confidence: 0.78,
    createdAt: new Date(Date.now() - 172800000).toISOString() // 2 days ago
  }
];

export function TweetSuggestions() {
  const [suggestions, setSuggestions] = useState<TweetSuggestion[]>(mockSuggestions);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateSuggestion = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const newSuggestion: TweetSuggestion = {
        id: `${Date.now()}`,
        text: 'New AI research shows promising results for solving complex optimization problems. This could revolutionize logistics and supply chain management! #AI #Optimization #SupplyChain',
        topics: ['AI', 'Optimization', 'SupplyChain'],
        confidence: 0.88,
        createdAt: new Date().toISOString()
      };
      setSuggestions([newSuggestion, ...suggestions]);
      setIsGenerating(false);
    }, 2000);
  };

  const handleApproveSuggestion = (suggestion: TweetSuggestion) => {
    alert(`Tweet approved: ${suggestion.text}`);
  };

  const handleRejectSuggestion = (suggestion: TweetSuggestion) => {
    setSuggestions(suggestions.filter(s => s.id !== suggestion.id));
  };

  const handleEditSuggestion = (suggestion: TweetSuggestion) => {
    alert(`Edit tweet: ${suggestion.text}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tweet Suggestions</h1>
        <Button onClick={handleGenerateSuggestion} disabled={isGenerating}>
          {isGenerating ? (
            <>
              <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Plus className="mr-2 h-4 w-4" />
              Generate New Suggestion
            </>
          )}
        </Button>
      </div>

      <Tabs defaultValue="all">
        <TabsList>
          <TabsTrigger value="all">All Suggestions</TabsTrigger>
          <TabsTrigger value="high">High Confidence</TabsTrigger>
          <TabsTrigger value="topics">By Topic</TabsTrigger>
        </TabsList>
        <TabsContent value="all" className="mt-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {suggestions.map(suggestion => (
              <TweetSuggestionCard
                key={suggestion.id}
                suggestion={suggestion}
                onApprove={handleApproveSuggestion}
                onReject={handleRejectSuggestion}
                onEdit={handleEditSuggestion}
              />
            ))}
          </div>
        </TabsContent>
        <TabsContent value="high" className="mt-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {suggestions
              .filter(s => s.confidence > 0.85)
              .map(suggestion => (
                <TweetSuggestionCard
                  key={suggestion.id}
                  suggestion={suggestion}
                  onApprove={handleApproveSuggestion}
                  onReject={handleRejectSuggestion}
                  onEdit={handleEditSuggestion}
                />
              ))}
          </div>
        </TabsContent>
        <TabsContent value="topics" className="mt-6">
          <div className="mb-6">
            <Input placeholder="Search by topic..." className="max-w-sm" />
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {suggestions.map(suggestion => (
              <TweetSuggestionCard
                key={suggestion.id}
                suggestion={suggestion}
                onApprove={handleApproveSuggestion}
                onReject={handleRejectSuggestion}
                onEdit={handleEditSuggestion}
              />
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
