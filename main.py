#!/usr/bin/env python3
"""GitHub Trending 每日推送 - 主入口"""

import sys
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import scrape_trending
from src.analyzer import analyze_repos
from src.generator import generate_markdown, save_report
from src.history import (
    RankingEntry, save_ranking_history, load_yesterday_rankings,
    calculate_rank_changes, format_rank_change
)
from src.dashboard import generate_dashboard_html, save_dashboard
from src.ai_summary import batch_generate_summaries
from src.rss import generate_rss, save_rss


def main():
    """主函数"""
    print('🚀 开始获取 GitHub Trending 数据...')

    # 1. 爬取 Trending 数据
    try:
        repos = scrape_trending()
        print(f'✅ 成功获取 {len(repos)} 个热门项目')
    except Exception as e:
        print(f'❌ 爬取失败: {e}')
        sys.exit(1)

    if not repos:
        print('⚠️ 未获取到任何项目，退出')
        sys.exit(0)

    # 2. 分析项目
    print('📊 正在分析项目...')
    analyses = analyze_repos(repos, fetch_details=False)
    print(f'✅ 分析完成，最高评分: {analyses[0].score}/10')

    today = datetime.now()
    base_dir = Path(__file__).parent / 'archives'

    # 3. 创建排名条目
    print('📈 正在计算排名变化...')
    current_entries = []
    for i, analysis in enumerate(analyses, 1):
        current_entries.append(RankingEntry(
            name=analysis.repo.name,
            rank=i,
            stars=analysis.repo.stars,
            stars_today=analysis.repo.stars_today,
            language=analysis.repo.language,
            description=analysis.repo.description
        ))

    # 4. 加载昨天数据并计算变化
    yesterday_entries = load_yesterday_rankings(str(base_dir), today)
    rank_changes = calculate_rank_changes(current_entries, yesterday_entries)

    # 统计新上榜项目
    new_count = sum(1 for c in rank_changes if c.is_new)
    if yesterday_entries:
        print(f'✅ 对比昨日数据完成: {new_count} 个新上榜项目')
    else:
        print('ℹ️ 未找到昨日数据，所有项目标记为新上榜')

    # 5. 保存今日排名历史
    history_path = save_ranking_history(current_entries, str(base_dir), today)
    print(f'✅ 排名数据已保存: {history_path}')

    # 6. 生成 AI 智能总结 (为 Top 10 项目生成)
    print('🤖 正在生成 AI 智能总结...')
    repos_for_ai = [
        {
            'name': a.repo.name,
            'description': a.repo.description,
            'language': a.repo.language,
            'stars': a.repo.stars,
            'stars_today': a.repo.stars_today,
            'topics': a.topics
        }
        for a in analyses[:10]
    ]
    ai_summaries = batch_generate_summaries(repos_for_ai, max_count=10)
    print(f'✅ AI 总结生成完成: {len(ai_summaries)} 个项目')

    # 7. 生成 Markdown 报告 (带排名变化)
    print('📝 正在生成 Markdown 报告...')
    markdown_content = generate_markdown_with_changes(analyses, rank_changes, today)
    md_path = save_report(markdown_content, base_dir=str(base_dir), date=today)
    print(f'✅ Markdown 报告已保存: {md_path}')

    # 8. 生成 HTML 仪表板 (中文版)
    print('🎨 正在生成 HTML 仪表板...')
    html_content_zh = generate_dashboard_html(analyses, rank_changes, today, lang='zh', ai_summaries=ai_summaries)
    html_path_zh = save_dashboard(html_content_zh, str(base_dir), today, lang='zh')
    print(f'✅ 中文版仪表板已保存: {html_path_zh}')

    # 9. 生成 HTML 仪表板 (英文版)
    html_content_en = generate_dashboard_html(analyses, rank_changes, today, lang='en', ai_summaries=ai_summaries)
    html_path_en = save_dashboard(html_content_en, str(base_dir), today, lang='en')
    print(f'✅ 英文版仪表板已保存: {html_path_en}')

    # 10. 生成 RSS Feed
    print('📡 正在生成 RSS Feed...')
    rss_content = generate_rss(analyses, today)
    rss_path = save_rss(rss_content, str(base_dir))
    print(f'✅ RSS Feed 已保存: {rss_path}')

    # 11. 输出摘要
    print('\n' + '=' * 50)
    print(f'📅 日期: {today.strftime("%Y-%m-%d")}')
    print(f'📊 收录项目: {len(repos)} 个')
    print(f'🆕 新上榜: {new_count} 个')
    print('\n🏆 Top 5 推荐:')
    for i, analysis in enumerate(analyses[:5], 1):
        change = next((c for c in rank_changes if c.name == analysis.repo.name), None)
        change_str = format_rank_change(change) if change else ''
        print(f'  {i}. {analysis.repo.name} (⭐ {analysis.score}/10) {change_str}')
    print('=' * 50)

    return 0


def generate_markdown_with_changes(analyses, rank_changes, date):
    """生成带排名变化的 Markdown 报告"""
    from src.generator import format_stars, score_to_stars, get_target_audience

    date_str = date.strftime('%Y-%m-%d')

    # 创建 name -> RankChange 映射
    change_map = {c.name: c for c in rank_changes}

    # 按评分排序
    sorted_analyses = sorted(analyses, key=lambda x: x.score, reverse=True)

    # 统计语言分布
    lang_count = {}
    for a in analyses:
        lang = a.repo.language or 'Other'
        lang_count[lang] = lang_count.get(lang, 0) + 1

    top_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:5]
    lang_summary = ' | '.join(f'{lang}: {count}' for lang, count in top_langs)

    # 统计新上榜
    new_count = sum(1 for c in rank_changes if c.is_new)

    lines = [
        f'# GitHub Trending 每日精选 ({date_str})',
        '',
        f'> 🔥 今日共收录 **{len(analyses)}** 个热门项目 | 🆕 新上榜 **{new_count}** 个',
        f'>',
        f'> 📊 语言分布: {lang_summary}',
        '',
        '---',
        '',
    ]

    # 新上榜项目 Banner
    new_projects = [(a, change_map.get(a.repo.name)) for a in sorted_analyses
                    if change_map.get(a.repo.name) and change_map.get(a.repo.name).is_new]

    if new_projects:
        lines.extend([
            '## 🆕 今日新上榜',
            '',
        ])
        for analysis, change in new_projects[:5]:
            repo = analysis.repo
            desc = repo.description[:60] + '...' if len(repo.description) > 60 else repo.description
            lines.append(f'- **[{repo.name}]({repo.url})** - {desc} ⭐ {format_stars(repo.stars)} (+{repo.stars_today})')
        lines.extend(['', '---', ''])

    # Top 3 推荐
    lines.extend([
        '## 🏆 今日重点推荐',
        '',
    ])

    medals = ['🥇', '🥈', '🥉']
    for i, analysis in enumerate(sorted_analyses[:3]):
        repo = analysis.repo
        change = change_map.get(repo.name)
        change_str = format_rank_change(change) if change else ''

        # 格式化语言
        if analysis.language_stats:
            lang_parts = [f'{lang} {pct:.0f}%' for lang, pct in list(analysis.language_stats.items())[:3]]
            lang_display = ', '.join(lang_parts)
        elif repo.language:
            lang_display = f'{repo.language} 100%'
        else:
            lang_display = '未知'

        star_display = score_to_stars(analysis.score)
        audience = get_target_audience(analysis)

        lines.extend([
            f'### {medals[i]} [{repo.name}]({repo.url})',
            f'> {analysis.readme_summary}' if analysis.readme_summary else '',
            '',
            '| 指标 | 数值 |',
            '|------|------|',
            f'| ⭐ Star | {format_stars(repo.stars)} |',
            f'| 📈 今日新增 | +{repo.stars_today} |',
            f'| 📊 排名变化 | {change_str} |',
            f'| 🔧 主要语言 | {lang_display} |',
            f'| 📊 推荐指数 | {star_display} ({analysis.score}/10) |',
            '',
            f'**核心功能**: {analysis.readme_summary[:100]}' if analysis.readme_summary else '',
            f'**技术栈**: {", ".join(analysis.tech_stack) if analysis.tech_stack else lang_display}',
            f'**适合人群**: {audience}',
            '',
            '---',
            '',
        ])

    # 完整列表
    lines.extend([
        '## 📋 完整列表',
        '',
        '| # | 项目 | 语言 | Star | 今日 | 变化 | 评分 |',
        '|---|------|------|------|------|------|------|',
    ])

    for i, analysis in enumerate(sorted_analyses, 1):
        repo = analysis.repo
        change = change_map.get(repo.name)
        change_str = format_rank_change(change) if change else '-'
        lang = repo.language or '未知'
        lines.append(f'| {i} | [{repo.name}]({repo.url}) | {lang} | {format_stars(repo.stars)} | +{repo.stars_today} | {change_str} | {analysis.score}/10 |')

    lines.extend([
        '',
        '---',
        '',
        f'📅 更新时间: {date.strftime("%Y-%m-%d %H:%M:%S")}',
        '',
        '> 本报告由 [GitHub Trending Daily](https://github.com) 自动生成',
    ])

    return '\n'.join(line for line in lines if line is not None)


if __name__ == '__main__':
    sys.exit(main())
