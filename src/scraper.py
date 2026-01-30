"""GitHub Trending 爬虫模块"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional


@dataclass
class Contributor:
    """贡献者数据结构"""
    username: str
    avatar_url: str


@dataclass
class TrendingRepo:
    """Trending 仓库数据结构"""
    name: str
    url: str
    description: str
    language: Optional[str]
    stars: str
    stars_today: str
    forks: str
    contributors: list[Contributor]


def parse_number(text: str) -> str:
    """解析数字文本，如 '1,234' -> '1,234'"""
    return text.strip().replace(',', ',') if text else '0'


def scrape_trending(language: str = '', since: str = 'daily') -> list[TrendingRepo]:
    """
    爬取 GitHub Trending 页面

    Args:
        language: 编程语言筛选，如 'python', 'javascript'，空字符串表示所有语言
        since: 时间范围，可选 'daily', 'weekly', 'monthly'

    Returns:
        TrendingRepo 列表
    """
    url = 'https://github.com/trending'
    if language:
        url += f'/{language}'

    params = {'since': since} if since else {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    repos = []

    # 查找所有仓库条目
    articles = soup.select('article.Box-row')

    for article in articles:
        # 仓库名和链接
        h2 = article.select_one('h2 a')
        if not h2:
            continue

        repo_path = h2.get('href', '').strip('/')
        repo_name = repo_path
        repo_url = f'https://github.com/{repo_path}'

        # 描述
        desc_elem = article.select_one('p')
        description = desc_elem.get_text(strip=True) if desc_elem else ''

        # 编程语言
        lang_elem = article.select_one('[itemprop="programmingLanguage"]')
        language_name = lang_elem.get_text(strip=True) if lang_elem else None

        # Star 数
        stars_elem = article.select_one('a[href$="/stargazers"]')
        stars = parse_number(stars_elem.get_text(strip=True)) if stars_elem else '0'

        # Fork 数
        forks_elem = article.select_one('a[href$="/forks"]')
        forks = parse_number(forks_elem.get_text(strip=True)) if forks_elem else '0'

        # 今日新增 Star
        stars_today_elem = article.select_one('span.d-inline-block.float-sm-right')
        stars_today = '0'
        if stars_today_elem:
            text = stars_today_elem.get_text(strip=True)
            # 提取数字，如 "1,234 stars today" -> "1,234"
            parts = text.split()
            if parts:
                stars_today = parse_number(parts[0])

        # 贡献者头像
        contributors = []
        contrib_links = article.select('a[data-hovercard-type="user"] img')
        for img in contrib_links[:5]:  # 最多取5个
            alt = img.get('alt', '')
            src = img.get('src', '')
            username = alt[1:] if alt.startswith('@') else alt
            if username and src:
                contributors.append(Contributor(username=username, avatar_url=src))

        repos.append(TrendingRepo(
            name=repo_name,
            url=repo_url,
            description=description,
            language=language_name,
            stars=stars,
            stars_today=stars_today,
            forks=forks,
            contributors=contributors
        ))

    return repos


if __name__ == '__main__':
    # 测试爬取
    repos = scrape_trending()
    print(f'获取到 {len(repos)} 个热门项目')
    for repo in repos[:3]:
        print(f'\n{repo.name}')
        print(f'  描述: {repo.description[:50]}...' if len(repo.description) > 50 else f'  描述: {repo.description}')
        print(f'  语言: {repo.language}')
        print(f'  Star: {repo.stars} (+{repo.stars_today} today)')
