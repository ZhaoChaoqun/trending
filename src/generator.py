"""Markdown 报告生成器"""

from datetime import datetime
from pathlib import Path
from .analyzer import RepoAnalysis


def format_stars(stars_str: str) -> str:
    """格式化 Star 数显示"""
    try:
        num = int(stars_str.replace(',', '').replace(',', ''))
        if num >= 1000:
            return f'{num / 1000:.1f}k'
        return str(num)
    except (ValueError, AttributeError):
        return stars_str


def score_to_stars(score: int) -> str:
    """将评分转换为星星显示"""
    full_stars = score // 2
    half_star = score % 2
    empty_stars = 5 - full_stars - half_star

    result = '⭐' * full_stars
    if half_star:
        result += '⭐'  # 简化处理，半星也用满星
        empty_stars = 5 - full_stars - 1
    result += '☆' * empty_stars

    return result


def get_target_audience(analysis: RepoAnalysis) -> str:
    """根据技术栈推断适合人群"""
    tech_stack = [t.lower() for t in analysis.tech_stack]
    language = analysis.repo.language.lower() if analysis.repo.language else ''

    audiences = []

    # 前端
    frontend_techs = {'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxt', 'typescript', 'javascript'}
    if any(t in frontend_techs for t in tech_stack) or language in frontend_techs:
        audiences.append('前端开发者')

    # 后端
    backend_techs = {'django', 'flask', 'fastapi', 'express', 'nestjs', 'spring', 'go', 'rust', 'java'}
    if any(t in backend_techs for t in tech_stack) or language in backend_techs:
        audiences.append('后端开发者')

    # AI/ML
    ai_techs = {'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'machine-learning', 'deep-learning', 'llm', 'ai'}
    if any(t in ai_techs for t in tech_stack + analysis.topics):
        audiences.append('AI/ML 工程师')

    # DevOps
    devops_techs = {'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'terraform', 'devops'}
    if any(t in devops_techs for t in tech_stack):
        audiences.append('DevOps 工程师')

    # 移动端
    mobile_techs = {'swift', 'kotlin', 'flutter', 'react-native', 'ios', 'android'}
    if any(t in mobile_techs for t in tech_stack) or language in mobile_techs:
        audiences.append('移动开发者')

    # Python
    if language == 'python' and not audiences:
        audiences.append('Python 开发者')

    if not audiences:
        audiences.append('软件开发者')

    return '、'.join(audiences[:3])


def generate_repo_section(analysis: RepoAnalysis, rank: int = 0) -> str:
    """生成单个仓库的 Markdown 内容"""
    repo = analysis.repo

    # 格式化语言占比
    if analysis.language_stats:
        lang_parts = [f'{lang} {pct:.0f}%' for lang, pct in list(analysis.language_stats.items())[:3]]
        lang_display = ', '.join(lang_parts)
    elif repo.language:
        lang_display = repo.language
    else:
        lang_display = '未知'

    # 格式化技术栈
    tech_stack_display = ', '.join(analysis.tech_stack) if analysis.tech_stack else lang_display

    # 推荐星级
    star_display = score_to_stars(analysis.score)

    # 适合人群
    audience = get_target_audience(analysis)

    # 生成 Markdown
    lines = [
        f'### {"🥇 " if rank == 1 else "🥈 " if rank == 2 else "🥉 " if rank == 3 else ""}[{repo.name}]({repo.url})',
        f'> {analysis.readme_summary}' if analysis.readme_summary else '',
        '',
        '| 指标 | 数值 |',
        '|------|------|',
        f'| ⭐ Star | {format_stars(repo.stars)} |',
        f'| 📈 今日新增 | +{repo.stars_today} |',
        f'| 🔧 主要语言 | {lang_display} |',
        f'| 📊 推荐指数 | {star_display} ({analysis.score}/10) |',
        '',
        f'**核心功能**: {analysis.readme_summary[:100]}' if analysis.readme_summary else '',
        f'**技术栈**: {tech_stack_display}',
        f'**适合人群**: {audience}',
        '',
    ]

    return '\n'.join(line for line in lines if line is not None)


def generate_simple_row(analysis: RepoAnalysis, index: int) -> str:
    """生成简单列表行"""
    repo = analysis.repo
    lang = repo.language or '未知'
    return f'| {index} | [{repo.name}]({repo.url}) | {lang} | {format_stars(repo.stars)} | +{repo.stars_today} | {analysis.score}/10 |'


def generate_markdown(analyses: list[RepoAnalysis], date: datetime = None) -> str:
    """
    生成完整的 Markdown 报告

    Args:
        analyses: 分析结果列表
        date: 报告日期，默认为今天

    Returns:
        Markdown 格式的字符串
    """
    if date is None:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%d')

    # 按评分排序
    sorted_analyses = sorted(analyses, key=lambda x: x.score, reverse=True)

    # 统计语言分布
    lang_count = {}
    for a in analyses:
        lang = a.repo.language or 'Other'
        lang_count[lang] = lang_count.get(lang, 0) + 1

    top_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:5]
    lang_summary = ' | '.join(f'{lang}: {count}' for lang, count in top_langs)

    # 生成报告
    lines = [
        f'# GitHub Trending 每日精选 ({date_str})',
        '',
        f'> 🔥 今日共收录 **{len(analyses)}** 个热门项目',
        f'>',
        f'> 📊 语言分布: {lang_summary}',
        '',
        '---',
        '',
        '## 🏆 今日重点推荐',
        '',
    ]

    # 添加 Top 3 推荐
    for i, analysis in enumerate(sorted_analyses[:3], 1):
        lines.append(generate_repo_section(analysis, rank=i))
        lines.append('---')
        lines.append('')

    # 完整列表
    lines.extend([
        '## 📋 完整列表',
        '',
        '| # | 项目 | 语言 | Star | 今日 | 评分 |',
        '|---|------|------|------|------|------|',
    ])

    for i, analysis in enumerate(sorted_analyses, 1):
        lines.append(generate_simple_row(analysis, i))

    lines.extend([
        '',
        '---',
        '',
        f'📅 更新时间: {date.strftime("%Y-%m-%d %H:%M:%S")}',
        '',
        '> 本报告由 [GitHub Trending Daily](https://github.com) 自动生成',
    ])

    return '\n'.join(lines)


def save_report(content: str, base_dir: str = 'archives', date: datetime = None) -> str:
    """
    保存报告到文件

    Args:
        content: Markdown 内容
        base_dir: 存档基础目录
        date: 报告日期

    Returns:
        保存的文件路径
    """
    if date is None:
        date = datetime.now()

    # 创建目录结构: archives/2026/01/
    dir_path = Path(base_dir) / date.strftime('%Y') / date.strftime('%m')
    dir_path.mkdir(parents=True, exist_ok=True)

    # 文件名: 2026-01-30.md
    file_path = dir_path / f'{date.strftime("%Y-%m-%d")}.md'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return str(file_path)
