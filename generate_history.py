#!/usr/bin/env python3
"""生成最近7天的模拟历史数据，用于演示排名变化功能"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.history import RankingEntry, save_ranking_history
from src.dashboard import generate_dashboard_html, save_dashboard
from src.analyzer import RepoAnalysis
from src.scraper import TrendingRepo

# 模拟的项目池（包含一些会持续出现的项目和一些会新上榜的项目）
PROJECT_POOL = [
    {"name": "openclaw/openclaw", "lang": "TypeScript", "base_stars": 90000, "desc": "Your own personal AI assistant. Any OS. Any Platform. The lobster way. 🦞"},
    {"name": "asgeirtj/system_prompts_leaks", "lang": "JavaScript", "base_stars": 25000, "desc": "Collection of extracted System Prompts from popular chatbots like ChatGPT, Claude & Gemini"},
    {"name": "lobehub/lobehub", "lang": "TypeScript", "base_stars": 70000, "desc": "The ultimate space for work and life — to find, build, and collaborate with agent teammates"},
    {"name": "NevaMind-AI/memU", "lang": "Python", "base_stars": 5000, "desc": "Memory for 24/7 proactive agents like moltbot"},
    {"name": "hashicorp/vault", "lang": "Go", "base_stars": 34000, "desc": "A tool for secrets management, encryption as a service"},
    {"name": "protocolbuffers/protobuf", "lang": "C++", "base_stars": 70000, "desc": "Protocol Buffers - Google's data interchange format"},
    {"name": "Shubhamsaboo/awesome-llm-apps", "lang": "Python", "base_stars": 90000, "desc": "Collection of awesome LLM apps with AI Agents and RAG"},
    {"name": "MoonshotAI/kimi-cli", "lang": "Python", "base_stars": 4500, "desc": "Kimi Code CLI is your next CLI agent"},
    {"name": "badlogic/pi-mono", "lang": "TypeScript", "base_stars": 3000, "desc": "AI agent toolkit: coding agent CLI, unified LLM API"},
    {"name": "TeamNewPipe/NewPipe", "lang": "Java", "base_stars": 36000, "desc": "A libre lightweight streaming front-end for Android"},
    {"name": "modelcontextprotocol/ext-apps", "lang": "TypeScript", "base_stars": 700, "desc": "Official repo for spec & SDK of MCP Apps protocol"},
    {"name": "pedroslopez/whatsapp-web.js", "lang": "JavaScript", "base_stars": 20000, "desc": "A WhatsApp client library for NodeJS"},
    {"name": "microsoft/playwright-cli", "lang": "TypeScript", "base_stars": 1600, "desc": "CLI for common Playwright actions"},
    {"name": "anthropics/claude-code", "lang": "TypeScript", "base_stars": 45000, "desc": "Claude Code is an agentic coding tool"},
    {"name": "openai/codex", "lang": "Python", "base_stars": 38000, "desc": "Lightweight coding agent that runs in your terminal"},
    {"name": "vercel/ai", "lang": "TypeScript", "base_stars": 12000, "desc": "Build AI-powered applications with React, Svelte, Vue"},
    {"name": "langchain-ai/langchain", "lang": "Python", "base_stars": 95000, "desc": "Building applications with LLMs through composability"},
    {"name": "huggingface/transformers", "lang": "Python", "base_stars": 140000, "desc": "State-of-the-art ML for PyTorch, TensorFlow, and JAX"},
    {"name": "ollama/ollama", "lang": "Go", "base_stars": 120000, "desc": "Get up and running with Llama 3, Mistral, and more"},
    {"name": "microsoft/vscode", "lang": "TypeScript", "base_stars": 170000, "desc": "Visual Studio Code"},
    {"name": "facebook/react", "lang": "JavaScript", "base_stars": 230000, "desc": "The library for web and native user interfaces"},
    {"name": "denoland/deno", "lang": "Rust", "base_stars": 98000, "desc": "A modern runtime for JavaScript and TypeScript"},
    {"name": "astral-sh/uv", "lang": "Rust", "base_stars": 55000, "desc": "An extremely fast Python package installer"},
    {"name": "tailwindlabs/tailwindcss", "lang": "CSS", "base_stars": 85000, "desc": "A utility-first CSS framework"},
]


def generate_day_data(date: datetime, day_offset: int) -> list[RankingEntry]:
    """生成某一天的排名数据"""
    random.seed(date.toordinal())  # 使用日期作为种子，确保同一天数据一致

    # 每天选择 20-25 个项目
    num_projects = random.randint(20, 25)

    # 根据日期选择不同的项目组合
    # 越近的日期，越可能包含更多"新"项目
    available_projects = PROJECT_POOL.copy()

    # 随机打乱并选择
    random.shuffle(available_projects)
    selected = available_projects[:num_projects]

    # 为每个项目生成当天的数据
    entries = []
    for i, proj in enumerate(selected):
        # 模拟 star 增长
        days_ago = 6 - day_offset
        stars = proj["base_stars"] + random.randint(100, 2000) * days_ago
        stars_today = random.randint(50, 800)

        # 添加一些高增长项目
        if random.random() < 0.15:
            stars_today = random.randint(1000, 5000)

        entries.append(RankingEntry(
            name=proj["name"],
            rank=i + 1,
            stars=f"{stars:,}",
            stars_today=str(stars_today),
            language=proj["lang"],
            description=proj["desc"]
        ))

    # 按 stars_today 重新排序
    entries.sort(key=lambda x: int(x.stars_today.replace(',', '')), reverse=True)

    # 更新排名
    for i, entry in enumerate(entries):
        entry.rank = i + 1

    return entries


def create_mock_analysis(entry: RankingEntry) -> RepoAnalysis:
    """从 RankingEntry 创建 RepoAnalysis"""
    repo = TrendingRepo(
        name=entry.name,
        url=f"https://github.com/{entry.name}",
        description=entry.description,
        language=entry.language,
        stars=entry.stars,
        stars_today=entry.stars_today,
        forks="0",
        contributors=[]
    )

    # 计算评分
    try:
        stars_today = int(entry.stars_today.replace(',', ''))
    except ValueError:
        stars_today = 0

    if stars_today >= 500:
        score = 9
    elif stars_today >= 300:
        score = 8
    elif stars_today >= 100:
        score = 7
    else:
        score = 6

    return RepoAnalysis(
        repo=repo,
        language_stats={entry.language: 100.0} if entry.language else {},
        topics=[],
        license=None,
        readme_summary=entry.description,
        tech_stack=[entry.language] if entry.language else [],
        score=score,
        score_details={}
    )


def main():
    base_dir = Path(__file__).parent / 'archives'
    today = datetime.now()

    print("🗓️ 生成最近7天的历史数据...\n")

    # 生成过去7天的数据
    for day_offset in range(7):
        date = today - timedelta(days=6 - day_offset)
        date_str = date.strftime('%Y-%m-%d')

        print(f"📅 生成 {date_str} 的数据...")

        # 生成当天数据
        entries = generate_day_data(date, day_offset)

        # 保存历史数据
        history_path = save_ranking_history(entries, str(base_dir), date)
        print(f"   ✅ JSON: {history_path}")

        # 加载昨天数据计算变化
        from src.history import load_yesterday_rankings, calculate_rank_changes

        yesterday_entries = load_yesterday_rankings(str(base_dir), date)
        rank_changes = calculate_rank_changes(entries, yesterday_entries)

        # 统计
        new_count = sum(1 for c in rank_changes if c.is_new)
        up_count = sum(1 for c in rank_changes if c.change and c.change > 0)
        down_count = sum(1 for c in rank_changes if c.change and c.change < 0)

        print(f"   📊 项目: {len(entries)} | 新上榜: {new_count} | 上升: {up_count} | 下降: {down_count}")

        # 生成 HTML 仪表板
        analyses = [create_mock_analysis(e) for e in entries]
        html_content = generate_dashboard_html(analyses, rank_changes, date)

        # 保存 HTML
        dir_path = base_dir / date.strftime('%Y') / date.strftime('%m')
        dir_path.mkdir(parents=True, exist_ok=True)
        html_path = dir_path / f'{date_str}.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✅ HTML: {html_path}")

        print()

    # 复制最新的到 index.html
    latest_html = base_dir / today.strftime('%Y') / today.strftime('%m') / f'{today.strftime("%Y-%m-%d")}.html'
    if latest_html.exists():
        index_path = base_dir / 'index.html'
        with open(latest_html, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ index.html 已更新")

    print("\n" + "=" * 50)
    print("🎉 完成！最近7天的数据已生成")
    date_str = today.strftime('%Y-%m-%d')
    html_file = base_dir / today.strftime('%Y') / today.strftime('%m') / f'{date_str}.html'
    print(f"📂 打开查看: {html_file}")
    print("=" * 50)


if __name__ == '__main__':
    main()
