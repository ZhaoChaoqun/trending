"""跨页面链接与数据一致性测试"""

import re
from pathlib import Path
from playwright.sync_api import Page, expect


def test_main_to_hn_link_correct(page: Page, main_page_url: str):
    """验证主页到 HN 页面链接正确"""
    page.goto(main_page_url)
    hn_link = page.locator('a:has-text("Top Stories")').first
    href = hn_link.get_attribute('href')
    assert href == '../../hn.html', f'链接应该是 ../../hn.html，实际: {href}'


def test_hn_to_main_link_correct(page: Page, hn_page_url: str):
    """验证 HN 页面到主页链接正确"""
    page.goto(hn_page_url)
    main_link = page.locator('a:has-text("全部热门")').first
    href = main_link.get_attribute('href')
    assert 'index.html' in href, f'链接应该包含 index.html，实际: {href}'


def test_deep_dive_back_link_correct(page: Page):
    """验证深度分析页面返回链接正确"""
    deep_dive_path = Path(__file__).parent.parent / 'archives/deep-dive/gitbutler.html'
    page.goto(f'file://{deep_dive_path.absolute()}')

    back_link = page.locator('a:has-text("返回")').first
    href = back_link.get_attribute('href')
    assert '../index.html' in href or 'index' in href, f'返回链接应该指向 index，实际: {href}'


def test_external_links_have_target_blank(page: Page, main_page_url: str):
    """验证外部链接在新窗口打开"""
    page.goto(main_page_url)

    # 检查 GitHub 链接
    github_links = page.locator('a[href*="github.com"]')
    count = github_links.count()

    for i in range(min(count, 5)):  # 只检查前 5 个
        link = github_links.nth(i)
        target = link.get_attribute('target')
        if target:
            assert target == '_blank', f'GitHub 链接应该有 target="_blank"'


def test_theme_consistency_main_and_hn(page: Page, main_page_url: str, hn_page_url: str):
    """验证主页和 HN 页面主题一致"""
    # 检查主页背景色
    page.goto(main_page_url)
    main_bg = page.evaluate('getComputedStyle(document.body).backgroundColor')

    # 检查 HN 页面背景色
    page.goto(hn_page_url)
    hn_bg = page.evaluate('getComputedStyle(document.body).backgroundColor')

    # 背景色应该一致（都是深色主题）
    assert main_bg == hn_bg, f'主题不一致: 主页 {main_bg}, HN {hn_bg}'


def test_sidebar_structure_consistent(page: Page, main_page_url: str, hn_page_url: str):
    """验证侧边栏结构一致"""
    # 检查主页侧边栏
    page.goto(main_page_url)
    main_logo = page.locator('h1:has-text("Trending")').count()

    # 检查 HN 页面侧边栏
    page.goto(hn_page_url)
    hn_logo = page.locator('h1:has-text("Pulse")').count()

    assert main_logo > 0 and hn_logo > 0, '两个页面都应该有 Logo'


def test_stats_cards_present_on_both_pages(page: Page, main_page_url: str, hn_page_url: str):
    """验证两个页面都有统计卡片"""
    # 检查主页统计卡片
    page.goto(main_page_url)
    main_stats = page.locator('.glass-card')
    main_count = main_stats.count()

    # 检查 HN 页面统计卡片
    page.goto(hn_page_url)
    hn_stats = page.locator('.glass-card')
    hn_count = hn_stats.count()

    assert main_count >= 4, f'主页应该有至少 4 个统计卡片，实际: {main_count}'
    assert hn_count >= 4, f'HN 页应该有至少 4 个统计卡片，实际: {hn_count}'


def test_mobile_responsive_main(page: Page, main_page_url: str):
    """验证主页移动端响应式"""
    page.goto(main_page_url)

    # 桌面
    page.set_viewport_size({'width': 1280, 'height': 800})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()

    # 平板
    page.set_viewport_size({'width': 768, 'height': 1024})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()

    # 手机
    page.set_viewport_size({'width': 375, 'height': 667})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()


def test_mobile_responsive_hn(page: Page, hn_page_url: str):
    """验证 HN 页面移动端响应式"""
    page.goto(hn_page_url)

    # 手机
    page.set_viewport_size({'width': 375, 'height': 667})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()

    # 验证内容可见
    expect(page.locator('.hn-story').first).to_be_visible()


def test_no_console_errors(page: Page, main_page_url: str):
    """验证页面无控制台错误"""
    errors = []

    def handle_console(msg):
        if msg.type == 'error':
            errors.append(msg.text)

    page.on('console', handle_console)
    page.goto(main_page_url)
    page.wait_for_timeout(1000)

    # 过滤掉一些常见的无害错误
    critical_errors = [e for e in errors if 'favicon' not in e.lower()]

    assert len(critical_errors) == 0, f'页面有控制台错误: {critical_errors}'


def test_fonts_load_correctly(page: Page, main_page_url: str):
    """验证字体加载"""
    page.goto(main_page_url)
    page.wait_for_timeout(2000)  # 等待字体加载

    # 检查 body 字体
    font_family = page.evaluate('getComputedStyle(document.body).fontFamily')
    assert 'Inter' in font_family or 'sans-serif' in font_family, \
        f'字体应该包含 Inter，实际: {font_family}'


def test_icons_visible(page: Page, main_page_url: str):
    """验证图标可见"""
    page.goto(main_page_url)
    page.wait_for_timeout(1000)

    # 检查 Material Symbols 图标
    icons = page.locator('.material-symbols-outlined')
    count = icons.count()
    assert count > 0, '页面应该有图标'

    # 验证第一个图标可见
    expect(icons.first).to_be_visible()
