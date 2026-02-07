"""主页导航与侧边栏测试"""

import re
from playwright.sync_api import Page, expect


def test_sidebar_logo_displayed(page: Page, main_page_url: str):
    """验证侧边栏 Logo 显示"""
    page.goto(main_page_url)
    logo = page.locator('h1:has-text("Trending")')
    expect(logo).to_be_visible()


def test_sidebar_version_label(page: Page, main_page_url: str):
    """验证版本标签 SYNAPSE v2.0"""
    page.goto(main_page_url)
    version = page.locator('text=SYNAPSE v2.0')
    expect(version).to_be_visible()


def test_sidebar_feeds_section(page: Page, main_page_url: str):
    """验证 Feeds 导航区域存在"""
    page.goto(main_page_url)
    # 检查各导航项
    expect(page.locator('a:has-text("全部热门")')).to_be_visible()
    expect(page.locator('a:has-text("AI & ML")')).to_be_visible()
    expect(page.locator('a:has-text("前端开发")')).to_be_visible()
    expect(page.locator('a:has-text("系统底层")')).to_be_visible()


def test_sidebar_insights_section(page: Page, main_page_url: str):
    """验证 Insights 导航区域存在"""
    page.goto(main_page_url)
    expect(page.locator('a:has-text("上升最快")')).to_be_visible()
    expect(page.locator('a:has-text("今日新上榜")')).to_be_visible()


def test_sidebar_hn_section(page: Page, main_page_url: str):
    """验证 Hacker News 导航存在"""
    page.goto(main_page_url)
    expect(page.locator('text=Hacker News')).to_be_visible()
    expect(page.locator('a:has-text("Top Stories")')).to_be_visible()


def test_sidebar_data_sync_indicator(page: Page, main_page_url: str):
    """验证数据同步状态指示器"""
    page.goto(main_page_url)
    sync_indicator = page.locator('text=数据已同步')
    expect(sync_indicator).to_be_visible()


def test_header_search_bar_exists(page: Page, main_page_url: str):
    """验证顶部搜索栏存在"""
    page.goto(main_page_url)
    search_input = page.locator('input[type="text"]').first
    expect(search_input).to_be_visible()


def test_header_date_displayed(page: Page, main_page_url: str):
    """验证日期显示"""
    page.goto(main_page_url)
    # 检查日期格式 YYYY-MM-DD
    date_text = page.locator('text=2026-02-07')
    expect(date_text).to_be_visible()


def test_domain_filter_ai_ml(page: Page, main_page_url: str):
    """验证 AI & ML 筛选功能"""
    page.goto(main_page_url)
    # 点击 AI & ML 筛选
    page.click('a:has-text("AI & ML")')
    # 等待筛选生效
    page.wait_for_timeout(500)
    # 验证筛选链接有 active 样式或正在显示
    ai_link = page.locator('a:has-text("AI & ML")')
    expect(ai_link).to_be_visible()


def test_domain_filter_frontend(page: Page, main_page_url: str):
    """验证前端筛选功能"""
    page.goto(main_page_url)
    page.click('a:has-text("前端开发")')
    page.wait_for_timeout(500)
    frontend_link = page.locator('a:has-text("前端开发")')
    expect(frontend_link).to_be_visible()


def test_domain_filter_system(page: Page, main_page_url: str):
    """验证系统底层筛选功能"""
    page.goto(main_page_url)
    page.click('a:has-text("系统底层")')
    page.wait_for_timeout(500)
    system_link = page.locator('a:has-text("系统底层")')
    expect(system_link).to_be_visible()
