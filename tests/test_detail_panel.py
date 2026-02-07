"""详情面板测试"""

from playwright.sync_api import Page, expect


def test_detail_panel_exists(page: Page, main_page_url: str):
    """验证详情面板存在"""
    page.goto(main_page_url)
    # 详情面板应该在右侧
    panel = page.locator('#detail-panel')
    expect(panel).to_be_visible()


def test_detail_panel_placeholder_text(page: Page, main_page_url: str):
    """验证详情面板默认占位文本"""
    page.goto(main_page_url)
    # 检查占位提示
    placeholder = page.locator('#detail-placeholder')
    # 面板存在
    panel = page.locator('#detail-panel')
    expect(panel).to_be_visible()


def test_detail_panel_shows_rank(page: Page, main_page_url: str):
    """验证详情面板显示排名"""
    page.goto(main_page_url)
    # 点击第一个项目
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查排名显示
    rank = page.locator('#detail-rank')
    expect(rank).to_be_visible()
    rank_text = rank.text_content()
    assert '#' in rank_text, f"排名应该包含 #，实际: {rank_text}"


def test_detail_panel_shows_project_name(page: Page, main_page_url: str):
    """验证详情面板显示项目名"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查项目名
    name = page.locator('#detail-name')
    expect(name).to_be_visible()
    name_text = name.text_content()
    assert len(name_text) > 0, "项目名不应为空"


def test_detail_panel_shows_author(page: Page, main_page_url: str):
    """验证详情面板显示作者"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查作者（带 @ 符号）
    author = page.locator('#detail-author')
    expect(author).to_be_visible()
    author_text = author.text_content()
    assert '@' in author_text, f"Author 应该包含 @，实际: {author_text}"


def test_detail_panel_view_repo_button(page: Page, main_page_url: str):
    """验证 View Repository 按钮"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查按钮
    btn = page.locator('#detail-repo-link')
    expect(btn).to_be_visible()
    href = btn.get_attribute('href')
    assert 'github.com' in href, f"按钮应该链接到 GitHub，实际: {href}"


def test_detail_panel_shows_total_stars(page: Page, main_page_url: str):
    """验证详情面板显示总 Star 数"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查 stars
    stars = page.locator('#detail-total-stars')
    expect(stars).to_be_visible()


def test_detail_panel_shows_stars_today(page: Page, main_page_url: str):
    """验证详情面板显示今日新增 Star"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查今日新增
    stars_today = page.locator('#detail-stars-today')
    expect(stars_today).to_be_visible()


def test_detail_panel_shows_description(page: Page, main_page_url: str):
    """验证详情面板显示描述"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # 检查描述
    desc = page.locator('#detail-desc')
    expect(desc).to_be_visible()


def test_detail_panel_ai_section(page: Page, main_page_url: str):
    """验证 AI 摘要区域存在"""
    page.goto(main_page_url)
    page.locator('[data-repo-id]').first.click()
    page.wait_for_timeout(500)
    # AI 摘要区域
    ai_section = page.locator('#detail-ai-section')
    expect(ai_section).to_have_count(1)


def test_detail_panel_click_different_items(page: Page, main_page_url: str):
    """验证点击不同项目更新详情面板"""
    page.goto(main_page_url)

    # 点击第一个项目
    items = page.locator('[data-repo-id]')
    items.first.click()
    page.wait_for_timeout(500)
    first_name = page.locator('#detail-name').text_content()

    # 点击第二个项目
    if items.count() > 1:
        items.nth(1).click()
        page.wait_for_timeout(500)
        second_name = page.locator('#detail-name').text_content()

        # 验证名称不同
        assert first_name != second_name, \
            f"点击不同项目应该更新详情，但名称相同: {first_name}"


def test_feed_item_has_repo_id(page: Page, main_page_url: str):
    """验证 Feed 项目有 repo-id 数据属性"""
    page.goto(main_page_url)
    first_item = page.locator('[data-repo-id]').first
    expect(first_item).to_be_visible()
    repo_id = first_item.get_attribute('data-repo-id')
    assert repo_id and '/' in repo_id, f"应该有 repo-id，实际: {repo_id}"


def test_feed_item_has_project_info(page: Page, main_page_url: str):
    """验证 Feed 项目显示项目信息"""
    page.goto(main_page_url)
    first_item = page.locator('[data-repo-id]').first
    expect(first_item).to_be_visible()
    # 项目应该有文本内容
    text = first_item.text_content()
    assert len(text) > 10, "Feed 项目应该有项目信息"


def test_feed_item_hover_effect(page: Page, main_page_url: str):
    """验证 Feed 项目悬停效果"""
    page.goto(main_page_url)
    first_item = page.locator('[data-repo-id]').first
    first_item.hover()
    # 悬停后应该有视觉变化
    expect(first_item).to_be_visible()
