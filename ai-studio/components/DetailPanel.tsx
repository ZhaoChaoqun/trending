import React from 'react';
import { Repo } from '../types';
import { Share2, Bookmark, Code, TrendingUp, Activity, MessageCircle } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

interface DetailPanelProps {
  repo: Repo;
}

const SPARKLINE_DATA = [
  { val: 10 }, { val: 15 }, { val: 12 }, { val: 20 }, { val: 25 }, 
  { val: 30 }, { val: 45 }, { val: 50 }, { val: 55 }, { val: 60 }
];

export const DetailPanel: React.FC<DetailPanelProps> = ({ repo }) => {
  return (
    <aside className="w-[400px] h-full flex flex-col bg-[#161B22]/70 backdrop-blur-xl border-l border-synapse-border shrink-0 z-20 overflow-y-auto hidden xl:flex">
      {/* Sticky Header */}
      <div className="p-6 pb-4 bg-[#0D1117]/90 backdrop-blur-md sticky top-0 z-10 border-b border-synapse-border">
        <div className="flex items-center justify-between mb-2">
          <span className="px-2 py-0.5 rounded bg-synapse-border/50 text-xs text-text-muted font-mono">Rank #{repo.rank}</span>
          <div className="flex gap-2">
            <button className="p-1.5 hover:bg-synapse-border rounded transition-colors text-text-muted hover:text-white">
              <Share2 size={16} />
            </button>
            <button className="p-1.5 hover:bg-synapse-border rounded transition-colors text-text-muted hover:text-white">
              <Bookmark size={16} />
            </button>
          </div>
        </div>
        
        <h2 className="text-2xl font-mono font-bold text-white leading-tight mb-2 truncate">{repo.name}</h2>
        
        <div className="flex gap-2 mb-4">
          <span className="px-2 py-0.5 rounded text-xs font-medium bg-blue-500/20 text-blue-300 border border-blue-500/30">{repo.language}</span>
          <span className="px-2 py-0.5 rounded text-xs font-medium bg-synapse-border text-text-muted">{repo.category}</span>
        </div>
        
        <a href="#" className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-electric-cyan hover:bg-cyan-400 text-black font-bold transition-all shadow-neon-cyan text-sm">
          <Code size={18} />
          View Repository
        </a>
      </div>

      <div className="p-6 space-y-6">
        {/* Trending Reason */}
        <div className="bg-[#0D1117]/60 border border-synapse-border/80 rounded-xl p-4 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full animate-[shimmer_2s_infinite]"></div>
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp size={18} className="text-electric-cyan" />
              <h4 className="text-sm font-bold text-white uppercase tracking-wide">Why it's trending</h4>
            </div>
            <p className="text-sm text-text-muted leading-relaxed">
              Sudden spike in interest due to the release of <span className="text-white font-medium">v5.0</span> which introduces plugin support and a new GUI. Major tech influencers on Twitter/X have been showcasing demos.
            </p>
        </div>

        {/* Growth Chart */}
        <div className="bg-[#0D1117]/60 border border-synapse-border/80 rounded-xl p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity size={18} className="text-muted-mint" />
              <h4 className="text-sm font-bold text-white uppercase tracking-wide">Star Growth</h4>
            </div>
            <span className="text-xs font-mono text-muted-mint">+1.2k / 24h</span>
          </div>
          
          <div className="h-24 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={SPARKLINE_DATA}>
                <Line 
                  type="monotone" 
                  dataKey="val" 
                  stroke="#00E5FF" 
                  strokeWidth={2} 
                  dot={{ r: 3, fill: "#00E5FF", strokeWidth: 0 }}
                  isAnimationActive={true}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-between mt-2 text-[10px] text-text-muted font-mono">
            <span>24h ago</span>
            <span>Now</span>
          </div>
        </div>

        {/* HN Comments */}
        <div className="bg-[#0D1117]/60 border-l-2 border-l-[#ff6600] border-y border-r border-synapse-border/80 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
             <div className="flex items-center gap-2">
                <MessageCircle size={18} className="text-[#ff6600]" />
                <h4 className="text-sm font-bold text-white uppercase tracking-wide">HN Top Comments</h4>
             </div>
             <a href="#" className="text-[10px] text-text-muted hover:text-white underline">View Thread</a>
          </div>
          <ul className="space-y-3">
            {[1, 2, 3].map((_, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-electric-cyan mt-1 text-[10px]">●</span>
                <p className="text-xs text-text-muted leading-relaxed">
                  <span className="text-white font-medium">user_{i}:</span> "The memory management is finally usable. I ran this on my M1 Air without swap issues."
                </p>
              </li>
            ))}
          </ul>
        </div>
        
        {/* Maintainer */}
         <div className="bg-[#0D1117]/60 border border-synapse-border/80 rounded-xl p-4 flex items-center gap-3">
            <div 
              className="w-10 h-10 rounded-full bg-cover bg-center ring-1 ring-synapse-border"
              style={{backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDBebOeMrWqnC2G2-R9MDVVtT4IthDCvRyMziVNfbh6QDiKsNHdLotWSRZN8ZGgsDUDv3Jlfhb2OCQWnVV5K8uEYFCW7fEgJo_2fGM_mfvTeyXOhGQSdNzoZu1g0JMj2IvPZe6dRLwLOuFmdBx3LSePRPGhDJ5Og5ScqMzPn6PEi-avRSyyL3gL6kYIdgpifkXKUfqIKV0y2YGNzzM7OJ7ccU3MEyTeHLaLUvhq0YFG3UAn7NMFXc1VCW7NaWJHJKhTGG-P5lgmjzS0')`}}
            />
            <div className="flex flex-col">
              <span className="text-xs text-text-muted uppercase">Maintained by</span>
              <span className="text-sm font-bold text-white">Significant-Gravitas</span>
            </div>
         </div>

      </div>
    </aside>
  );
};
