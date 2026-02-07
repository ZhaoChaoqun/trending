"""深度分析页面测试"""

import pytest
from pathlib import Path
from playwright.sync_api import Page, expect


@pytest.fixture
def deep_dive_url():
    """深度分析页面 URL"""
    path = Path(__file__).parent.parent / 'archives/deep-dive/gitbutler.html'
    return f'file://{path.absolute()}'


def test_deep_dive_page_loads(page: Page, deep_dive_url: str):
    """验证深度分析页面加载"""
    page.goto(deep_dive_url)
    # 页面应该加载成功
    expect(page.locator('body')).to_be_visible()


def test_deep_dive_back_link(page: Page, deep_dive_url: str):
    """验证返回链接"""
    page.goto(deep_dive_url)
    back_link = page.locator('a:has-text("返回")')
    expect(back_link).to_be_visible()


def test_deep_dive_project_name(page: Page, deep_dive_url: str):
    """验证项目名显示"""
    page.goto(deep_dive_url)
    # 项目名应该在 h1 中
    h1 = page.locator('h1').first
    expect(h1).to_be_visible()
    name = h1.text_content()
    assert len(name) > 0, "项目名不应为空"


def test_deep_dive_new_badge(page: Page, deep_dive_url: str):
    """验证 NEW 标签"""
    page.goto(deep_dive_url)
    # NEW 标签可能存在
    new_badge = page.locator('text=NEW')
    # 不强制要求存在，因为不是所有页面都有
    expect(new_badge.first).to_be_visible()


def test_deep_dive_github_button(page: Page, deep_dive_url: str):
    """验证 GitHub 按钮"""
    page.goto(deep_dive_url)
    github_btn = page.locator('a[href*="github.com"]').first
    expect(github_btn).to_be_visible()
    href = github_btn.get_attribute('href')
    assert 'github.com' in href, f"应该链接到 GitHub: {href}"


def test_deep_dive_meta_info(page: Page, deep_dive_url: str):
    """验证元信息显示"""
    page.goto(deep_dive_url)
    # 检查有 Star 相关内容
    expect(page.locator('body')).to_contain_text('Star')


def test_deep_dive_stats_grid(page: Page, deep_dive_url: str):
    """验证统计网格"""
    page.goto(deep_dive_url)
    # 检查排名或分数
    rank_or_score = page.locator('text=/[#\\d]|Score/i')
    expect(rank_or_score.first).to_be_visible()


def test_deep_dive_ai_analysis(page: Page, deep_dive_url: str):
    """验证 AI 分析区域"""
    page.goto(deep_dive_url)
    # 检查 AI 生成标记
    ai_label = page.locator('text=AI')
    expect(ai_label.first).to_be_visible()


def test_deep_dive_maintainer_section(page: Page, deep_dive_url: str):
    """验证维护者区域存在"""
    page.goto(deep_dive_url)
    # 检查页面包含 GitHub 相关内容（注意大小写）
    expect(page.locator('body')).to_contain_text('GitHub')


def test_deep_dive_view_repo_cta(page: Page, deep_dive_url: str):
    """验证查看仓库 CTA"""
    page.goto(deep_dive_url)
    cta = page.locator('text=查看仓库')
    expect(cta.first).to_be_visible()


def test_deep_dive_footer(page: Page, deep_dive_url: str):
    """验证页脚"""
    page.goto(deep_dive_url)
    footer = page.locator('text=GitHub Trending')
    expect(footer.first).to_be_visible()


def test_deep_dive_responsive_layout(page: Page, deep_dive_url: str):
    """验证响应式布局"""
    page.goto(deep_dive_url)

    # 检查桌面布局
    page.set_viewport_size({'width': 1280, 'height': 800})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()

    # 检查移动端布局
    page.set_viewport_size({'width': 375, 'height': 667})
    page.wait_for_timeout(300)
    expect(page.locator('body')).to_be_visible()


def test_all_deep_dive_pages_exist(page: Page):
    """验证所有深度分析页面存在"""
    deep_dive_dir = Path(__file__).parent.parent / 'archives/deep-dive'
    html_files = list(deep_dive_dir.glob('*.html'))

    assert len(html_files) > 0, "应该有深度分析页面"

    for html_file in html_files:
        url = f'file://{html_file.absolute()}'
        page.goto(url)
        # 每个页面都应该能加载
        expect(page.locator('body')).to_be_visible()
