import React from 'react';
import { Repo } from '../types';
import { ArrowUp, ArrowDown, Star, MessageSquare, ChevronRight, Minus } from 'lucide-react';

interface RepoListProps {
  repos: Repo[];
  selectedRepoId: string | null;
  onSelectRepo: (id: string) => void;
}

export const RepoList: React.FC<RepoListProps> = ({ repos, selectedRepoId, onSelectRepo }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-4">
      {repos.map((repo) => {
        const isSelected = selectedRepoId === repo.id;
        
        return (
          <div 
            key={repo.id}
            onClick={() => onSelectRepo(repo.id)}
            className={`group relative flex flex-col md:flex-row items-start md:items-center gap-4 p-4 rounded-xl border transition-all cursor-pointer
              ${isSelected 
                ? 'border-electric-cyan/30 bg-synapse-card/80 shadow-[0_0_15px_-3px_rgba(0,229,255,0.1)]' 
                : 'border-synapse-border bg-synapse-card/40 hover:bg-synapse-card hover:border-text-muted/30'
              }`}
          >
            {/* Rank */}
            <div className="flex flex-row md:flex-col items-center justify-center min-w-[3rem] gap-1 shrink-0">
              <span className={`text-2xl font-bold font-mono ${isSelected ? 'text-white' : 'text-text-muted group-hover:text-white'}`}>
                {String(repo.rank).padStart(2, '0')}
              </span>
              
              {repo.trend === 'up' && (
                <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-bold flex items-center
                  ${isSelected ? 'bg-electric-cyan/10 text-electric-cyan border border-electric-cyan/20' : 'bg-green-500/10 text-green-400 border border-green-500/20'}
                `}>
                  <ArrowUp size={10} className="mr-0.5" /> {repo.trendValue}
                </span>
              )}
               {repo.trend === 'down' && (
                <span className="px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 text-[10px] font-bold border border-red-500/20 flex items-center">
                  <ArrowDown size={10} className="mr-0.5" /> {repo.trendValue}
                </span>
              )}
               {repo.trend === 'neutral' && (
                <span className="px-1.5 py-0.5 rounded-full bg-synapse-border text-text-muted text-[10px] font-bold flex items-center">
                  <Minus size={10} />
                </span>
              )}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0 flex flex-col gap-1.5">
              <div className="flex items-center gap-3 flex-wrap">
                <h3 className={`text-lg font-mono font-bold truncate transition-colors ${isSelected ? 'text-electric-cyan' : 'text-white group-hover:text-electric-cyan'}`}>
                  {repo.owner}/{repo.name}
                </h3>
                {repo.isNew && (
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-glow-amber/10 text-glow-amber border border-glow-amber/30 shadow-neon-amber animate-pulse">
                    NEW
                  </span>
                )}
              </div>
              <p className="text-sm text-text-muted line-clamp-2 leading-relaxed">
                {repo.description}
              </p>
              
              <div className="flex items-center gap-4 mt-1">
                <div className="flex items-center gap-1.5 text-xs text-text-muted">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: repo.languageColor }}></span>
                  <span>{repo.language}</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-text-muted">
                  <Star size={12} />
                  <span>{repo.stars}</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-[#ff6600]">
                  <MessageSquare size={12} />
                  <span>{repo.hnComments} HN</span>
                </div>
                <div className="text-xs text-text-muted">Updated {repo.updated}</div>
              </div>
            </div>

            {/* Action Arrow */}
            <div className={`hidden md:flex items-center justify-center pr-2 transition-opacity ${isSelected ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}>
              <ChevronRight size={20} className={isSelected ? 'text-electric-cyan' : 'text-text-muted'} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
