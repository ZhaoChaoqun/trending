import React, { useMemo } from 'react';
import * as d3 from 'd3';
import { TREEMAP_DATA } from '../constants';

interface TreemapViewProps {}

export const TreemapView: React.FC<TreemapViewProps> = () => {
  const width = 1200;
  const height = 600;

  const root = useMemo(() => {
    const root = d3.hierarchy(TREEMAP_DATA)
      .sum((d: any) => d.size)
      .sort((a, b) => (b.value || 0) - (a.value || 0));

    return d3.treemap()
      .size([width, height])
      .paddingOuter(4)
      .paddingTop(20)
      .paddingInner(4)
      .round(true)(root);
  }, []);

  return (
    <div className="flex flex-col h-full bg-[#0f2123] overflow-hidden">
      {/* Header */}
      <div className="flex-none px-6 py-4 bg-[#102123] border-b border-[#21464a]">
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4 mb-4">
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">Tech Pulse Treemap</h1>
            <p className="text-[#8ec6cc] text-sm">Real-time GitHub market sentiment. Area = Growth, Color = Momentum.</p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
             <div className="bg-[#1c3538] p-1 rounded-lg flex border border-[#2d5d63]">
                <button className="px-3 py-1.5 rounded text-xs font-medium bg-[#102123] text-white shadow-sm border border-[#2d5d63]">24h</button>
                <button className="px-3 py-1.5 rounded text-xs font-medium text-[#8ec6cc] hover:text-white hover:bg-[#254246] transition-colors">7d</button>
             </div>
             <div className="h-8 w-px bg-[#2d5d63] mx-1"></div>
             <button className="px-3 py-1.5 rounded-lg bg-primary/20 text-primary border border-primary/30 text-sm font-medium">All Languages</button>
          </div>
        </div>
      </div>

      {/* Visualization */}
      <div className="flex-1 p-6 relative overflow-hidden">
        <div className="w-full h-full relative" style={{ minHeight: '600px' }}>
          {root.leaves().map((leaf: any, i) => {
             const isTop = leaf.data.name === 'langchain' || leaf.data.name === 'shadcn/ui' || leaf.data.name === 'bun';
             return (
              <div
                key={i}
                className="absolute border border-[#162a2d] hover:border-white/50 hover:z-10 hover:scale-[1.01] hover:shadow-2xl transition-all duration-200 rounded overflow-hidden cursor-pointer group"
                style={{
                  left: `${(leaf.x0 / width) * 100}%`,
                  top: `${(leaf.y0 / height) * 100}%`,
                  width: `${((leaf.x1 - leaf.x0) / width) * 100}%`,
                  height: `${((leaf.y1 - leaf.y0) / height) * 100}%`,
                  backgroundColor: leaf.data.color || '#1c3538',
                  background: isTop ? `linear-gradient(135deg, ${leaf.data.color}40, #1c3538 90%)` : leaf.data.color + '40'
                }}
              >
                <div className="absolute inset-0 p-3 flex flex-col justify-between">
                    <div className="flex justify-between items-start">
                        <span className={`font-bold ${isTop ? 'text-lg' : 'text-sm'} text-white truncate`}>{leaf.data.name}</span>
                        {isTop && <span className="text-[10px] bg-white/20 text-white px-1 rounded">HOT</span>}
                    </div>
                    {isTop && (
                         <div className="text-xs text-white/70 truncate">
                            {leaf.data.size.toLocaleString()} stars
                         </div>
                    )}
                </div>
              </div>
             )
          })}
          
          {/* Labels for Parents */}
          {root.children?.map((child: any, i) => (
             <div 
              key={`label-${i}`}
              className="absolute pointer-events-none text-white font-bold text-sm uppercase tracking-wider flex items-center gap-2"
              style={{
                  left: `${(child.x0 / width) * 100}%`,
                  top: `${(child.y0 / height) * 100}%`,
                  marginTop: '-24px',
                  marginLeft: '4px'
              }}
             >
                <div className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-purple-500' : i === 1 ? 'bg-blue-500' : 'bg-orange-500'}`}></div>
                {child.data.name}
             </div>
          ))}
        </div>
      </div>
    </div>
  );
};
