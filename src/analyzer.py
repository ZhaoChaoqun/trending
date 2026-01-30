"""项目分析模块"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
from .scraper import TrendingRepo


@dataclass
class RepoAnalysis:
    """仓库分析结果"""
    repo: TrendingRepo
    language_stats: dict[str, float]  # 语言占比
    topics: list[str]  # 标签
    license: Optional[str]
    readme_summary: str
    tech_stack: list[str]
    score: int  # 推荐评分 1-10
    score_details: dict[str, int]  # 各维度评分


def fetch_repo_details(repo_url: str, headers: dict) -> dict:
    """
    获取仓库详情页信息

    Args:
        repo_url: 仓库 URL
        headers: 请求头

    Returns:
        包含语言统计、topics、license 等信息的字典
    """
    result = {
        'language_stats': {},
        'topics': [],
        'license': None
    }

    try:
        response = requests.get(repo_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # 获取 topics/tags
        topic_links = soup.select('a[data-octo-click="topic_click"]')
        result['topics'] = [t.get_text(strip=True) for t in topic_links]

        # 获取 license
        license_elem = soup.select_one('a[data-analytics-event*="LICENSE"]')
        if license_elem:
            result['license'] = license_elem.get_text(strip=True)

        # 获取语言统计
        lang_stats = soup.select('a[data-ga-click*="Repository, language stats"]')
        for stat in lang_stats:
            spans = stat.select('span')
            if len(spans) >= 2:
                lang = spans[0].get_text(strip=True)
                pct_text = spans[1].get_text(strip=True).replace('%', '')
                try:
                    pct = float(pct_text)
                    result['language_stats'][lang] = pct
                except ValueError:
                    pass

        # 备用方法：从进度条获取语言统计
        if not result['language_stats']:
            lang_bar = soup.select('ul.list-style-none li a')
            for item in lang_bar:
                aria_label = item.get('aria-label', '')
                if aria_label:
                    # 格式如 "Python 65.2%"
                    parts = aria_label.rsplit(' ', 1)
                    if len(parts) == 2:
                        lang = parts[0]
                        pct_text = parts[1].replace('%', '')
                        try:
                            pct = float(pct_text)
                            result['language_stats'][lang] = pct
                        except ValueError:
                            pass

    except Exception:
        pass

    return result


def calculate_score(repo: TrendingRepo, details: dict) -> tuple[int, dict[str, int]]:
    """
    计算推荐评分

    评分维度:
    - star_growth: Star 增长速度 (今日新增)
    - popularity: 项目热度 (总 Star 数)
    - documentation: 文档完整度 (基于 topics 和描述)
    - community: 社区参与度 (贡献者数、forks)

    Returns:
        (总分, 各维度评分字典)
    """
    scores = {}

    # Star 增长速度 (1-10)
    try:
        stars_today = int(repo.stars_today.replace(',', '').replace(',', ''))
    except (ValueError, AttributeError):
        stars_today = 0

    if stars_today >= 500:
        scores['star_growth'] = 10
    elif stars_today >= 300:
        scores['star_growth'] = 9
    elif stars_today >= 200:
        scores['star_growth'] = 8
    elif stars_today >= 100:
        scores['star_growth'] = 7
    elif stars_today >= 50:
        scores['star_growth'] = 6
    elif stars_today >= 30:
        scores['star_growth'] = 5
    elif stars_today >= 20:
        scores['star_growth'] = 4
    elif stars_today >= 10:
        scores['star_growth'] = 3
    else:
        scores['star_growth'] = 2

    # 项目热度 (1-10)
    try:
        total_stars = int(repo.stars.replace(',', '').replace(',', '').replace('k', '000'))
    except (ValueError, AttributeError):
        total_stars = 0

    if total_stars >= 50000:
        scores['popularity'] = 10
    elif total_stars >= 20000:
        scores['popularity'] = 9
    elif total_stars >= 10000:
        scores['popularity'] = 8
    elif total_stars >= 5000:
        scores['popularity'] = 7
    elif total_stars >= 2000:
        scores['popularity'] = 6
    elif total_stars >= 1000:
        scores['popularity'] = 5
    elif total_stars >= 500:
        scores['popularity'] = 4
    elif total_stars >= 100:
        scores['popularity'] = 3
    else:
        scores['popularity'] = 2

    # 文档完整度 (1-10)
    doc_score = 5  # 基础分
    if repo.description and len(repo.description) > 50:
        doc_score += 1
    if details.get('topics') and len(details['topics']) >= 3:
        doc_score += 2
    if details.get('license'):
        doc_score += 1
    scores['documentation'] = min(doc_score, 10)

    # 社区参与度 (1-10)
    try:
        forks = int(repo.forks.replace(',', '').replace(',', ''))
    except (ValueError, AttributeError):
        forks = 0

    contrib_count = len(repo.contributors)

    community_score = 4  # 基础分
    if forks >= 1000:
        community_score += 3
    elif forks >= 500:
        community_score += 2
    elif forks >= 100:
        community_score += 1

    if contrib_count >= 5:
        community_score += 2
    elif contrib_count >= 3:
        community_score += 1

    scores['community'] = min(community_score, 10)

    # 计算总分 (加权平均)
    weights = {
        'star_growth': 0.35,
        'popularity': 0.25,
        'documentation': 0.20,
        'community': 0.20
    }

    total = sum(scores[k] * weights[k] for k in scores)
    final_score = round(total)

    return final_score, scores


def identify_tech_stack(repo: TrendingRepo, details: dict) -> list[str]:
    """
    识别技术栈

    基于语言、topics 等信息推断技术栈
    """
    tech_stack = []

    # 添加主要语言
    if repo.language:
        tech_stack.append(repo.language)

    # 从 topics 中提取技术栈信息
    tech_keywords = {
        'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxt',
        'django', 'flask', 'fastapi', 'express', 'nestjs',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'docker', 'kubernetes', 'aws', 'gcp', 'azure',
        'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'graphql', 'rest-api', 'grpc',
        'typescript', 'rust', 'go', 'nodejs'
    }

    topics = details.get('topics', [])
    for topic in topics:
        topic_lower = topic.lower()
        if topic_lower in tech_keywords:
            formatted = topic.title() if topic_lower not in ('aws', 'gcp', 'api', 'grpc') else topic.upper()
            if formatted not in tech_stack:
                tech_stack.append(formatted)

    # 添加其他语言
    for lang in details.get('language_stats', {}).keys():
        if lang not in tech_stack:
            tech_stack.append(lang)

    return tech_stack[:6]  # 最多返回6个


def analyze_repo(repo: TrendingRepo, fetch_details: bool = True) -> RepoAnalysis:
    """
    分析单个仓库

    Args:
        repo: TrendingRepo 对象
        fetch_details: 是否获取详情页信息

    Returns:
        RepoAnalysis 分析结果
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    details = {'language_stats': {}, 'topics': [], 'license': None}

    if fetch_details:
        details = fetch_repo_details(repo.url, headers)

    # 如果没有获取到语言统计，使用默认值
    if not details['language_stats'] and repo.language:
        details['language_stats'] = {repo.language: 100.0}

    score, score_details = calculate_score(repo, details)
    tech_stack = identify_tech_stack(repo, details)

    # 生成简短摘要
    readme_summary = repo.description if repo.description else '暂无描述'

    return RepoAnalysis(
        repo=repo,
        language_stats=details['language_stats'],
        topics=details['topics'],
        license=details['license'],
        readme_summary=readme_summary,
        tech_stack=tech_stack,
        score=score,
        score_details=score_details
    )


def analyze_repos(repos: list[TrendingRepo], fetch_details: bool = False) -> list[RepoAnalysis]:
    """
    批量分析仓库

    Args:
        repos: TrendingRepo 列表
        fetch_details: 是否获取详情页（注意：开启会增加请求数量）

    Returns:
        RepoAnalysis 列表
    """
    analyses = []
    for repo in repos:
        analysis = analyze_repo(repo, fetch_details=fetch_details)
        analyses.append(analysis)

    # 按评分排序
    analyses.sort(key=lambda x: x.score, reverse=True)

    return analyses
