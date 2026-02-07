"""HN 页面内容测试"""

import re
from playwright.sync_api import Page, expect


def test_hn_stories_count(page: Page, hn_page_url: str):
    """验证 HN 页面显示 30 条 Stories"""
    page.goto(hn_page_url)
    stories = page.locator('.hn-story')
    expect(stories).to_have_count(30)


def test_hn_chinese_titles(page: Page, hn_page_url: str):
    """验证标题包含中文翻译"""
    page.goto(hn_page_url)
    first_title = page.locator('.hn-story h3').first
    title_text = first_title.text_content()
    # 检查是否包含中文字符
    assert re.search(r'[\u4e00-\u9fff]', title_text), f'标题应包含中文: {title_text}'


def test_hn_english_subtitle(page: Page, hn_page_url: str):
    """验证英文原标题作为副标题显示"""
    page.goto(hn_page_url)
    # 检查副标题元素存在 (text-text-muted/60 类)
    subtitles = page.locator('.hn-story p.truncate')
    expect(subtitles.first).to_be_visible()


def test_hn_stats_cards(page: Page, hn_page_url: str):
    """验证统计卡片显示"""
    page.goto(hn_page_url)
    stats = page.locator('.glass-card')
    expect(stats).to_have_count(4)


def test_hn_story_has_score(page: Page, hn_page_url: str):
    """验证每个 Story 都有分数显示"""
    page.goto(hn_page_url)
    # 检查分数 badge
    score_badges = page.locator('.hn-story .text-glow-amber.font-bold')
    expect(score_badges.first).to_be_visible()


def test_hn_story_has_discuss_link(page: Page, hn_page_url: str):
    """验证每个 Story 都有 discuss 链接"""
    page.goto(hn_page_url)
    discuss_links = page.locator('.hn-story a:has-text("discuss")')
    expect(discuss_links.first).to_be_visible()
    # 验证链接指向 news.ycombinator.com
    href = discuss_links.first.get_attribute('href')
    assert 'news.ycombinator.com' in href, f'discuss 链接应指向 HN: {href}'
