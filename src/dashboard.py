"""HTML 仪表板生成器 - 类似 OpenStock 风格，支持中英文双语"""

from datetime import datetime
from pathlib import Path
from .analyzer import RepoAnalysis
from .history import RankChange, format_rank_change

# 多语言文本配置
LANG_TEXTS = {
    'zh': {
        'title': 'GitHub Trending 每日热榜',
        'subtitle': '每日热门项目追踪',
        'date_prefix': '📅',
        'project_count': '个项目',
        'new_today': '🔥 今日新上榜',
        'data_source': '数据来源',
        'update_time': '更新时间',
        'today_suffix': '今日',
        'unknown': '未知',
    },
    'en': {
        'title': 'GitHub Trending Dashboard',
        'subtitle': 'Daily Hot Projects Tracker',
        'date_prefix': '📅',
        'project_count': 'projects',
        'new_today': '🔥 New Today',
        'data_source': 'Data Source',
        'update_time': 'Updated',
        'today_suffix': 'today',
        'unknown': 'Unknown',
    }
}


def get_heat_color(score: int, stars_today: int) -> str:
    """
    根据评分和今日新增 Star 计算热力颜色

    Returns:
        CSS 渐变背景
    """
    # 基于评分和今日增长计算热度
    try:
        today_num = int(str(stars_today).replace(',', '').replace(',', ''))
    except (ValueError, TypeError):
        today_num = 0

    # 热度计算: 评分 * 0.3 + 今日增长热度 * 0.7 (增长权重更高)
    growth_heat = min(today_num / 500, 1.0)  # 500+ stars today = max heat
    score_heat = score / 10

    heat = score_heat * 0.3 + growth_heat * 0.7

    # 颜色映射: 使用渐变使方块更有质感
    # 从深蓝(冷) -> 青色 -> 绿色 -> 黄色 -> 橙色 -> 红色(热)
    if heat >= 0.85:
        # 深红 - 最热
        return "linear-gradient(135deg, hsl(0, 80%, 50%) 0%, hsl(0, 85%, 40%) 100%)"
    elif heat >= 0.7:
        # 红色
        return "linear-gradient(135deg, hsl(10, 85%, 55%) 0%, hsl(5, 80%, 45%) 100%)"
    elif heat >= 0.55:
        # 橙色
        return "linear-gradient(135deg, hsl(25, 90%, 55%) 0%, hsl(20, 85%, 45%) 100%)"
    elif heat >= 0.4:
        # 黄橙
        return "linear-gradient(135deg, hsl(40, 95%, 55%) 0%, hsl(35, 90%, 45%) 100%)"
    elif heat >= 0.25:
        # 绿色
        return "linear-gradient(135deg, hsl(120, 55%, 50%) 0%, hsl(130, 50%, 40%) 100%)"
    elif heat >= 0.1:
        # 青绿
        return "linear-gradient(135deg, hsl(170, 55%, 45%) 0%, hsl(180, 50%, 38%) 100%)"
    else:
        # 蓝色 - 最冷
        return "linear-gradient(135deg, hsl(210, 55%, 55%) 0%, hsl(220, 50%, 45%) 100%)"


def format_stars_display(stars_str: str) -> str:
    """格式化 Star 数显示"""
    try:
        num = int(str(stars_str).replace(',', '').replace(',', ''))
        if num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)
    except (ValueError, TypeError):
        return stars_str


def generate_project_card(analysis: RepoAnalysis, rank: int, rank_change: RankChange = None,
                          lang: str = 'zh', ai_summary = None) -> str:
    """生成单个项目卡片 HTML"""
    texts = LANG_TEXTS.get(lang, LANG_TEXTS['zh'])
    repo = analysis.repo
    heat_color = get_heat_color(analysis.score, repo.stars_today)
    change_text = format_rank_change(rank_change) if rank_change else "-"
    is_new = rank_change.is_new if rank_change else False

    # 语言颜色映射
    lang_colors = {
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
    }
    lang_color = lang_colors.get(repo.language, '#6e7681')

    # 截断描述
    desc = repo.description[:80] + '...' if len(repo.description) > 80 else repo.description
    desc = desc.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

    new_badge = '<span class="new-badge">NEW</span>' if is_new else ''
    change_class = 'up' if rank_change and rank_change.change and rank_change.change > 0 else \
                   'down' if rank_change and rank_change.change and rank_change.change < 0 else ''

    # AI 总结区域 - 直接展示内容
    ai_section = ''
    if ai_summary:
        highlights_html = ''.join(f'<li>{h}</li>' for h in ai_summary.highlights) if ai_summary.highlights else ''
        ai_section = f'''
        <div class="ai-summary">
            <p class="ai-desc">✨ {ai_summary.summary}</p>
            <ul class="ai-highlights">{highlights_html}</ul>
            <p class="ai-use-cases"><strong>{'适用场景' if lang == 'zh' else 'Use Cases'}:</strong> {ai_summary.use_cases}</p>
        </div>
        '''

    # 贡献者头像
    contributors_html = ''
    if hasattr(repo, 'contributors') and repo.contributors:
        avatars = ''.join([
            f'<img src="{c.avatar_url}" alt="{c.username}" title="{c.username}" class="contributor-avatar">'
            for c in repo.contributors[:3]
        ])
        contributors_html = f'<div class="contributors">{avatars}</div>'

    return f'''
    <a href="{repo.url}" target="_blank" class="project-card {'new-project' if is_new else ''} {'has-ai' if ai_summary else ''}" style="--heat-color: {heat_color}">
        <div class="card-header">
            <span class="rank">#{rank}</span>
            <span class="change {change_class}">{change_text}</span>
            {new_badge}
        </div>
        <div class="card-body">
            <h3 class="project-name">{repo.name.split('/')[-1]}</h3>
            <p class="project-author">@{repo.name.split('/')[0]}</p>
            <p class="project-desc">{desc}</p>
            {ai_section}
        </div>
        <div class="card-footer">
            <div class="stats">
                <span class="stars">⭐ {format_stars_display(repo.stars)}</span>
                <span class="today">+{repo.stars_today}</span>
            </div>
            <div class="meta">
                <span class="language" style="--lang-color: {lang_color}">{repo.language or texts['unknown']}</span>
                {contributors_html}
                <span class="score">{analysis.score}/10</span>
            </div>
        </div>
    </a>
    '''


def squarify_treemap(values: list[dict], x: float, y: float, width: float, height: float) -> list[dict]:
    """
    Squarified Treemap 算法 - 生成尽可能接近正方形的矩形布局

    Args:
        values: 包含 value 和其他属性的字典列表，需按 value 降序排列
        x, y: 起始位置
        width, height: 可用空间

    Returns:
        带有 x, y, w, h 布局信息的字典列表
    """
    if not values:
        return []

    # 复制列表避免修改原数据
    items = [v.copy() for v in values]

    # 计算总值和比例
    total = sum(item['value'] for item in items)
    if total == 0:
        return items

    # 归一化：将值转换为面积
    area = width * height
    for item in items:
        item['area'] = (item['value'] / total) * area

    result = []

    def worst_ratio(row: list[dict], w: float) -> float:
        """计算一行中最差的长宽比"""
        if not row or w == 0:
            return float('inf')
        s = sum(r['area'] for r in row)
        if s == 0:
            return float('inf')
        rmax = max(r['area'] for r in row)
        rmin = min(r['area'] for r in row)
        return max((w * w * rmax) / (s * s), (s * s) / (w * w * rmin))

    def layout_row(row: list[dict], x: float, y: float, w: float, h: float, vertical: bool):
        """布局一行元素"""
        s = sum(r['area'] for r in row)
        if vertical:
            row_h = s / w if w > 0 else 0
            cx = x
            for r in row:
                r_w = r['area'] / row_h if row_h > 0 else 0
                r['x'] = cx
                r['y'] = y
                r['w'] = r_w
                r['h'] = row_h
                result.append(r)
                cx += r_w
            return x, y + row_h, w, h - row_h
        else:
            row_w = s / h if h > 0 else 0
            cy = y
            for r in row:
                r_h = r['area'] / row_w if row_w > 0 else 0
                r['x'] = x
                r['y'] = cy
                r['w'] = row_w
                r['h'] = r_h
                result.append(r)
                cy += r_h
            return x + row_w, y, w - row_w, h

    def squarify(items: list[dict], x: float, y: float, w: float, h: float):
        if not items:
            return

        if len(items) == 1:
            items[0]['x'] = x
            items[0]['y'] = y
            items[0]['w'] = w
            items[0]['h'] = h
            result.append(items[0])
            return

        vertical = w >= h
        short_side = h if vertical else w

        row = []
        remaining = items.copy()

        while remaining:
            item = remaining[0]
            new_row = row + [item]

            if not row or worst_ratio(new_row, short_side) <= worst_ratio(row, short_side):
                row = new_row
                remaining = remaining[1:]
            else:
                # 布局当前行，递归处理剩余
                x, y, w, h = layout_row(row, x, y, w, h, vertical)
                squarify(remaining, x, y, w, h)
                return

        # 布局最后一行
        if row:
            layout_row(row, x, y, w, h, vertical)

    squarify(items, x, y, width, height)
    return result


def generate_heatmap_section(analyses: list[RepoAnalysis], lang: str = 'zh') -> str:
    """
    生成 Repo Heatmap 区域 - 使用 ECharts Treemap 实现类似 TradingView 的专业热力图

    每个方块显示:
    - repo name
    - 新增 star 数
    """
    import json
    import math

    if not analyses:
        return ''

    # 按 stars_today 排序，取前 12 个
    sorted_repos = sorted(analyses, key=lambda x: int(str(x.repo.stars_today).replace(',', '') or '0'), reverse=True)[:12]

    # 准备 ECharts 数据
    treemap_data = []
    max_stars_today = 0

    for analysis in sorted_repos:
        repo = analysis.repo
        try:
            stars_today = int(str(repo.stars_today).replace(',', ''))
            total_stars = int(str(repo.stars).replace(',', ''))
        except (ValueError, TypeError):
            stars_today = 0
            total_stars = 1

        if stars_today > max_stars_today:
            max_stars_today = stars_today

        # 使用 stars_today 直接计算面积，保留大小差异（类似 TradingView 风格）
        # 使用平方根变换而非对数，保持更明显的大小差异
        area_value = (stars_today ** 0.7) + 1

        # 获取 GitHub 头像 URL (owner 头像)
        owner = repo.name.split('/')[0] if '/' in repo.name else repo.name
        avatar_url = f'https://github.com/{owner}.png?size=200'

        treemap_data.append({
            'name': repo.name.split('/')[-1],
            'fullName': repo.name,
            'value': area_value,
            'starsToday': stars_today,
            'totalStars': total_stars,
            'url': repo.url,
            'language': repo.language or 'Unknown',
            'avatarUrl': avatar_url,
            'owner': owner
        })

    # 转换为 JSON
    data_json = json.dumps(treemap_data, ensure_ascii=False)

    heatmap_title = 'Trending Heatmap' if lang == 'en' else '热力图'
    tooltip_stars = 'Stars Today' if lang == 'en' else '今日新增'
    tooltip_total = 'Total Stars' if lang == 'en' else '总 Star'
    tooltip_lang = 'Language' if lang == 'en' else '语言'

    return f'''
    <section class="heatmap-section">
        <h2>🔥 {heatmap_title}</h2>
        <div id="treemap-wrapper" style="width: 100%; height: 400px; border-radius: 12px; overflow: hidden; position: relative;">
            <div id="treemap-chart" style="width: 100%; height: 100%;"></div>
        </div>
        <script>
        (function() {{
            var chartDom = document.getElementById('treemap-chart');
            var myChart = echarts.init(chartDom);

            var rawData = {data_json};
            var maxStars = Math.max(...rawData.map(d => d.starsToday));

            // 30 个经典配色（参考 GitHub 语言颜色、Material Design 等）
            var classicColors = [
                '#3572A5',  // Python 蓝
                '#f1e05a',  // JavaScript 黄
                '#e34c26',  // HTML 橙红
                '#563d7c',  // CSS 紫
                '#b07219',  // Java 棕
                '#00ADD8',  // Go 青
                '#dea584',  // Rust 肉色
                '#178600',  // C# 绿
                '#f34b7d',  // C++ 粉
                '#438eff',  // TypeScript 蓝
                '#701516',  // Ruby 暗红
                '#4F5D95',  // PHP 紫蓝
                '#DA5B0B',  // Jupyter 橙
                '#89e051',  // Shell 亮绿
                '#c22d40',  // Scala 红
                '#12aa51',  // Vue 翠绿
                '#ff6f00',  // 琥珀色
                '#00bcd4',  // 青色
                '#9c27b0',  // 紫色
                '#e91e63',  // 粉红
                '#3f51b5',  // 靛蓝
                '#009688',  // 青绿
                '#795548',  // 棕色
                '#607d8b',  // 蓝灰
                '#ff5722',  // 深橙
                '#8bc34a',  // 浅绿
                '#ffc107',  // 琥珀
                '#03a9f4',  // 浅蓝
                '#673ab7',  // 深紫
                '#cddc39'   // 黄绿
            ];

            // 基于项目名生成稳定的颜色索引（同一项目每次颜色一致）
            function hashCode(str) {{
                var hash = 0;
                for (var i = 0; i < str.length; i++) {{
                    hash = ((hash << 5) - hash) + str.charCodeAt(i);
                    hash = hash & hash;
                }}
                return Math.abs(hash);
            }}

            function getItemColor(starsToday, index, total, name) {{
                // 使用项目名的哈希值选择颜色，确保同一项目颜色稳定
                var colorIndex = hashCode(name) % classicColors.length;
                return classicColors[colorIndex];
            }}

            var treeData = rawData.map(function(item, index) {{
                return {{
                    name: item.name,
                    value: item.value,
                    starsToday: item.starsToday,
                    totalStars: item.totalStars,
                    url: item.url,
                    fullName: item.fullName,
                    language: item.language,
                    avatarUrl: item.avatarUrl,
                    owner: item.owner,
                    itemStyle: {{
                        color: getItemColor(item.starsToday, index, rawData.length, item.name),
                        borderColor: 'rgba(0,0,0,0.2)',
                        borderWidth: 1
                    }}
                }};
            }});

            var option = {{
                tooltip: {{
                    backgroundColor: 'rgba(0,0,0,0.85)',
                    borderColor: '#333',
                    textStyle: {{ color: '#fff', fontSize: 13 }},
                    formatter: function(params) {{
                        var d = params.data;
                        var starsDisplay = d.starsToday >= 1000 ? (d.starsToday/1000).toFixed(1) + 'k' : d.starsToday;
                        var totalDisplay = d.totalStars >= 1000 ? (d.totalStars/1000).toFixed(1) + 'k' : d.totalStars;
                        return '<div style="font-weight:600;margin-bottom:8px;font-size:14px;">' + d.fullName + '</div>' +
                               '<div style="margin:4px 0;">⭐ {tooltip_stars}: <span style="color:#f39c12;font-weight:600;">+' + starsDisplay + '</span></div>' +
                               '<div style="margin:4px 0;">📊 {tooltip_total}: ' + totalDisplay + '</div>' +
                               '<div>🔧 {tooltip_lang}: ' + d.language + '</div>';
                    }}
                }},
                series: [{{
                    type: 'treemap',
                    width: '100%',
                    height: '100%',
                    roam: false,
                    nodeClick: false,
                    breadcrumb: {{ show: false }},
                    itemStyle: {{ borderRadius: 4, gapWidth: 2 }},
                    label: {{
                        show: true,
                        position: 'inside',
                        formatter: function(params) {{
                            var d = params.data;
                            var starsDisplay = d.starsToday >= 1000 ? '+' + (d.starsToday/1000).toFixed(1) + 'k' : '+' + d.starsToday;
                            return d.name + '\\n' + starsDisplay;
                        }},
                        fontSize: 16,
                        fontWeight: 700,
                        color: '#fff',
                        textShadowColor: 'rgba(0,0,0,0.8)',
                        textShadowBlur: 6,
                        textShadowOffsetX: 1,
                        textShadowOffsetY: 1,
                        lineHeight: 24,
                        textBorderColor: 'rgba(0,0,0,0.5)',
                        textBorderWidth: 2
                    }},
                    upperLabel: {{
                        show: false
                    }},
                    data: treeData
                }}]
            }};

            myChart.setOption(option);

            myChart.on('click', function(params) {{
                if (params.data && params.data.url) window.open(params.data.url, '_blank');
            }});

            window.addEventListener('resize', function() {{
                myChart.resize();
            }});
        }})();
        </script>
    </section>
    '''


def generate_banner_section(new_projects: list[tuple[RepoAnalysis, RankChange]], lang: str = 'zh',
                            ai_summaries: dict = None) -> str:
    """生成新项目 Banner 区域 - 使用与项目卡片相同的样式"""
    texts = LANG_TEXTS.get(lang, LANG_TEXTS['zh'])

    if not new_projects:
        return ''

    if ai_summaries is None:
        ai_summaries = {}

    cards = []
    for i, (analysis, change) in enumerate(new_projects[:3], 1):  # 最多显示3个新项目
        ai_summary = ai_summaries.get(analysis.repo.name)
        card_html = generate_project_card(analysis, i, change, lang, ai_summary)
        cards.append(card_html)

    return f'''
    <section class="banner-section">
        <h2>{texts['new_today']}</h2>
        <div class="banner-container">
            {''.join(cards)}
        </div>
    </section>
    '''


def generate_dashboard_html(analyses: list[RepoAnalysis],
                            rank_changes: list[RankChange],
                            date: datetime = None,
                            lang: str = 'zh',
                            ai_summaries: dict = None) -> str:
    """
    生成完整的 HTML 仪表板

    Args:
        analyses: 分析结果列表
        rank_changes: 排名变化列表
        date: 报告日期
        lang: 语言 ('zh' 中文, 'en' 英文)
        ai_summaries: AI 生成的项目总结字典 {repo_name: AISummary}

    Returns:
        HTML 字符串
    """
    texts = LANG_TEXTS.get(lang, LANG_TEXTS['zh'])
    html_lang = 'zh-CN' if lang == 'zh' else 'en'

    if date is None:
        date = datetime.now()

    if ai_summaries is None:
        ai_summaries = {}

    date_str = date.strftime('%Y-%m-%d')

    # 创建 name -> RankChange 映射
    change_map = {c.name: c for c in rank_changes}

    # 按评分排序
    sorted_analyses = sorted(analyses, key=lambda x: x.score, reverse=True)[:25]

    # 找出新上榜项目
    new_projects = []
    for i, analysis in enumerate(sorted_analyses, 1):
        change = change_map.get(analysis.repo.name)
        if change and change.is_new:
            new_projects.append((analysis, change))

    # 生成 Banner
    banner_html = generate_banner_section(new_projects, lang, ai_summaries)

    # 生成 Heatmap
    heatmap_html = generate_heatmap_section(sorted_analyses, lang)

    # 生成所有项目卡片
    cards_html = []
    for i, analysis in enumerate(sorted_analyses, 1):
        change = change_map.get(analysis.repo.name)
        ai_summary = ai_summaries.get(analysis.repo.name)
        cards_html.append(generate_project_card(analysis, i, change, lang, ai_summary))

    # 统计语言分布
    lang_count = {}
    for a in sorted_analyses:
        lang = a.repo.language or 'Other'
        lang_count[lang] = lang_count.get(lang, 0) + 1

    top_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:6]

    lang_stats_html = ''.join([
        f'<span class="lang-stat"><span class="lang-dot" style="background: {get_lang_color(prog_lang)}"></span>{prog_lang}: {count}</span>'
        for prog_lang, count in top_langs
    ])

    # 项目数量显示
    project_count_text = f"{len(sorted_analyses)} {texts['project_count']}"

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{texts['title']} - {date_str}</title>
    <link rel="icon" href="https://github.githubassets.com/favicons/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="https://github.githubassets.com/favicons/favicon-dark.png" type="image/png" media="(prefers-color-scheme: dark)">
    <link rel="icon" href="https://github.githubassets.com/favicons/favicon.png" type="image/png" media="(prefers-color-scheme: light)">
    <link rel="apple-touch-icon" href="https://github.githubassets.com/apple-touch-icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        /* 深色主题 (默认) */
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --border-color: #3d444d;
            --accent-green: #3fb950;
            --accent-red: #f85149;
            --accent-blue: #58a6ff;
            --accent-yellow: #d29922;
            --card-shadow: rgba(0, 0, 0, 0.4);
            --banner-bg: #3d2e00;
            --banner-border: #9e6a03;
        }}

        /* 浅色主题 */
        [data-theme="light"] {{
            --bg-primary: #ffffff;
            --bg-secondary: #f6f8fa;
            --bg-tertiary: #e1e4e8;
            --text-primary: #24292f;
            --text-secondary: #57606a;
            --text-muted: #6e7781;
            --border-color: #d1d9e0;
            --accent-green: #1a7f37;
            --accent-red: #cf222e;
            --accent-blue: #0969da;
            --accent-yellow: #9a6700;
            --card-shadow: rgba(0, 0, 0, 0.1);
            --banner-bg: #fff8c5;
            --banner-border: #9a6700;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.5;
            transition: background 0.3s ease, color 0.3s ease;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* 主题切换按钮 */
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 0.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
        }}

        .theme-toggle:hover {{
            border-color: var(--accent-blue);
        }}

        .theme-toggle .icon {{
            font-size: 1.2rem;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }}

        .theme-toggle .icon.active {{
            background: var(--accent-blue);
            color: white;
        }}

        header {{
            margin-bottom: 2rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
        }}

        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.5rem;
        }}

        .header-title {{
            text-align: left;
        }}

        .header-actions {{
            display: flex;
            gap: 0.5rem;
        }}

        .subscribe-btn {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--accent-yellow);
            color: #000;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .subscribe-btn:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        header .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}

        header .date {{
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}

        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}

        .lang-stat {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}

        .lang-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}

        /* Heatmap Section - ECharts */
        .heatmap-section {{
            margin-bottom: 2rem;
        }}

        .heatmap-section h2 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        #treemap-chart {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
        }}

        /* Banner Section */
        .banner-section {{
            margin-bottom: 2rem;
        }}

        .banner-section h2 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .banner-container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }}

        /* Project Grid */
        .project-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }}

        .project-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}

        .project-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--heat-color);
        }}

        .project-card:hover {{
            transform: translateY(-2px);
            border-color: var(--heat-color);
            box-shadow: 0 8px 24px var(--card-shadow);
        }}

        .project-card.new-project {{
            border-color: var(--accent-yellow);
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}

        .rank {{
            font-weight: 700;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        .change {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            background: var(--bg-tertiary);
        }}

        .change.up {{
            color: var(--accent-green);
            background: rgba(63, 185, 80, 0.15);
        }}

        .change.down {{
            color: var(--accent-red);
            background: rgba(248, 81, 73, 0.15);
        }}

        .new-badge {{
            background: var(--accent-yellow);
            color: #fff;
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            margin-left: auto;
        }}

        [data-theme="light"] .new-badge {{
            color: #000;
        }}

        .card-body {{
            flex: 1;
        }}

        .project-name {{
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .project-author {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }}

        .project-desc {{
            color: var(--text-secondary);
            font-size: 0.8rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 2.4rem;
        }}

        /* AI Summary Styles */
        .ai-summary {{
            margin-top: 0.75rem;
            padding: 0.5rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
        }}

        .ai-desc {{
            font-size: 0.8rem;
            color: var(--text-primary);
            line-height: 1.4;
            margin-bottom: 0.5rem;
        }}

        .ai-highlights {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            padding-left: 1rem;
            margin: 0.5rem 0;
        }}

        .ai-highlights li {{
            margin-bottom: 0.25rem;
        }}

        .ai-use-cases {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin: 0;
        }}

        .project-card.has-ai {{
            border-color: var(--accent-yellow);
            border-width: 1px;
            border-style: solid;
        }}

        .card-footer {{
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border-color);
        }}

        .stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }}

        .stars {{
            color: var(--accent-yellow);
            font-weight: 500;
            font-size: 0.85rem;
        }}

        .today {{
            color: var(--accent-green);
            font-size: 0.8rem;
            font-weight: 500;
        }}

        .meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .language {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .language::before {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--lang-color);
        }}

        .score {{
            font-size: 0.75rem;
            color: var(--text-muted);
            background: var(--bg-tertiary);
            padding: 0.15rem 0.5rem;
            border-radius: 10px;
        }}

        .contributors {{
            display: flex;
            align-items: center;
        }}

        .contributor-avatar {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid var(--bg-secondary);
            margin-left: -6px;
        }}

        .contributor-avatar:first-child {{
            margin-left: 0;
        }}

        footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        footer a {{
            color: var(--accent-blue);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        /* Modal Styles */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }}

        .modal-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            max-width: 400px;
            width: 90%;
            position: relative;
            text-align: center;
        }}

        .modal-close {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--text-muted);
            cursor: pointer;
        }}

        .modal-close:hover {{
            color: var(--text-primary);
        }}

        .modal-content h3 {{
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }}

        .modal-desc {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }}

        #subscribeForm {{
            display: flex;
            gap: 0.5rem;
        }}

        #subscribeEmail {{
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 0.9rem;
        }}

        #subscribeEmail:focus {{
            outline: none;
            border-color: var(--accent-blue);
        }}

        .submit-btn {{
            padding: 0.75rem 1.5rem;
            background: var(--accent-green);
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        .submit-btn:hover {{
            opacity: 0.9;
        }}

        .modal-note {{
            margin-top: 1rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            header h1 {{
                font-size: 1.75rem;
            }}

            .project-grid {{
                grid-template-columns: 1fr;
            }}

            .stats-bar {{
                gap: 1rem;
            }}

            .theme-toggle {{
                top: 0.5rem;
                right: 0.5rem;
                padding: 0.3rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- 主题切换按钮 -->
    <div class="theme-toggle" onclick="toggleTheme()" title="切换主题 / Toggle Theme">
        <span class="icon active" id="darkIcon">🌙</span>
        <span class="icon" id="lightIcon">☀️</span>
    </div>

    <div class="container">
        <header>
            <div class="header-top">
                <div class="header-title">
                    <h1>{texts['title']}</h1>
                    <p class="subtitle">{texts['subtitle']}</p>
                </div>
                <div class="header-actions">
                    <button class="subscribe-btn" onclick="document.getElementById('subscribeModal').style.display='flex'" title="{'邮件订阅' if lang == 'zh' else 'Subscribe'}">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                        </svg>
                        {'邮件订阅' if lang == 'zh' else 'Subscribe'}
                    </button>
                </div>
            </div>
            <p class="date">{texts['date_prefix']} {date_str} · {project_count_text}</p>
            <div class="stats-bar">
                {lang_stats_html}
            </div>
        </header>

        {banner_html}

        {heatmap_html}

        <section class="project-section">
            <div class="project-grid">
                {''.join(cards_html)}
            </div>
        </section>

        <footer>
            <p>{texts['data_source']}: <a href="https://github.com/trending" target="_blank">GitHub Trending</a></p>
            <p>{texts['update_time']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>

    <!-- 订阅弹窗 -->
    <div id="subscribeModal" class="modal" onclick="if(event.target===this)this.style.display='none'">
        <div class="modal-content">
            <button class="modal-close" onclick="document.getElementById('subscribeModal').style.display='none'">&times;</button>
            <h3>{'📧 订阅每日热榜' if lang == 'zh' else '📧 Subscribe to Daily Digest'}</h3>
            <p class="modal-desc">{'每天早上 9 点，将 GitHub 热门项目推送到您的邮箱' if lang == 'zh' else 'Get daily GitHub trending projects delivered to your inbox at 9 AM'}</p>
            <form id="subscribeForm" onsubmit="handleSubscribe(event)">
                <input type="email" id="subscribeEmail" placeholder="{'请输入邮箱地址' if lang == 'zh' else 'Enter your email'}" required>
                <button type="submit" class="submit-btn">{'订阅' if lang == 'zh' else 'Subscribe'}</button>
            </form>
            <p class="modal-note">{'* 您可以随时取消订阅' if lang == 'zh' else '* You can unsubscribe at any time'}</p>
        </div>
    </div>

    <script>
        // 主题切换逻辑
        function toggleTheme() {{
            const html = document.documentElement;
            const darkIcon = document.getElementById('darkIcon');
            const lightIcon = document.getElementById('lightIcon');

            if (html.getAttribute('data-theme') === 'light') {{
                html.removeAttribute('data-theme');
                darkIcon.classList.add('active');
                lightIcon.classList.remove('active');
                localStorage.setItem('theme', 'dark');
            }} else {{
                html.setAttribute('data-theme', 'light');
                darkIcon.classList.remove('active');
                lightIcon.classList.add('active');
                localStorage.setItem('theme', 'light');
            }}
        }}

        // 加载保存的主题
        (function() {{
            const savedTheme = localStorage.getItem('theme');
            const darkIcon = document.getElementById('darkIcon');
            const lightIcon = document.getElementById('lightIcon');

            if (savedTheme === 'light') {{
                document.documentElement.setAttribute('data-theme', 'light');
                darkIcon.classList.remove('active');
                lightIcon.classList.add('active');
            }}
        }})();
    </script>
</body>
</html>
'''


def get_lang_color(lang: str) -> str:
    """获取语言对应的颜色"""
    colors = {
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
        'Other': '#6e7681',
    }
    return colors.get(lang, '#6e7681')


def save_dashboard(html_content: str, base_dir: str = 'archives', date: datetime = None, lang: str = 'zh') -> str:
    """
    保存 HTML 仪表板

    Args:
        html_content: HTML 内容
        base_dir: 存档基础目录
        date: 报告日期
        lang: 语言 ('zh' 中文, 'en' 英文)

    Returns:
        保存的文件路径
    """
    if date is None:
        date = datetime.now()

    # 创建目录结构
    dir_path = Path(base_dir) / date.strftime('%Y') / date.strftime('%m')
    dir_path.mkdir(parents=True, exist_ok=True)

    # 文件名: 2026-01-30.html (中文) 或 2026-01-30_en.html (英文)
    suffix = '' if lang == 'zh' else f'_{lang}'
    file_path = dir_path / f'{date.strftime("%Y-%m-%d")}{suffix}.html'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 中文版同时保存一份到根目录作为 index.html
    if lang == 'zh':
        index_path = Path(base_dir) / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    return str(file_path)
