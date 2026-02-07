import React from 'react';
import { LayoutGrid, Bot, Globe, Smartphone, BarChart2, Flame, Star, Settings, ChevronRight } from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onChangeView: (view: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onChangeView }) => {
  const NavItem = ({ icon: Icon, label, id, active = false, hasSub = false }: any) => (
    <button 
      onClick={() => onChangeView(id)}
      className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group relative
        ${active 
          ? 'bg-electric-cyan/10 text-white border-l-2 border-electric-cyan' 
          : 'text-text-muted hover:text-white hover:bg-synapse-border/30 border-l-2 border-transparent'
        }`}
    >
      <Icon size={18} className={active ? 'text-electric-cyan' : 'group-hover:text-muted-mint transition-colors'} />
      <span className="text-sm font-medium">{label}</span>
      {hasSub && <ChevronRight size={14} className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />}
      {active && <div className="absolute inset-0 bg-electric-cyan/5 blur-sm -z-10" />}
    </button>
  );

  return (
    <aside className="w-64 h-full flex flex-col bg-[#161B22]/70 backdrop-blur-xl border-r border-synapse-border shrink-0 z-20">
      {/* Header */}
      <div className="h-16 flex items-center px-6 border-b border-synapse-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-electric-cyan to-blue-600 flex items-center justify-center shadow-neon-cyan">
            <Bot className="text-black" size={20} />
          </div>
          <h1 className="font-bold text-xl tracking-tight text-white">Synapse</h1>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-6 flex flex-col gap-6 px-4">
        <div>
          <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-3 px-2">Feeds</p>
          <div className="space-y-1">
            <NavItem icon={LayoutGrid} label="All Trending" id="dashboard" active={currentView === 'dashboard'} />
            <NavItem icon={Bot} label="LLM & AI" id="dashboard" />
            <NavItem icon={Globe} label="Web Dev" id="dashboard" />
            <NavItem icon={Smartphone} label="Mobile" id="dashboard" />
            <NavItem icon={BarChart2} label="Data Science" id="treemap" active={currentView === 'treemap'} />
          </div>
        </div>

        <div>
          <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-3 px-2">Insights</p>
          <div className="space-y-1">
            <NavItem icon={Flame} label="Viral on HN" id="dashboard" />
            <NavItem icon={Star} label="Rising Stars" id="dashboard" />
            <NavItem icon={BarChart2} label="Deep Dive: OmniParse" id="deep-dive" active={currentView === 'deep-dive'} />
          </div>
        </div>
      </div>

      {/* User */}
      <div className="p-4 border-t border-synapse-border">
        <button className="flex items-center gap-3 w-full p-2 rounded-lg hover:bg-synapse-border/30 transition-colors">
          <div 
            className="w-8 h-8 rounded-full bg-cover bg-center ring-2 ring-synapse-border"
            style={{backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuBmOsxwt-vhaOYB-Ffo3NB_DAdirzDMOsQ5v5xoQ26ljzf2Bi1cYczYIDJCEAUYpULe3lka0I650NK-HPVU21cxenGaUfpCfh_YA5FwvltllaR1xcDyMnLBsEEVPWZ9HMeIYSoGQyYaHxa9qubeprblu6AclyHwIPtGmPKQk3X-nYOBczjYMtKUckkpgf33cU6gSi3NUrBA7tWHNuxSNoILl-ebNv43J4zXv_1x7l_ZdMRgC0wygANlNb7N15Lh9DBB0Bgp2NDaMNug')`}}
          />
          <div className="flex flex-col items-start">
            <span className="text-sm font-medium text-white">Alex Dev</span>
            <span className="text-xs text-text-muted">Pro Plan</span>
          </div>
          <Settings size={16} className="ml-auto text-text-muted" />
        </button>
      </div>
    </aside>
  );
};
