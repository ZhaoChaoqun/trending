"""HTML 仪表板生成器 - Synapse 风格 3 列布局"""

import json
from datetime import datetime
from pathlib import Path
from .analyzer import RepoAnalysis
from .history import RankChange, format_rank_change

# 领域分类映射 (顺序重要：先检查具体关键词，再检查通用语言)
DOMAIN_MAPPING = {
    'AI & ML': {
        # AI/ML 特定关键词，避免使用太短或太通用的词
        'keywords': ['llm', 'gpt', 'langchain', 'llama', 'agent', 'transformer', 'openai', 'chatgpt',
                     'neural', 'deep-learning', 'machine-learning', 'embedding', 'rag', 'diffusion',
                     'stable-diffusion', 'ollama', 'huggingface', 'pytorch', 'tensorflow', 'model'],
        'languages': []  # 不依赖语言，仅靠关键词
    },
    'Frontend': {
        # 前端特定关键词
        'keywords': ['react', 'vue', 'nextjs', 'tailwind', 'frontend', 'shadcn', 'radix',
                     'svelte', 'angular', 'animation', 'design-system', 'component-library'],
        'languages': ['TypeScript', 'JavaScript', 'CSS', 'HTML', 'Vue', 'Svelte']
    },
    'System': {
        # 系统编程特定关键词
        'keywords': ['docker', 'kubernetes', 'runtime', 'compiler', 'kernel', 'database', 'server',
                     'cli', 'terminal', 'shell', 'async', 'concurrent', 'k8s', 'container'],
        'languages': ['Rust', 'Go', 'C', 'C++', 'Zig']
    },
    'Other': {
        'keywords': [],
        'languages': []
    }
}

# 语言颜色映射
LANG_COLORS = {
    'Python': '#3572A5',
    'JavaScript': '#f1e05a',
    'TypeScript': '#3178c6',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'Java': '#b07219',
    'C++': '#f34b7d',
    'C': '#555555',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Swift': '#F05138',
    'Kotlin': '#A97BFF',
    'Dart': '#00B4AB',
    'Vue': '#41b883',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Shell': '#89e051',
    'Zig': '#ec915c',
    'Jupyter Notebook': '#DA5B0B',
}


def classify_domain(repo_name: str, description: str, language: str) -> str:
    """
    基于仓库名、描述、语言分类到领域
    """
    text = f"{repo_name} {description}".lower()

    # 首先检查关键词
    for domain, config in DOMAIN_MAPPING.items():
        if domain == 'Other':
            continue
        for keyword in config['keywords']:
            if keyword in text:
                return domain

    # 然后检查语言
    for domain, config in DOMAIN_MAPPING.items():
        if domain == 'Other':
            continue
        if language in config['languages']:
            return domain

    return 'Other'


def get_lang_color(lang: str) -> str:
    """获取语言对应的颜色"""
    return LANG_COLORS.get(lang, '#8B949E')


def format_stars_display(stars_str: str) -> str:
    """格式化 Star 数显示"""
    try:
        num = int(str(stars_str).replace(',', '').replace(',', ''))
        if num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)
    except (ValueError, TypeError):
        return stars_str


def generate_sidebar_html(lang: str = 'zh') -> str:
    """生成左侧边栏 HTML"""
    texts = {
        'zh': {
            'feeds': '分类',
            'all': '全部热门',
            'ai_ml': 'AI & ML',
            'frontend': '前端开发',
            'system': '系统底层',
            'insights': '洞察',
            'rising': '上升最快',
            'new_today': '今日新上榜',
        },
        'en': {
            'feeds': 'Feeds',
            'all': 'All Trending',
            'ai_ml': 'AI & ML',
            'frontend': 'Frontend',
            'system': 'System',
            'insights': 'Insights',
            'rising': 'Rising Stars',
            'new_today': 'New Today',
        }
    }
    t = texts.get(lang, texts['zh'])

    return f'''
    <aside class="w-64 h-full flex flex-col glass-panel border-r border-synapse-border shrink-0 z-20">
        <!-- Header / Logo -->
        <div class="h-16 flex items-center px-6 border-b border-synapse-border">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-electric-cyan to-blue-600 flex items-center justify-center shadow-neon-cyan">
                    <span class="material-symbols-outlined text-black font-bold" style="font-size: 20px;">trending_up</span>
                </div>
                <div>
                    <h1 class="font-bold text-lg tracking-tight text-white">GitHub<span class="text-electric-cyan">Trending</span></h1>
                    <p class="text-[10px] text-text-muted font-mono tracking-wider">SYNAPSE v2.0</p>
                </div>
            </div>
        </div>

        <!-- Navigation -->
        <div class="flex-1 overflow-y-auto py-6 flex flex-col gap-2">
            <div class="px-4 mb-2">
                <p class="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">{t['feeds']}</p>
                <a href="#" class="nav-item-active flex items-center gap-3 px-3 py-2.5 rounded-r-lg transition-colors group" data-filter="all">
                    <span class="material-symbols-outlined text-electric-cyan">grid_view</span>
                    <span class="text-sm font-medium">{t['all']}</span>
                </a>
                <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors group border-l-2 border-transparent hover:border-text-muted/50 ml-1" data-filter="AI & ML">
                    <span class="material-symbols-outlined group-hover:text-muted-mint transition-colors">smart_toy</span>
                    <span class="text-sm font-medium">{t['ai_ml']}</span>
                </a>
                <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors group border-l-2 border-transparent hover:border-text-muted/50 ml-1" data-filter="Frontend">
                    <span class="material-symbols-outlined group-hover:text-muted-mint transition-colors">language</span>
                    <span class="text-sm font-medium">{t['frontend']}</span>
                </a>
                <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors group border-l-2 border-transparent hover:border-text-muted/50 ml-1" data-filter="System">
                    <span class="material-symbols-outlined group-hover:text-muted-mint transition-colors">memory</span>
                    <span class="text-sm font-medium">{t['system']}</span>
                </a>
            </div>
            <div class="px-4 mt-4">
                <p class="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">{t['insights']}</p>
                <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors border-l-2 border-transparent ml-1" data-filter="rising">
                    <span class="material-symbols-outlined text-muted-mint">rocket_launch</span>
                    <span class="text-sm font-medium">{t['rising']}</span>
                </a>
                <a href="#" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors border-l-2 border-transparent ml-1" data-filter="new">
                    <span class="material-symbols-outlined text-glow-amber">new_releases</span>
                    <span class="text-sm font-medium">{t['new_today']}</span>
                </a>
            </div>

            <!-- Hacker News Section -->
            <div class="px-4 mt-4">
                <p class="text-xs font-bold text-text-muted uppercase tracking-wider mb-2 px-2">
                    <span class="text-glow-amber">Y</span> Hacker News
                </p>
                <a href="../../hn.html" class="nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg text-text-muted hover:text-white hover:bg-synapse-border/30 transition-colors border-l-2 border-transparent hover:border-glow-amber/50 ml-1">
                    <span class="material-symbols-outlined text-glow-amber">local_fire_department</span>
                    <span class="text-sm font-medium">{'Top Stories' if lang == 'en' else 'Top Stories'}</span>
                </a>
            </div>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t border-synapse-border">
            <div class="flex items-center gap-2 text-xs text-text-muted">
                <span class="w-2 h-2 rounded-full bg-muted-mint pulse-dot"></span>
                <span class="font-mono">{'数据已同步' if lang == 'zh' else 'Data Synced'}</span>
            </div>
        </div>
    </aside>
    '''


def generate_detail_panel_html(lang: str = 'zh') -> str:
    """生成右侧详情面板 HTML (静态模板，由 JS 动态填充)"""
    texts = {
        'zh': {
            'rank': '排名',
            'view_repo': '查看仓库',
            'why_trending': '为什么在热榜',
            'star_growth': 'Star 增长',
            'ai_summary': 'AI 总结',
            'maintainer': '维护者',
            'select_hint': '点击左侧项目查看详情',
        },
        'en': {
            'rank': 'Rank',
            'view_repo': 'View Repository',
            'why_trending': 'Why it\'s trending',
            'star_growth': 'Star Growth',
            'ai_summary': 'AI Summary',
            'maintainer': 'Maintained by',
            'select_hint': 'Select a project to view details',
        }
    }
    t = texts.get(lang, texts['zh'])

    return f'''
    <aside id="detail-panel" class="w-[400px] h-full flex flex-col glass-panel border-l border-synapse-border shrink-0 z-20 overflow-y-auto hidden xl:flex">
        <!-- Placeholder when nothing selected -->
        <div id="detail-placeholder" class="flex-1 flex items-center justify-center">
            <div class="text-center text-text-muted">
                <span class="material-symbols-outlined text-4xl mb-2 block">touch_app</span>
                <p class="text-sm">{t['select_hint']}</p>
            </div>
        </div>

        <!-- Detail Content (hidden by default) -->
        <div id="detail-content" class="hidden">
            <!-- Sticky Header -->
            <div class="p-6 pb-4 bg-[#0D1117]/90 backdrop-blur-md sticky top-0 z-10 border-b border-synapse-border">
                <div class="flex items-center justify-between mb-2">
                    <span id="detail-rank" class="px-2 py-0.5 rounded bg-synapse-border/50 text-xs text-text-muted font-mono">{t['rank']} #1</span>
                    <div class="flex gap-2">
                        <span id="detail-new-badge" class="hidden px-2 py-0.5 rounded text-[10px] font-bold bg-glow-amber/10 text-glow-amber border border-glow-amber/30 animate-pulse">NEW</span>
                        <button onclick="copyToClipboard()" class="p-1.5 hover:bg-synapse-border rounded transition-colors text-text-muted hover:text-white" title="Copy link">
                            <span class="material-symbols-outlined text-sm">share</span>
                        </button>
                    </div>
                </div>
                <h2 id="detail-name" class="text-2xl font-mono font-bold text-white leading-tight mb-2">Project Name</h2>
                <p id="detail-author" class="text-sm text-electric-cyan font-mono mb-3">@owner</p>
                <div id="detail-tags" class="flex gap-2 flex-wrap mb-4">
                    <!-- Tags will be inserted here -->
                </div>
                <a id="detail-repo-link" href="#" target="_blank" class="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-electric-cyan hover:bg-cyan-400 text-black font-bold transition-all shadow-neon-cyan text-sm">
                    <span class="material-symbols-outlined text-lg">code</span>
                    {t['view_repo']}
                </a>
            </div>

            <div class="p-6 space-y-5">
                <!-- Description -->
                <div class="glass-card rounded-xl p-4">
                    <p id="detail-desc" class="text-sm text-text-muted leading-relaxed">
                        Project description will appear here...
                    </p>
                </div>

                <!-- Star Stats -->
                <div class="glass-card rounded-xl p-4">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-2">
                            <span class="material-symbols-outlined text-muted-mint text-lg">show_chart</span>
                            <h4 class="text-sm font-bold text-white uppercase tracking-wide">{t['star_growth']}</h4>
                        </div>
                        <span id="detail-stars-today" class="text-xs font-mono text-muted-mint">+0 / 24h</span>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="flex items-center gap-2">
                            <span class="material-symbols-outlined text-glow-amber">star</span>
                            <span id="detail-total-stars" class="text-2xl font-bold text-white">0</span>
                        </div>
                        <div class="flex-1 h-2 bg-synapse-border rounded-full overflow-hidden">
                            <div id="detail-stars-bar" class="h-full bg-gradient-to-r from-electric-cyan to-muted-mint rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>

                <!-- AI Summary -->
                <div id="detail-ai-section" class="glass-card rounded-xl p-4 border-l-2 border-l-glow-amber hidden">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="material-symbols-outlined text-glow-amber text-lg">auto_awesome</span>
                        <h4 class="text-sm font-bold text-white uppercase tracking-wide">{t['ai_summary']}</h4>
                    </div>
                    <p id="detail-ai-summary" class="text-sm text-text-muted leading-relaxed mb-3"></p>
                    <ul id="detail-ai-highlights" class="space-y-1 text-xs text-text-muted"></ul>
                    <p id="detail-ai-usecases" class="text-xs text-text-muted mt-3 pt-3 border-t border-synapse-border"></p>
                </div>

                <!-- Maintainer -->
                <div class="glass-card rounded-xl p-4 flex items-center gap-3">
                    <img id="detail-avatar" src="" alt="avatar" class="w-10 h-10 rounded-full ring-1 ring-synapse-border bg-synapse-card">
                    <div class="flex flex-col">
                        <span class="text-xs text-text-muted uppercase">{t['maintainer']}</span>
                        <span id="detail-maintainer" class="text-sm font-bold text-white">Owner</span>
                    </div>
                </div>
            </div>
        </div>
    </aside>
    '''


def generate_feed_item_html(analysis: RepoAnalysis, rank: int, rank_change: RankChange = None,
                            domain: str = 'Other', ai_summary=None) -> str:
    """生成单个 Feed 项目 HTML"""
    repo = analysis.repo
    is_new = rank_change.is_new if rank_change else False
    change_text = format_rank_change(rank_change) if rank_change else "-"
    change_val = rank_change.change if rank_change and rank_change.change else 0

    # 获取语言颜色
    lang_color = get_lang_color(repo.language or 'Other')

    # 截断描述
    desc = repo.description[:100] + '...' if len(repo.description) > 100 else repo.description
    desc = desc.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;').replace("'", "&#39;")

    # 排名变化样式
    if change_val > 0:
        change_badge = f'''<span class="px-1.5 py-0.5 rounded-full bg-electric-cyan/10 text-electric-cyan text-[10px] font-bold border border-electric-cyan/20 flex items-center">
            <span class="material-symbols-outlined text-[10px] mr-0.5">arrow_upward</span>{change_val}
        </span>'''
    elif change_val < 0:
        change_badge = f'''<span class="px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-400 text-[10px] font-bold border border-red-500/20 flex items-center">
            <span class="material-symbols-outlined text-[10px] mr-0.5">arrow_downward</span>{abs(change_val)}
        </span>'''
    else:
        change_badge = f'''<span class="px-1.5 py-0.5 rounded-full bg-synapse-border text-text-muted text-[10px] font-bold">-</span>'''

    # NEW 徽章
    new_badge = '''<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-glow-amber/10 text-glow-amber border border-glow-amber/30 shadow-neon-amber animate-pulse">NEW</span>''' if is_new else ''

    # 选中样式 (第一个默认选中)
    selected_class = 'border-electric-cyan/30 bg-synapse-card/80 shadow-[0_0_15px_-3px_rgba(0,229,255,0.1)]' if rank == 1 else 'border-synapse-border bg-synapse-card/40 hover:bg-synapse-card hover:border-text-muted/30'

    # 获取 owner 头像
    owner = repo.name.split('/')[0] if '/' in repo.name else repo.name
    short_name = repo.name.split('/')[-1] if '/' in repo.name else repo.name

    return f'''
    <div class="feed-item group relative flex flex-col md:flex-row items-start md:items-center gap-4 p-4 rounded-xl border {selected_class} transition-all cursor-pointer"
         data-repo-id="{repo.name}"
         data-domain="{domain}"
         data-is-new="{'true' if is_new else 'false'}"
         data-change="{change_val}"
         onclick="selectRepo('{repo.name}')">
        <!-- Rank -->
        <div class="flex flex-row md:flex-col items-center justify-center min-w-[3rem] gap-1 shrink-0">
            <span class="text-2xl font-bold {'text-white' if rank == 1 else 'text-text-muted group-hover:text-white'} transition-colors font-mono">{rank:02d}</span>
            {change_badge}
        </div>

        <!-- Content -->
        <div class="flex-1 min-w-0 flex flex-col gap-1.5">
            <div class="flex items-center gap-3 flex-wrap">
                <h3 class="text-lg font-mono font-bold {'text-electric-cyan' if rank == 1 else 'text-white group-hover:text-electric-cyan'} transition-colors truncate">{repo.name}</h3>
                {new_badge}
            </div>
            <p class="text-sm text-text-muted line-clamp-2 leading-relaxed">{desc}</p>
            <div class="flex items-center gap-4 mt-1 flex-wrap">
                <div class="flex items-center gap-1.5 text-xs text-text-muted">
                    <span class="w-2.5 h-2.5 rounded-full" style="background: {lang_color}"></span>
                    <span>{repo.language or 'Unknown'}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs text-text-muted">
                    <span class="material-symbols-outlined text-xs">star</span>
                    <span>{format_stars_display(repo.stars)}</span>
                </div>
                <div class="flex items-center gap-1.5 text-xs text-muted-mint">
                    <span class="material-symbols-outlined text-xs">add</span>
                    <span>+{repo.stars_today}</span>
                </div>
                <span class="px-1.5 py-0.5 rounded text-[10px] text-text-muted bg-synapse-border/50">{domain}</span>
            </div>
        </div>

        <!-- Arrow -->
        <div class="hidden md:flex items-center justify-center pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <span class="material-symbols-outlined {'text-electric-cyan' if rank == 1 else 'text-text-muted'}">chevron_right</span>
        </div>
    </div>
    '''


def calculate_momentum(stars_today: int, max_stars: int) -> str:
    """计算动量等级 (low/medium/high)"""
    if max_stars <= 0:
        return 'low'
    ratio = stars_today / max_stars
    if ratio > 0.6:
        return 'high'
    elif ratio > 0.3:
        return 'medium'
    return 'low'


def generate_treemap_item_html(repo: dict, size: str, rank: int, is_new: bool, momentum: str) -> str:
    """生成单个 Treemap 项目 HTML"""
    # 尺寸映射到 CSS grid
    size_classes = {
        'huge': 'col-span-8 row-span-5',
        'large': 'col-span-6 row-span-4',
        'medium': 'col-span-4 row-span-3',
        'small': 'col-span-3 row-span-2',
        'tiny': 'col-span-2 row-span-2'
    }

    # 动量颜色
    momentum_bg = {
        'high': 'bg-electric-cyan/30 border-electric-cyan/50',
        'medium': 'bg-[#2d5d63] border-[#3d7d83]',
        'low': 'bg-[#1c3538] border-[#2d5d63]'
    }

    # NEW 项目发光效果
    glow_class = 'shadow-[0_0_15px_rgba(0,229,255,0.4)] border-electric-cyan' if is_new else ''

    # 特殊标签
    badges = []
    if rank == 1:
        badges.append('<span class="text-[10px] bg-white/10 px-1.5 py-0.5 rounded text-white">#1 Trending</span>')
    if repo.get('change', 0) > 3:
        badges.append('<span class="text-[10px] text-electric-cyan">Rising</span>')
    if repo.get('starsToday', 0) > 500:
        badges.append('<span class="material-symbols-outlined text-glow-amber text-sm">local_fire_department</span>')

    badge_html = ' '.join(badges)

    # 增长百分比 (简化计算)
    stars_today = repo.get('starsToday', 0)
    growth_badge = f'<span class="text-[10px] font-mono text-muted-mint bg-muted-mint/10 px-1.5 py-0.5 rounded">+{stars_today}</span>' if stars_today > 0 else ''

    size_class = size_classes.get(size, 'col-span-3 row-span-2')
    bg_class = momentum_bg.get(momentum, momentum_bg['low'])

    # 大尺寸显示更多内容
    if size in ['huge', 'large']:
        content = f'''
            <div class="absolute inset-0 p-3 flex flex-col justify-between z-10">
                <div class="flex justify-between items-start">
                    <span class="font-bold text-white text-base truncate">{repo['name']}</span>
                    {growth_badge}
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-[10px] text-white/70">{repo.get('language', '')} • {format_stars_display(str(repo.get('stars', '0')))} ⭐</span>
                    {badge_html}
                </div>
            </div>
        '''
    elif size == 'medium':
        content = f'''
            <div class="absolute inset-0 p-2 flex flex-col justify-between">
                <span class="font-bold text-white text-sm truncate">{repo['name']}</span>
                <span class="text-[10px] text-white/70">{growth_badge}</span>
            </div>
        '''
    else:
        content = f'''
            <div class="absolute inset-0 p-2 flex items-center justify-center">
                <span class="font-medium text-white/80 text-xs truncate">{repo['name']}</span>
            </div>
        '''

    return f'''
        <div class="treemap-item {size_class} {bg_class} {glow_class} border relative rounded overflow-hidden cursor-pointer hover:border-white/50 transition-all"
             onclick="window.open('{repo.get('url', '#')}', '_blank')">
            {content}
        </div>
    '''


def generate_domain_column_html(domain: str, repos: list, max_stars: int, lang: str = 'zh') -> str:
    """生成单个领域列的 HTML"""
    domain_colors = {
        'AI & ML': 'bg-purple-500',
        'Frontend': 'bg-blue-500',
        'System': 'bg-orange-500',
        'Other': 'bg-gray-500'
    }

    domain_names = {
        'zh': {
            'AI & ML': 'AI & 机器学习',
            'Frontend': '前端 & Web',
            'System': '系统 & 基础设施',
            'Other': '其他'
        },
        'en': {
            'AI & ML': 'AI & Machine Learning',
            'Frontend': 'Frontend & Web',
            'System': 'System & Infrastructure',
            'Other': 'Other'
        }
    }

    color_class = domain_colors.get(domain, 'bg-gray-500')
    display_name = domain_names.get(lang, domain_names['en']).get(domain, domain)

    # 生成 treemap 项目
    items_html = []

    # 根据项目数量动态选择尺寸，避免少量项目时差距过大
    repo_count = len(repos[:8])
    if repo_count == 1:
        sizes = ['huge']
    elif repo_count == 2:
        sizes = ['huge', 'large']
    elif repo_count == 3:
        sizes = ['large', 'large', 'medium']
    elif repo_count == 4:
        sizes = ['large', 'medium', 'medium', 'medium']
    elif repo_count == 5:
        sizes = ['large', 'medium', 'medium', 'small', 'small']
    else:
        sizes = ['huge', 'large', 'medium', 'medium', 'small', 'small', 'tiny', 'tiny']

    for i, repo in enumerate(repos[:8]):
        size = sizes[i] if i < len(sizes) else 'tiny'
        momentum = calculate_momentum(repo.get('starsToday', 0), max_stars)
        is_new = repo.get('isNew', False)
        rank = repo.get('rank', i + 1)
        items_html.append(generate_treemap_item_html(repo, size, rank, is_new, momentum))

    return f'''
        <div class="flex flex-col h-full gap-2">
            <div class="flex items-center justify-between px-1">
                <h3 class="text-white font-semibold text-sm tracking-wide flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full {color_class}"></span>
                    {display_name}
                </h3>
                <span class="text-xs text-text-muted">{len(repos)} Repos</span>
            </div>
            <div class="flex-1 relative bg-synapse-card/30 rounded-xl overflow-hidden p-1 border border-synapse-border min-h-[280px]">
                <div class="treemap-grid">
                    {''.join(items_html)}
                </div>
            </div>
        </div>
    '''


def generate_treemap_section(analyses: list[RepoAnalysis], lang: str = 'zh',
                             rank_changes: list = None) -> str:
    """生成 Tech Pulse Treemap - 3 列布局"""
    if not analyses:
        return ''

    if rank_changes is None:
        rank_changes = []

    # 创建 name -> RankChange 映射
    change_map = {c.name: c for c in rank_changes}

    # 按领域分组并收集数据
    domain_data = {'AI & ML': [], 'Frontend': [], 'System': [], 'Other': []}
    max_stars = 0

    for i, analysis in enumerate(analyses[:25], 1):
        repo = analysis.repo
        domain = classify_domain(repo.name, repo.description, repo.language or '')

        try:
            stars_today = int(str(repo.stars_today).replace(',', ''))
        except (ValueError, TypeError):
            stars_today = 0

        max_stars = max(max_stars, stars_today)

        change = change_map.get(repo.name)

        domain_data[domain].append({
            'name': repo.name.split('/')[-1],
            'fullName': repo.name,
            'stars': repo.stars,
            'starsToday': stars_today,
            'language': repo.language or 'Unknown',
            'url': repo.url,
            'rank': i,
            'isNew': change.is_new if change else False,
            'change': change.change if change and change.change else 0
        })

    # 文本
    texts = {
        'zh': {
            'title': 'Tech Pulse Treemap',
            'subtitle': '实时 GitHub 市场情绪。面积 = 增长，颜色 = 动量。',
            'intensity': '强度',
            'low': '低动量',
            'high': '高动量',
            'new_repo': '新项目 (发光边框)'
        },
        'en': {
            'title': 'Tech Pulse Treemap',
            'subtitle': 'Real-time GitHub market sentiment. Area = Growth, Color = Momentum.',
            'intensity': 'Intensity Key',
            'low': 'Low Momentum',
            'high': 'High Momentum',
            'new_repo': 'New Repo (Outer Glow)'
        }
    }
    t = texts.get(lang, texts['en'])

    # 生成每个领域的列 (只显示有数据的领域，最多3列)
    columns_html = []
    for domain in ['AI & ML', 'Frontend', 'System']:
        if domain_data[domain]:
            columns_html.append(generate_domain_column_html(domain, domain_data[domain], max_stars, lang))

    # 如果少于3列，添加 Other
    if len(columns_html) < 3 and domain_data['Other']:
        columns_html.append(generate_domain_column_html('Other', domain_data['Other'], max_stars, lang))

    # 收集所有语言用于筛选按钮
    all_languages = set()
    for repos in domain_data.values():
        for repo in repos:
            if repo['language'] != 'Unknown':
                all_languages.add(repo['language'])
    top_languages = sorted(all_languages, key=lambda x: sum(1 for repos in domain_data.values() for r in repos if r['language'] == x), reverse=True)[:3]

    lang_buttons = ''.join([
        f'<button class="treemap-lang-filter flex items-center gap-2 px-3 py-1.5 rounded-lg bg-synapse-card hover:bg-synapse-border text-text-muted hover:text-white border border-synapse-border transition-colors text-sm font-medium" data-lang="{l}">{l}</button>'
        for l in top_languages
    ])

    return f'''
    <section class="mb-8">
        <!-- Header -->
        <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-4 mb-4">
            <div>
                <div class="flex items-center gap-3 mb-1">
                    <span class="material-symbols-outlined text-electric-cyan">local_fire_department</span>
                    <h2 class="text-xl font-bold text-white">{t['title']}</h2>
                </div>
                <p class="text-text-muted text-sm">{t['subtitle']}</p>
            </div>
            <div class="flex flex-wrap items-center gap-3">
                <!-- Time Range Toggle -->
                <div class="bg-synapse-card p-1 rounded-lg flex border border-synapse-border">
                    <button class="treemap-time-filter px-3 py-1.5 rounded text-xs font-medium bg-synapse-bg text-white shadow-sm border border-synapse-border" data-time="24h">24h</button>
                    <button class="treemap-time-filter px-3 py-1.5 rounded text-xs font-medium text-text-muted hover:text-white hover:bg-synapse-border transition-colors" data-time="7d">7d</button>
                    <button class="treemap-time-filter px-3 py-1.5 rounded text-xs font-medium text-text-muted hover:text-white hover:bg-synapse-border transition-colors" data-time="30d">30d</button>
                </div>
                <div class="h-8 w-px bg-synapse-border mx-1 hidden md:block"></div>
                <!-- Language Filters -->
                <button class="treemap-lang-filter flex items-center gap-2 px-3 py-1.5 rounded-lg bg-electric-cyan/20 text-electric-cyan border border-electric-cyan/30 text-sm font-medium" data-lang="all">
                    <span>All Languages</span>
                </button>
                {lang_buttons}
            </div>
        </div>

        <!-- Legend -->
        <div class="flex items-center gap-4 text-xs text-text-muted border-t border-b border-synapse-border py-3 mb-4">
            <span class="uppercase tracking-wider font-semibold">{t['intensity']}:</span>
            <div class="flex items-center gap-2">
                <span>{t['low']}</span>
                <div class="h-3 w-32 rounded-full bg-gradient-to-r from-[#1c3538] via-[#2d5d63] to-electric-cyan"></div>
                <span class="text-white">{t['high']}</span>
            </div>
            <div class="ml-6 flex items-center gap-2">
                <div class="w-3 h-3 border border-electric-cyan shadow-[0_0_8px_rgba(0,229,255,0.3)] rounded-sm"></div>
                <span class="text-electric-cyan">{t['new_repo']}</span>
            </div>
        </div>

        <!-- 3 Column Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {''.join(columns_html)}
        </div>
    </section>

    <style>
        .treemap-grid {{
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 4px;
            height: 100%;
        }}

        .treemap-item {{
            transition: transform 0.2s ease, z-index 0s;
        }}

        .treemap-item:hover {{
            z-index: 10;
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
    </style>

    <script>
    (function() {{
        // 时间筛选按钮点击 (暂时只做 UI 效果，实际筛选需要后端数据支持)
        document.querySelectorAll('.treemap-time-filter').forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.treemap-time-filter').forEach(function(b) {{
                    b.classList.remove('bg-synapse-bg', 'text-white', 'shadow-sm', 'border-synapse-border');
                    b.classList.add('text-text-muted');
                }});
                this.classList.add('bg-synapse-bg', 'text-white', 'shadow-sm', 'border-synapse-border');
                this.classList.remove('text-text-muted');
            }});
        }});

        // 语言筛选按钮点击
        document.querySelectorAll('.treemap-lang-filter').forEach(function(btn) {{
            btn.addEventListener('click', function() {{
                var lang = this.dataset.lang;

                // 更新按钮样式
                document.querySelectorAll('.treemap-lang-filter').forEach(function(b) {{
                    b.classList.remove('bg-electric-cyan/20', 'text-electric-cyan', 'border-electric-cyan/30');
                    b.classList.add('bg-synapse-card', 'text-text-muted', 'border-synapse-border');
                }});
                this.classList.add('bg-electric-cyan/20', 'text-electric-cyan', 'border-electric-cyan/30');
                this.classList.remove('bg-synapse-card', 'text-text-muted', 'border-synapse-border');

                // TODO: 实际的筛选逻辑 (需要重新渲染 treemap)
                console.log('Filter by language:', lang);
            }});
        }});
    }})();
    </script>
    '''


def generate_stats_bar(analyses: list[RepoAnalysis], lang: str = 'zh') -> str:
    """生成顶部统计条"""
    if not analyses:
        return ''

    total_stars = 0
    new_count = 0
    lang_count = {}

    for a in analyses:
        try:
            total_stars += int(str(a.repo.stars_today).replace(',', ''))
        except:
            pass
        prog_lang = a.repo.language or 'Other'
        lang_count[prog_lang] = lang_count.get(prog_lang, 0) + 1

    top_lang = max(lang_count.items(), key=lambda x: x[1])[0] if lang_count else 'Unknown'
    avg_score = round(sum(a.score for a in analyses) / len(analyses), 1) if analyses else 0

    def fmt(n):
        if n >= 1000:
            return f'{n/1000:.1f}k'
        return str(n)

    texts = {
        'zh': ['今日 Star', '平均评分', '热门项目', '热门语言'],
        'en': ['Stars Today', 'Avg Score', 'Projects', 'Top Lang']
    }
    t = texts.get(lang, texts['zh'])

    return f'''
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-muted-mint/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-muted-mint">star</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[0]}</p>
                <p class="text-xl font-bold text-white">{fmt(total_stars)}</p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-electric-cyan/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-electric-cyan">analytics</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[1]}</p>
                <p class="text-xl font-bold text-white">{avg_score}<span class="text-sm text-text-muted">/10</span></p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-glow-amber/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-glow-amber">folder</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[2]}</p>
                <p class="text-xl font-bold text-white">{len(analyses)}</p>
            </div>
        </div>
        <div class="glass-card rounded-xl p-4 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center">
                <span class="material-symbols-outlined text-purple-400">code</span>
            </div>
            <div>
                <p class="text-xs text-text-muted">{t[3]}</p>
                <p class="text-xl font-bold text-white">{top_lang}</p>
            </div>
        </div>
    </div>
    '''


def generate_repo_data_script(analyses: list[RepoAnalysis], rank_changes: list[RankChange],
                               ai_summaries: dict = None) -> str:
    """生成 JavaScript 数据对象供详情面板使用"""
    if ai_summaries is None:
        ai_summaries = {}

    change_map = {c.name: c for c in rank_changes}

    repo_data = {}
    for i, analysis in enumerate(analyses, 1):
        repo = analysis.repo
        change = change_map.get(repo.name)
        ai = ai_summaries.get(repo.name)

        owner = repo.name.split('/')[0] if '/' in repo.name else repo.name
        short_name = repo.name.split('/')[-1] if '/' in repo.name else repo.name

        # 安全处理描述文本
        desc = repo.description.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', '')

        repo_data[repo.name] = {
            'rank': i,
            'name': short_name,
            'fullName': repo.name,
            'owner': owner,
            'description': desc,
            'url': repo.url,
            'stars': repo.stars,
            'starsToday': repo.stars_today,
            'language': repo.language or 'Unknown',
            'langColor': get_lang_color(repo.language or 'Unknown'),
            'score': analysis.score,
            'domain': classify_domain(repo.name, repo.description, repo.language or ''),
            'isNew': change.is_new if change else False,
            'change': change.change if change and change.change else 0,
            'avatar': f'https://github.com/{owner}.png?size=80',
            'aiSummary': ai.summary if ai else None,
            'aiHighlights': ai.highlights if ai else [],
            'aiUseCases': ai.use_cases if ai else None,
        }

    return f'''
    <script>
    window.REPO_DATA = {json.dumps(repo_data, ensure_ascii=False)};
    </script>
    '''


def generate_dashboard_html(analyses: list[RepoAnalysis],
                            rank_changes: list[RankChange],
                            date: datetime = None,
                            lang: str = 'zh',
                            ai_summaries: dict = None) -> str:
    """
    生成完整的 Synapse 风格 HTML 仪表板
    """
    if date is None:
        date = datetime.now()

    if ai_summaries is None:
        ai_summaries = {}

    date_str = date.strftime('%Y-%m-%d')
    html_lang = 'zh-CN' if lang == 'zh' else 'en'

    # 创建 name -> RankChange 映射
    change_map = {c.name: c for c in rank_changes}

    # 按评分排序取前25
    sorted_analyses = sorted(analyses, key=lambda x: x.score, reverse=True)[:25]

    # 生成 Feed 列表
    feed_items = []
    for i, analysis in enumerate(sorted_analyses, 1):
        change = change_map.get(analysis.repo.name)
        domain = classify_domain(analysis.repo.name, analysis.repo.description, analysis.repo.language or '')
        ai_summary = ai_summaries.get(analysis.repo.name)
        feed_items.append(generate_feed_item_html(analysis, i, change, domain, ai_summary))

    texts = {
        'zh': {
            'title': 'GitHub Trending - Synapse',
            'search_placeholder': '搜索项目...',
            'all_projects': '全部项目',
        },
        'en': {
            'title': 'GitHub Trending - Synapse',
            'search_placeholder': 'Search projects...',
            'all_projects': 'All Projects',
        }
    }
    t = texts.get(lang, texts['zh'])

    return f'''<!DOCTYPE html>
<html lang="{html_lang}" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']} - {date_str}</title>
    <link rel="icon" href="https://github.githubassets.com/favicons/favicon.svg" type="image/svg+xml">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com?plugins=forms"></script>

    <!-- ECharts -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

    <!-- Tailwind Config -->
    <script>
        tailwind.config = {{
            darkMode: "class",
            theme: {{
                extend: {{
                    colors: {{
                        "synapse-bg": "#0D1117",
                        "synapse-card": "#161B22",
                        "synapse-border": "#30363D",
                        "electric-cyan": "#00E5FF",
                        "muted-mint": "#70FFC9",
                        "glow-amber": "#FFAB00",
                        "text-main": "#C9D1D9",
                        "text-muted": "#8B949E",
                    }},
                    fontFamily: {{
                        "display": ["Inter", "sans-serif"],
                        "mono": ["JetBrains Mono", "monospace"],
                    }},
                    boxShadow: {{
                        'neon-cyan': '0 0 5px theme("colors.electric-cyan"), 0 0 20px theme("colors.electric-cyan")',
                        'neon-amber': '0 0 5px theme("colors.glow-amber"), 0 0 10px rgba(255, 171, 0, 0.5)',
                    }}
                }},
            }},
        }}
    </script>

    <style>
        body {{
            background-color: #0D1117;
            color: #C9D1D9;
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: #0D1117;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #30363D;
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #00E5FF;
        }}

        .glass-panel {{
            background: rgba(22, 27, 34, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(48, 54, 61, 0.5);
        }}

        .glass-card {{
            background: rgba(13, 17, 23, 0.6);
            border: 1px solid rgba(48, 54, 61, 0.8);
        }}

        .nav-item-active {{
            background: rgba(0, 229, 255, 0.1);
            border-left: 3px solid #00E5FF;
            color: #fff;
        }}

        .pulse-dot {{
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}

        .feed-item.selected {{
            border-color: rgba(0, 229, 255, 0.3) !important;
            background: rgba(22, 27, 34, 0.8) !important;
            box-shadow: 0 0 15px -3px rgba(0, 229, 255, 0.1);
        }}

        .feed-item.selected h3 {{
            color: #00E5FF !important;
        }}

        .feed-item.selected .rank-num {{
            color: #fff !important;
        }}
    </style>
</head>
<body class="h-screen w-full flex overflow-hidden font-display selection:bg-electric-cyan selection:text-black">

    {generate_sidebar_html(lang)}

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col h-full overflow-hidden bg-synapse-bg relative">
        <!-- Top Search Bar -->
        <header class="h-16 shrink-0 border-b border-synapse-border flex items-center justify-between px-6 bg-synapse-bg/80 backdrop-blur-md z-10 sticky top-0">
            <div class="flex items-center w-full max-w-md relative">
                <span class="material-symbols-outlined absolute left-3 text-text-muted">search</span>
                <input type="text" id="search-input"
                    class="w-full bg-synapse-card border border-synapse-border rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder-text-muted focus:outline-none focus:border-electric-cyan focus:ring-1 focus:ring-electric-cyan transition-all"
                    placeholder="{t['search_placeholder']}"
                    onkeyup="filterBySearch(this.value)">
            </div>
            <div class="flex items-center gap-4">
                <span class="text-sm text-text-muted font-mono">{date_str}</span>
                <button onclick="window.open('https://github.com/trending', '_blank')" class="p-2 text-text-muted hover:text-white transition-colors" title="GitHub Trending">
                    <span class="material-symbols-outlined">open_in_new</span>
                </button>
            </div>
        </header>

        <!-- Feed List -->
        <div class="flex-1 overflow-y-auto p-4 md:p-6">
            {generate_stats_bar(sorted_analyses, lang)}

            {generate_treemap_section(sorted_analyses, lang, rank_changes)}

            <div class="flex items-center gap-3 mb-4">
                <span class="material-symbols-outlined text-electric-cyan">apps</span>
                <h2 class="text-lg font-bold text-white">{t['all_projects']}</h2>
                <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-synapse-border text-text-muted">TOP {len(sorted_analyses)}</span>
            </div>

            <div id="feed-list" class="space-y-3">
                {''.join(feed_items)}
            </div>
        </div>
    </main>

    {generate_detail_panel_html(lang)}

    {generate_repo_data_script(sorted_analyses, rank_changes, ai_summaries)}

    <script>
    // 当前选中的 repo
    var currentRepoId = null;

    // 选中 repo 并更新详情面板
    function selectRepo(repoId) {{
        var repo = window.REPO_DATA[repoId];
        if (!repo) return;

        currentRepoId = repoId;

        // 更新选中状态
        document.querySelectorAll('.feed-item').forEach(function(item) {{
            item.classList.remove('selected');
            if (item.dataset.repoId === repoId) {{
                item.classList.add('selected');
            }}
        }});

        // 显示详情内容
        document.getElementById('detail-placeholder').classList.add('hidden');
        document.getElementById('detail-content').classList.remove('hidden');

        // 填充数据
        document.getElementById('detail-rank').textContent = 'Rank #' + repo.rank;
        document.getElementById('detail-name').textContent = repo.name;
        document.getElementById('detail-author').textContent = '@' + repo.owner;
        document.getElementById('detail-desc').textContent = repo.description;
        document.getElementById('detail-repo-link').href = repo.url;
        document.getElementById('detail-total-stars').textContent = repo.stars;
        document.getElementById('detail-stars-today').textContent = '+' + repo.starsToday + ' / 24h';
        document.getElementById('detail-maintainer').textContent = repo.owner;
        document.getElementById('detail-avatar').src = repo.avatar;

        // NEW 徽章
        var newBadge = document.getElementById('detail-new-badge');
        if (repo.isNew) {{
            newBadge.classList.remove('hidden');
        }} else {{
            newBadge.classList.add('hidden');
        }}

        // 标签
        var tagsContainer = document.getElementById('detail-tags');
        tagsContainer.innerHTML = '';

        // 语言标签
        var langTag = document.createElement('span');
        langTag.className = 'px-2 py-0.5 rounded text-xs font-medium border';
        langTag.style.backgroundColor = repo.langColor + '20';
        langTag.style.color = repo.langColor;
        langTag.style.borderColor = repo.langColor + '30';
        langTag.textContent = repo.language;
        tagsContainer.appendChild(langTag);

        // 领域标签
        var domainTag = document.createElement('span');
        domainTag.className = 'px-2 py-0.5 rounded text-xs font-medium bg-synapse-border text-text-muted';
        domainTag.textContent = repo.domain;
        tagsContainer.appendChild(domainTag);

        // 评分标签
        var scoreTag = document.createElement('span');
        scoreTag.className = 'px-2 py-0.5 rounded text-xs font-medium bg-electric-cyan/10 text-electric-cyan border border-electric-cyan/20';
        scoreTag.textContent = repo.score + '/10';
        tagsContainer.appendChild(scoreTag);

        // Star 进度条
        var maxStars = 50000;
        try {{
            var starsNum = parseInt(repo.stars.replace(/,/g, ''));
            var pct = Math.min((starsNum / maxStars) * 100, 100);
            document.getElementById('detail-stars-bar').style.width = pct + '%';
        }} catch(e) {{
            document.getElementById('detail-stars-bar').style.width = '0%';
        }}

        // AI 总结
        var aiSection = document.getElementById('detail-ai-section');
        if (repo.aiSummary) {{
            aiSection.classList.remove('hidden');
            document.getElementById('detail-ai-summary').textContent = repo.aiSummary;

            var highlightsList = document.getElementById('detail-ai-highlights');
            highlightsList.innerHTML = '';
            if (repo.aiHighlights && repo.aiHighlights.length > 0) {{
                repo.aiHighlights.forEach(function(h) {{
                    var li = document.createElement('li');
                    li.className = 'flex items-start gap-2';
                    li.innerHTML = '<span class="text-electric-cyan mt-0.5">•</span><span>' + h + '</span>';
                    highlightsList.appendChild(li);
                }});
            }}

            if (repo.aiUseCases) {{
                document.getElementById('detail-ai-usecases').textContent = '适用场景: ' + repo.aiUseCases;
            }} else {{
                document.getElementById('detail-ai-usecases').textContent = '';
            }}
        }} else {{
            aiSection.classList.add('hidden');
        }}
    }}

    // 复制链接
    function copyToClipboard() {{
        if (currentRepoId && window.REPO_DATA[currentRepoId]) {{
            navigator.clipboard.writeText(window.REPO_DATA[currentRepoId].url);
            alert('Link copied!');
        }}
    }}

    // 筛选功能
    function filterByDomain(domain) {{
        document.querySelectorAll('.feed-item').forEach(function(item) {{
            if (domain === 'all') {{
                item.style.display = '';
            }} else if (domain === 'new') {{
                item.style.display = item.dataset.isNew === 'true' ? '' : 'none';
            }} else if (domain === 'rising') {{
                var change = parseInt(item.dataset.change) || 0;
                item.style.display = change > 0 ? '' : 'none';
            }} else {{
                item.style.display = item.dataset.domain === domain ? '' : 'none';
            }}
        }});
    }}

    // 搜索功能
    function filterBySearch(query) {{
        query = query.toLowerCase();
        document.querySelectorAll('.feed-item').forEach(function(item) {{
            var repoId = item.dataset.repoId.toLowerCase();
            item.style.display = repoId.includes(query) ? '' : 'none';
        }});
    }}

    // 侧边栏导航点击
    document.querySelectorAll('.nav-item, .nav-item-active').forEach(function(item) {{
        item.addEventListener('click', function(e) {{
            e.preventDefault();

            // 更新激活状态
            document.querySelectorAll('.nav-item, .nav-item-active').forEach(function(n) {{
                n.className = n.className.replace('nav-item-active', 'nav-item')
                    .replace('text-electric-cyan', 'text-text-muted');
            }});
            this.className = this.className.replace('nav-item', 'nav-item-active');

            // 筛选
            filterByDomain(this.dataset.filter);
        }});
    }});

    // 默认选中第一个
    document.addEventListener('DOMContentLoaded', function() {{
        var firstItem = document.querySelector('.feed-item');
        if (firstItem) {{
            selectRepo(firstItem.dataset.repoId);
        }}
    }});
    </script>
</body>
</html>
'''


def save_dashboard(html_content: str, base_dir: str = 'archives', date: datetime = None, lang: str = 'zh') -> str:
    """
    保存 HTML 仪表板
    """
    if date is None:
        date = datetime.now()

    # 创建目录结构
    dir_path = Path(base_dir) / date.strftime('%Y') / date.strftime('%m')
    dir_path.mkdir(parents=True, exist_ok=True)

    # 文件名
    suffix = '' if lang == 'zh' else f'_{lang}'
    file_path = dir_path / f'{date.strftime("%Y-%m-%d")}{suffix}.html'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 中文版同时保存到 index.html
    if lang == 'zh':
        index_path = Path(base_dir) / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    return str(file_path)
