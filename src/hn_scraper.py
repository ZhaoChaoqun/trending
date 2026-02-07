"""
Hacker News 数据抓取器

使用 HN 官方 Firebase REST API 获取 Top/Best Stories
"""

import requests
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class HNStory:
    """Hacker News 故事"""
    id: int
    title: str
    url: str
    score: int
    author: str
    time: int  # unix timestamp
    comments: int
    hn_url: str  # https://news.ycombinator.com/item?id=xxx
    title_zh: str = ''  # 中文翻译标题

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'title_zh': self.title_zh,
            'url': self.url,
            'score': self.score,
            'author': self.author,
            'time': self.time,
            'comments': self.comments,
            'hn_url': self.hn_url
        }


HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def fetch_story_ids(story_type: str = 'top') -> list[int]:
    """
    获取故事 ID 列表

    Args:
        story_type: 'top', 'best', 'new'

    Returns:
        故事 ID 列表
    """
    endpoints = {
        'top': f"{HN_API_BASE}/topstories.json",
        'best': f"{HN_API_BASE}/beststories.json",
        'new': f"{HN_API_BASE}/newstories.json"
    }

    url = endpoints.get(story_type, endpoints['top'])

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取 HN {story_type} stories 失败: {e}")
        return []


def fetch_story_detail(story_id: int) -> HNStory | None:
    """
    获取单个故事详情

    Args:
        story_id: 故事 ID

    Returns:
        HNStory 对象或 None
    """
    url = f"{HN_API_BASE}/item/{story_id}.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data or data.get('type') != 'story':
            return None

        return HNStory(
            id=data.get('id', 0),
            title=data.get('title', ''),
            url=data.get('url', ''),
            score=data.get('score', 0),
            author=data.get('by', ''),
            time=data.get('time', 0),
            comments=data.get('descendants', 0) or 0,
            hn_url=f"https://news.ycombinator.com/item?id={data.get('id', 0)}"
        )
    except Exception as e:
        print(f"获取故事 {story_id} 详情失败: {e}")
        return None


def fetch_top_stories(limit: int = 30) -> list[HNStory]:
    """
    获取 HN Top Stories

    Args:
        limit: 获取数量限制

    Returns:
        HNStory 列表
    """
    return _fetch_stories('top', limit)


def fetch_best_stories(limit: int = 30) -> list[HNStory]:
    """
    获取 HN Best Stories

    Args:
        limit: 获取数量限制

    Returns:
        HNStory 列表
    """
    return _fetch_stories('best', limit)


def _fetch_stories(story_type: str, limit: int) -> list[HNStory]:
    """
    并行获取故事详情

    Args:
        story_type: 'top', 'best', 'new'
        limit: 获取数量限制

    Returns:
        HNStory 列表
    """
    story_ids = fetch_story_ids(story_type)[:limit]

    if not story_ids:
        return []

    stories = []
    # 使用线程池并行获取
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {
            executor.submit(fetch_story_detail, sid): sid
            for sid in story_ids
        }

        for future in as_completed(future_to_id):
            story = future.result()
            if story:
                stories.append(story)

    # 按原始排序恢复顺序
    id_order = {sid: i for i, sid in enumerate(story_ids)}
    stories.sort(key=lambda s: id_order.get(s.id, 999))

    return stories


def classify_hn_category(title: str, url: str) -> str:
    """
    分类 HN 故事

    Args:
        title: 故事标题
        url: 故事链接

    Returns:
        分类: AI/ML, Startup, Tools, Programming, Science, Other
    """
    title_lower = title.lower()
    url_lower = url.lower() if url else ''

    # AI/ML 关键词
    ai_keywords = ['ai', 'llm', 'gpt', 'claude', 'openai', 'anthropic', 'machine learning',
                   'neural', 'transformer', 'deep learning', 'chatgpt', 'gemini', 'model']
    if any(kw in title_lower for kw in ai_keywords):
        return 'AI/ML'

    # Startup 关键词
    startup_keywords = ['startup', 'yc', 'funding', 'raise', 'acquired', 'ipo', 'series',
                        'valuation', 'founder', 'launch']
    if any(kw in title_lower for kw in startup_keywords):
        return 'Startup'

    # Tools 关键词
    tools_keywords = ['tool', 'cli', 'app', 'editor', 'ide', 'terminal', 'browser',
                      'vim', 'emacs', 'vscode', 'plugin']
    if any(kw in title_lower for kw in tools_keywords):
        return 'Tools'

    # Programming 关键词
    prog_keywords = ['rust', 'python', 'javascript', 'typescript', 'go ', 'golang',
                     'java', 'c++', 'programming', 'code', 'compiler', 'language',
                     'framework', 'library', 'api', 'database', 'sql']
    if any(kw in title_lower for kw in prog_keywords):
        return 'Programming'

    # Science 关键词
    science_keywords = ['research', 'paper', 'study', 'physics', 'math', 'science',
                        'biology', 'chemistry', 'quantum', 'space', 'nasa']
    if any(kw in title_lower for kw in science_keywords):
        return 'Science'

    # GitHub 链接
    if 'github.com' in url_lower:
        return 'Tools'

    return 'Other'


def batch_translate_titles(stories: list[HNStory]) -> list[HNStory]:
    """
    批量翻译 HN Stories 标题为中文

    Args:
        stories: HNStory 列表

    Returns:
        更新了 title_zh 的 HNStory 列表
    """
    import os
    import json
    from pathlib import Path

    # 加载 .env 文件
    try:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).parent.parent / '.env')
    except ImportError:
        pass

    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    api_key = os.getenv('AZURE_OPENAI_KEY', '')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o')
    api_version = '2025-04-01-preview'

    if not endpoint or not api_key:
        print("⚠️ 未配置 Azure OpenAI，跳过标题翻译")
        return stories

    # 收集需要翻译的标题
    titles = [s.title for s in stories]

    # 构建 prompt - 批量翻译
    prompt = f"""请将以下英文标题翻译成简洁的中文。保持技术术语的准确性，翻译要通顺自然。

请按 JSON 数组格式返回翻译结果，顺序与输入一致：
["翻译1", "翻译2", ...]

英文标题列表：
{json.dumps(titles, ensure_ascii=False, indent=2)}
"""

    try:
        url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }

        payload = {
            'messages': [
                {'role': 'system', 'content': '你是一个专业的技术文章翻译专家，擅长将英文技术标题翻译成简洁准确的中文。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'max_completion_tokens': 2000
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content'].strip()

        # 解析 JSON 响应
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        content = content.strip()

        translations = json.loads(content)

        # 更新 stories 的 title_zh
        for i, story in enumerate(stories):
            if i < len(translations):
                story.title_zh = translations[i]
            else:
                story.title_zh = story.title  # fallback

        print(f"✅ 成功翻译 {len(translations)} 条标题")
        return stories

    except Exception as e:
        print(f"⚠️ 标题翻译失败: {e}")
        # fallback: 使用原标题
        for story in stories:
            story.title_zh = story.title
        return stories


if __name__ == '__main__':
    # 测试
    print("获取 HN Top Stories...")
    stories = fetch_top_stories(limit=10)
    print(f"获取到 {len(stories)} 条 stories\n")

    for i, story in enumerate(stories, 1):
        category = classify_hn_category(story.title, story.url)
        print(f"{i:2}. [{category:12}] {story.title}")
        print(f"    {story.score} pts | {story.comments} comments | by {story.author}")
        print(f"    {story.url or story.hn_url}\n")
