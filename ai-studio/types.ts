export interface Repo {
  id: string;
  rank: number;
  name: string;
  owner: string;
  description: string;
  language: string;
  languageColor: string;
  stars: string;
  hnComments: number;
  updated: string;
  isNew?: boolean;
  trend: 'up' | 'down' | 'neutral';
  trendValue: number;
  category: string;
}

export interface Comment {
  user: string;
  text: string;
}

export interface DeepDiveData {
  title: string;
  subtitle: string;
  description: string;
  stars: string;
  forks: string;
  tags: string[];
  techAnalysis: string;
  capabilities: string[];
  performance: string[];
  whyItMatters: {
    privacy: string;
    tableExtraction: string;
    dependency: string;
    license: string;
  };
  comments: Comment[];
}
