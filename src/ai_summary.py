"""AI 智能总结模块 - 使用 Azure OpenAI 为项目生成中文解读"""

import os
import re
import requests
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# 加载 .env 文件（本地开发用）
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / '.env')
except ImportError:
    pass


@dataclass
class AISummary:
    """AI 生成的项目总结"""
    repo_name: str
    summary: str  # 一句话中文总结
    highlights: list[str]  # 核心亮点 (2-3条)
    use_cases: str  # 适用场景


# Azure OpenAI 配置 (通过环境变量配置)
def get_azure_config():
    """延迟获取配置，确保 .env 已加载"""
    return {
        'endpoint': os.getenv('AZURE_OPENAI_ENDPOINT', ''),
        'api_key': os.getenv('AZURE_OPENAI_KEY', ''),
        'deployment': os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o'),
        'api_version': '2025-04-01-preview'
    }


def fetch_readme(repo_name: str, max_length: int = 16000) -> Optional[str]:
    """
    从 GitHub 获取仓库的 README 内容

    Args:
        repo_name: 仓库名称 (owner/repo)
        max_length: 最大返回字符数 (避免 token 过长)

    Returns:
        README 内容文本，失败返回 None
    """
    # 尝试常见的 README 文件名
    readme_files = ['README.md', 'readme.md', 'README', 'readme', 'README.rst']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0',
        'Accept': 'application/vnd.github.raw+json'
    }

    for readme_file in readme_files:
        url = f"https://raw.githubusercontent.com/{repo_name}/main/{readme_file}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.text
                # 清理 markdown：移除图片、徽章、HTML 标签
                content = re.sub(r'!\[.*?\]\(.*?\)', '', content)  # 移除图片
                content = re.sub(r'<[^>]+>', '', content)  # 移除 HTML 标签
                content = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', content)  # 移除徽章链接
                content = re.sub(r'\n{3,}', '\n\n', content)  # 压缩多余空行
                content = content.strip()

                if len(content) > max_length:
                    content = content[:max_length] + '...'
                return content
        except requests.exceptions.RequestException:
            continue

        # 尝试 master 分支
        url = f"https://raw.githubusercontent.com/{repo_name}/master/{readme_file}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = response.text
                content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
                content = re.sub(r'<[^>]+>', '', content)
                content = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', content)
                content = re.sub(r'\n{3,}', '\n\n', content)
                content = content.strip()

                if len(content) > max_length:
                    content = content[:max_length] + '...'
                return content
        except requests.exceptions.RequestException:
            continue

    return None


def generate_summary(repo_name: str, description: str, language: str,
                     stars: str, stars_today: str, topics: list[str] = None,
                     readme: str = None) -> Optional[AISummary]:
    """
    使用 Azure OpenAI 生成项目的中文智能总结

    Args:
        repo_name: 仓库名称 (owner/repo)
        description: 项目描述 (通常是英文)
        language: 主要编程语言
        stars: 总 Star 数
        stars_today: 今日新增 Star
        topics: GitHub topics 标签
        readme: README 文件内容 (可选，提供更准确的总结)

    Returns:
        AISummary 对象，失败返回 None
    """
    if not description:
        description = "无描述"

    topics_str = ', '.join(topics) if topics else '无'

    # 构建项目信息，包含 README 内容
    readme_section = ""
    if readme:
        readme_section = f"""
README 内容摘要:
{readme[:1500]}
"""

    prompt = f"""你是一个技术项目分析专家。请为以下 GitHub 热门项目生成简洁的中文解读。

项目信息：
- 名称: {repo_name}
- 描述: {description}
- 语言: {language or '未知'}
- Star: {stars} (今日 +{stars_today})
- 标签: {topics_str}
{readme_section}
请根据以上信息，按以下 JSON 格式输出（不要输出其他内容）：
{{
  "summary": "一句话总结这个项目是做什么的（20-40字，用中文，通俗易懂，让普通开发者能快速理解）",
  "highlights": ["核心亮点1", "核心亮点2"],
  "use_cases": "适用场景（15-25字）"
}}"""

    try:
        config = get_azure_config()
        url = f"{config['endpoint'].rstrip('/')}/openai/deployments/{config['deployment']}/chat/completions?api-version={config['api_version']}"

        headers = {
            'Content-Type': 'application/json',
            'api-key': config['api_key']
        }

        payload = {
            'messages': [
                {'role': 'system', 'content': '你是一个专业的技术项目分析师，擅长用简洁的中文解读开源项目的价值。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_completion_tokens': 300
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content'].strip()

        # 解析 JSON 响应
        import json
        # 处理可能的 markdown 代码块包裹
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
        content = content.strip()

        data = json.loads(content)

        return AISummary(
            repo_name=repo_name,
            summary=data.get('summary', ''),
            highlights=data.get('highlights', []),
            use_cases=data.get('use_cases', '')
        )

    except requests.exceptions.RequestException as e:
        print(f"⚠️ AI 总结请求失败 ({repo_name}): {e}")
        return None
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"⚠️ AI 响应解析失败 ({repo_name}): {e}")
        return None


def batch_generate_summaries(repos: list[dict], max_count: int = 10,
                              fetch_readme_content: bool = True) -> dict[str, AISummary]:
    """
    批量生成项目总结

    Args:
        repos: 项目信息列表，每个包含 name, description, language, stars, stars_today, topics
        max_count: 最多生成多少个总结 (控制 API 调用次数)
        fetch_readme_content: 是否获取 README 内容以提供更准确的总结

    Returns:
        {repo_name: AISummary} 字典
    """
    summaries = {}
    total = min(len(repos), max_count)

    for i, repo in enumerate(repos[:max_count]):
        repo_name = repo['name']
        print(f"🤖 正在生成 AI 总结 ({i+1}/{total}): {repo_name}")

        # 获取 README 内容
        readme = None
        if fetch_readme_content:
            print(f"   📖 获取 README...")
            readme = fetch_readme(repo_name)
            if readme:
                print(f"   ✅ README 获取成功 ({len(readme)} 字符)")
            else:
                print(f"   ⚠️ README 获取失败，使用描述生成")

        summary = generate_summary(
            repo_name=repo_name,
            description=repo.get('description', ''),
            language=repo.get('language'),
            stars=repo.get('stars', '0'),
            stars_today=repo.get('stars_today', '0'),
            topics=repo.get('topics', []),
            readme=readme
        )

        if summary:
            summaries[repo_name] = summary
            print(f"   ✅ 总结: {summary.summary}")

    return summaries


if __name__ == '__main__':
    # 测试 - 包含 README 获取
    print("📖 获取 README...")
    readme = fetch_readme('facebook/react')

    print("\n🤖 生成 AI 总结...")
    test_summary = generate_summary(
        repo_name='facebook/react',
        description='A declarative, efficient, and flexible JavaScript library for building user interfaces.',
        language='JavaScript',
        stars='220,000',
        stars_today='100',
        topics=['react', 'javascript', 'frontend', 'ui'],
        readme=readme
    )

    if test_summary:
        print(f"\n✅ 测试成功!")
        print(f"总结: {test_summary.summary}")
        print(f"亮点: {test_summary.highlights}")
        print(f"场景: {test_summary.use_cases}")
    else:
        print("\n❌ 测试失败")
