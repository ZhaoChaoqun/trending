"""HN 页面导航测试"""

import re
import pytest
from playwright.sync_api import Page, expect


def test_hn_link_href_correct(page: Page, main_page_url: str):
    """验证 HN 链接路径正确"""
    page.goto(main_page_url)
    hn_link = page.locator('a:has-text("Top Stories")').first
    href = hn_link.get_attribute('href')
    # 从 archives/2026/02/ 到 archives/ 需要向上 2 级
    assert href == '../../hn.html', f'期望 ../../hn.html, 实际 {href}'


@pytest.mark.skip(reason="file:// 协议不支持页面导航，需要 HTTP 服务器")
def test_hn_link_navigation(page: Page, main_page_url: str):
    """验证点击 HN 链接能正确跳转"""
    page.goto(main_page_url)
    page.click('a:has-text("Top Stories")')
    # 等待页面加载
    page.wait_for_load_state('networkidle')
    # 验证 URL 包含 hn.html
    expect(page).to_have_url(re.compile(r'hn\.html'))
    # 验证页面标题
    expect(page.locator('h1')).to_contain_text('Hacker News')


def test_github_link_from_hn_page(page: Page, hn_page_url: str):
    """验证从 HN 页面返回主页"""
    page.goto(hn_page_url)
    page.click('a:has-text("全部热门")')
    page.wait_for_load_state('networkidle')
    # 验证返回主页 (应该能找到 Tech Pulse 相关内容)
    expect(page.locator('h2').first).to_be_visible()


def test_sidebar_hn_active_state(page: Page, hn_page_url: str):
    """验证 HN 页面侧边栏高亮状态"""
    page.goto(hn_page_url)
    # 查找 HN 导航链接
    hn_nav = page.locator('a:has-text("Top Stories")').first
    # 验证有 active 样式类
    expect(hn_nav).to_have_class(re.compile(r'nav-item-active'))
