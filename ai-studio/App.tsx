import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { RepoList } from './components/RepoList';
import { DetailPanel } from './components/DetailPanel';
import { TreemapView } from './components/TreemapView';
import { DeepDiveView } from './components/DeepDiveView';
import { REPO_DATA } from './constants';
import { Search, Bell } from 'lucide-react';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState('dashboard'); // 'dashboard', 'treemap', 'deep-dive'
  const [selectedRepoId, setSelectedRepoId] = useState<string>(REPO_DATA[0].id);

  const selectedRepo = REPO_DATA.find(r => r.id === selectedRepoId) || REPO_DATA[0];

  const handleSelectRepo = (id: string) => {
    setSelectedRepoId(id);
    // If selecting OmniParse, user might want to go to deep dive, but we keep them on dashboard until clicked elsewhere in real app.
    // Here we just select it.
  };

  return (
    <div className="h-screen w-full flex overflow-hidden font-display selection:bg-electric-cyan selection:text-black bg-[#0D1117]">
      <Sidebar currentView={currentView} onChangeView={setCurrentView} />
      
      <main className="flex-1 flex flex-col h-full overflow-hidden bg-synapse-bg relative">
        {/* Top Search Bar - Only show on dashboard/treemap for consistent layout */}
        <header className="h-16 shrink-0 border-b border-synapse-border flex items-center justify-between px-8 bg-synapse-bg/80 backdrop-blur-md z-10 sticky top-0">
            <div className="flex items-center w-full max-w-xl relative">
                <Search className="absolute left-3 text-text-muted" size={18} />
                <input 
                    type="text" 
                    placeholder="Search repositories, discussions..." 
                    className="w-full bg-synapse-card border border-synapse-border rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-text-muted focus:outline-none focus:border-electric-cyan focus:ring-1 focus:ring-electric-cyan transition-all"
                />
                <div className="absolute right-3 flex gap-1">
                    <span className="px-1.5 py-0.5 rounded border border-synapse-border bg-[#0D1117] text-[10px] text-text-muted font-mono">⌘K</span>
                </div>
            </div>
            <div className="flex items-center gap-4">
                <button className="relative p-2 text-text-muted hover:text-white transition-colors">
                    <Bell size={20} />
                    <span className="absolute top-2 right-2 w-2 h-2 bg-electric-cyan rounded-full shadow-[0_0_5px_#00E5FF]"></span>
                </button>
            </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 flex overflow-hidden">
            {currentView === 'dashboard' && (
                <>
                    <RepoList 
                        repos={REPO_DATA} 
                        selectedRepoId={selectedRepoId} 
                        onSelectRepo={handleSelectRepo} 
                    />
                    <DetailPanel repo={selectedRepo} />
                </>
            )}
            
            {currentView === 'treemap' && (
                <div className="flex-1 h-full">
                    <TreemapView />
                </div>
            )}

             {currentView === 'deep-dive' && (
                <div className="flex-1 h-full">
                    <DeepDiveView />
                </div>
            )}
        </div>
      </main>
    </div>
  );
};

export default App;
