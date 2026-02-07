import React from 'react';
import { OMNIPARSE_DATA } from '../constants';
import { Star, GitFork, Clock, Github, Rocket, MessageCircle, Terminal, CheckCircle, XCircle, AlertTriangle, Lightbulb } from 'lucide-react';

interface DeepDiveViewProps {}

export const DeepDiveView: React.FC<DeepDiveViewProps> = () => {
  const data = OMNIPARSE_DATA;

  return (
    <div className="flex-1 overflow-y-auto bg-[#0f1618] text-slate-300">
      <div className="max-w-7xl mx-auto px-6 py-8">
        
        {/* Breadcrumbs */}
        <div className="flex items-center gap-2 mb-8 text-sm text-slate-400">
            <span className="hover:text-primary transition-colors cursor-pointer">Trending</span>
            <span>/</span>
            <span className="text-white">{data.title}</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            {/* Left Content */}
            <div className="lg:col-span-8 flex flex-col gap-8">
                {/* Hero */}
                <div className="bg-[#162224]/70 backdrop-blur-md border border-primary/10 rounded-xl p-8 relative overflow-hidden group">
                    <div className="absolute -top-24 -right-24 size-64 bg-primary/10 blur-[80px] rounded-full pointer-events-none group-hover:bg-primary/15 transition-all duration-700"></div>
                    
                    <div className="relative z-10">
                        <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
                            <div className="flex flex-col gap-2">
                                <div className="flex items-center gap-3">
                                    <h1 className="text-4xl md:text-5xl font-black text-white tracking-tight">{data.title}</h1>
                                    <span className="bg-primary/10 text-primary border border-primary/20 text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider animate-pulse shadow-[0_0_10px_rgba(6,224,249,0.3)]">New</span>
                                </div>
                                <p className="text-slate-400 text-lg max-w-2xl">{data.description}</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <button className="flex items-center justify-center size-10 rounded-lg bg-[#24292e] hover:bg-[#2f363d] text-white border border-white/10 transition-all hover:-translate-y-0.5 shadow-lg">
                                    <Github size={20} />
                                </button>
                                <button className="flex items-center justify-center size-10 rounded-lg bg-[#ff6600] hover:bg-[#ff7417] text-white transition-all hover:-translate-y-0.5 shadow-lg shadow-orange-500/20">
                                    <span className="font-bold text-lg font-mono">Y</span>
                                </button>
                            </div>
                        </div>

                        <div className="flex flex-wrap items-center gap-6 text-sm text-slate-400 border-t border-white/5 pt-4 mt-2">
                            <div className="flex items-center gap-2">
                                <span className="size-2.5 rounded-full bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.5)]"></span>
                                <span>Python</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <Star size={16} />
                                <span className="text-white font-medium">{data.stars}</span> stars
                            </div>
                            <div className="flex items-center gap-1.5">
                                <GitFork size={16} />
                                <span className="text-white font-medium">{data.forks}</span> forks
                            </div>
                            <div className="flex items-center gap-1.5 ml-auto text-primary">
                                <Clock size={16} />
                                <span>Trending since 4h ago</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Technical Analysis */}
                <div className="rounded-xl border border-[#21464a] bg-[#131d1f] overflow-hidden">
                    <div className="px-6 py-4 border-b border-[#21464a] bg-[#1a2628] flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Terminal size={18} className="text-primary" />
                            <h3 className="text-white font-bold text-lg">Technical Analysis</h3>
                        </div>
                        <span className="text-xs font-mono text-slate-500 uppercase">LLM Generated • gpt-4-turbo</span>
                    </div>
                    <div className="p-6 md:p-8 text-slate-300 leading-relaxed space-y-4">
                        <h4 className="text-xl font-bold text-white mb-2">Technical Overview</h4>
                        <p>{data.techAnalysis}</p>
                        
                        <div className="grid md:grid-cols-2 gap-4 my-6">
                             <div className="bg-[#0f1618] p-4 rounded-lg border border-white/5">
                                <h5 className="text-primary font-bold mb-2 text-sm flex items-center gap-2">
                                    Core Capabilities
                                </h5>
                                <ul className="list-disc list-inside text-sm space-y-1 text-slate-400">
                                    {data.capabilities.map((c, i) => <li key={i}>{c}</li>)}
                                </ul>
                             </div>
                             <div className="bg-[#0f1618] p-4 rounded-lg border border-white/5">
                                <h5 className="text-secondary font-bold mb-2 text-sm flex items-center gap-2">
                                    Performance
                                </h5>
                                <ul className="list-disc list-inside text-sm space-y-1 text-slate-400">
                                    {data.performance.map((c, i) => <li key={i}>{c}</li>)}
                                </ul>
                             </div>
                        </div>
                    </div>
                </div>

                {/* Comparison Matrix */}
                <div className="rounded-xl border border-[#21464a] bg-[#131d1f] p-6">
                    <div className="flex items-center gap-2 mb-6">
                        <CheckCircle size={18} className="text-secondary" />
                        <h3 className="text-white font-bold text-lg">Why it Matters</h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-0 border border-[#21464a] rounded-lg overflow-hidden">
                        {/* Headers */}
                        <div className="hidden md:flex flex-col bg-[#1a2628] md:col-span-1 border-b md:border-b-0 md:border-r border-[#21464a]">
                            <div className="h-14"></div>
                            {Object.keys(data.whyItMatters).map(key => (
                                <div key={key} className="flex-1 p-4 border-b border-[#21464a] flex items-center text-sm font-medium text-slate-400 capitalize">
                                    {key.replace(/([A-Z])/g, ' $1').trim()}
                                </div>
                            ))}
                        </div>
                        {/* OmniParse */}
                        <div className="flex flex-col bg-[#0f1618]/50 md:col-span-1 border-b md:border-b-0 md:border-r border-[#21464a] relative">
                             <div className="absolute top-0 left-0 w-full h-1 bg-primary shadow-[0_0_10px_#06e0f9]"></div>
                             <div className="h-14 flex items-center justify-center border-b border-[#21464a] bg-[#131d1f]">
                                <span className="font-bold text-white text-lg">OmniParse</span>
                             </div>
                             <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-secondary">
                                <CheckCircle size={16} className="mr-2"/> Native
                             </div>
                             <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-secondary">
                                <CheckCircle size={16} className="mr-2"/> Advanced
                             </div>
                             <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-slate-300">
                                Moderate
                             </div>
                             <div className="flex-1 p-4 flex items-center justify-center text-sm text-white">
                                <span className="font-mono text-xs bg-slate-800 px-2 py-1 rounded">GPL-3.0</span>
                             </div>
                        </div>
                        {/* Standard */}
                        <div className="flex flex-col bg-[#131d1f] md:col-span-1">
                             <div className="h-14 flex items-center justify-center border-b border-[#21464a] bg-[#1a2628]">
                                <span className="font-bold text-slate-400 text-lg">Standard OCR</span>
                             </div>
                              <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-red-400">
                                <XCircle size={16} className="mr-2"/> Cloud/API
                             </div>
                             <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-yellow-400">
                                <AlertTriangle size={16} className="mr-2"/> Hit or Miss
                             </div>
                             <div className="flex-1 p-4 border-b border-[#21464a] flex items-center justify-center text-sm text-slate-300">
                                High
                             </div>
                             <div className="flex-1 p-4 flex items-center justify-center text-sm text-white">
                                <span className="font-mono text-xs bg-slate-800 px-2 py-1 rounded">Various</span>
                             </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Right Sidebar */}
            <div className="lg:col-span-4 flex flex-col gap-6">
                {/* HN Comments */}
                <div className="bg-[#162224]/50 border border-[#21464a] rounded-xl p-6">
                    <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center gap-2">
                            <MessageCircle size={18} className="text-[#ff6600]" />
                            <h3 className="text-white font-bold text-lg">HN Intelligence</h3>
                        </div>
                        <a href="#" className="text-xs text-primary hover:text-white transition-colors">View Thread</a>
                    </div>
                    <div className="space-y-4">
                        {data.comments.map((comment, i) => (
                             <div key={i} className="bg-[#1a2628] p-4 rounded-lg rounded-tl-none border border-white/5 relative">
                                <p className="text-slate-300 text-sm italic mb-2">"{comment.text}"</p>
                                <div className="flex items-center justify-between text-xs">
                                    <span className="font-bold text-primary">@{comment.user}</span>
                                    <span className="flex items-center gap-1 text-secondary font-medium">
                                        <ArrowUpIcon /> 142
                                    </span>
                                </div>
                             </div>
                        ))}
                    </div>
                </div>

                {/* Actionable Idea */}
                <div className="rounded-xl p-[1px] bg-gradient-to-br from-primary via-secondary to-primary/20 relative group">
                    <div className="absolute inset-0 bg-primary/20 blur-xl opacity-20 group-hover:opacity-40 transition-opacity"></div>
                    <div className="bg-[#0f1618] rounded-[11px] p-6 h-full relative z-10">
                        <div className="size-12 rounded-full bg-primary/10 flex items-center justify-center mb-4 text-primary border border-primary/20">
                            <Lightbulb size={24} />
                        </div>
                        <h4 className="text-white font-bold text-lg mb-2">Actionable Idea</h4>
                        <p className="text-slate-300 text-sm leading-relaxed mb-6">
                            Build a specialized VS Code extension that uses OmniParse to auto-document legacy PDF specs directly into your code comments.
                        </p>
                        <button className="w-full py-2.5 rounded-lg bg-primary hover:bg-[#33e7fc] text-[#0f1618] font-bold text-sm transition-colors flex items-center justify-center gap-2">
                            <span>Start Project</span>
                            <Rocket size={18} />
                        </button>
                    </div>
                </div>
            </div>

        </div>
      </div>
    </div>
  );
};

const ArrowUpIcon = () => (
    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
        <line x1="12" y1="19" x2="12" y2="5"></line>
        <polyline points="5 12 12 5 19 12"></polyline>
    </svg>
)
