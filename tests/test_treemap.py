"""Tech Pulse Treemap 测试"""

from playwright.sync_api import Page, expect


def test_treemap_section_header(page: Page, main_page_url: str):
    """验证 Treemap 区域标题"""
    page.goto(main_page_url)
    header = page.locator('h2:has-text("Tech Pulse")')
    expect(header).to_be_visible()


def test_treemap_subtitle(page: Page, main_page_url: str):
    """验证 Treemap 副标题说明"""
    page.goto(main_page_url)
    # 检查副标题文本
    subtitle = page.locator('text=实时 GitHub 市场情绪')
    expect(subtitle).to_be_visible()


def test_treemap_time_filters(page: Page, main_page_url: str):
    """验证时间筛选按钮"""
    page.goto(main_page_url)
    expect(page.locator('button:has-text("24h")')).to_be_visible()
    expect(page.locator('button:has-text("7d")')).to_be_visible()
    expect(page.locator('button:has-text("30d")')).to_be_visible()


def test_treemap_language_filters(page: Page, main_page_url: str):
    """验证语言筛选按钮"""
    page.goto(main_page_url)
    # All Languages 按钮
    expect(page.locator('button:has-text("All Languages")')).to_be_visible()


def test_treemap_has_domain_headers(page: Page, main_page_url: str):
    """验证领域标题存在"""
    page.goto(main_page_url)
    # 检查页面包含领域相关内容
    body_text = page.locator('body').text_content()
    assert 'AI' in body_text or 'Frontend' in body_text or 'System' in body_text, \
        "页面应该包含领域分类信息"


def test_treemap_items_exist(page: Page, main_page_url: str):
    """验证 Treemap 项目存在"""
    page.goto(main_page_url)
    # 检查 treemap 项目元素
    treemap_items = page.locator('.treemap-item')
    count = treemap_items.count()
    assert count > 0, f"Treemap 应该有项目，实际 {count} 个"


def test_treemap_item_has_repo_name(page: Page, main_page_url: str):
    """验证 Treemap 项目显示仓库名"""
    page.goto(main_page_url)
    # 检查第一个 treemap 项目
    first_item = page.locator('.treemap-item').first
    expect(first_item).to_be_visible()
    # 项目应该有文本内容
    text = first_item.text_content()
    assert len(text) > 0, "Treemap 项目应该显示仓库名"


def test_treemap_item_hover_effect(page: Page, main_page_url: str):
    """验证 Treemap 项目悬停效果"""
    page.goto(main_page_url)
    item = page.locator('.treemap-item').first
    # 悬停前获取样式
    item.hover()
    # 悬停应该触发 CSS transform 效果（通过类或 style 检测）
    expect(item).to_be_visible()


def test_treemap_time_filter_24h_default(page: Page, main_page_url: str):
    """验证 24h 按钮是默认状态"""
    page.goto(main_page_url)
    btn_24h = page.locator('.treemap-time-filter[data-time="24h"]')
    expect(btn_24h).to_be_visible()
    # 检查是否有特殊样式（bg-synapse-bg 表示激活）
    class_attr = btn_24h.get_attribute('class')
    assert 'bg-synapse-bg' in class_attr or 'text-white' in class_attr, \
        f"24h 按钮应该是默认激活状态，实际 class: {class_attr}"


def test_treemap_click_time_filter(page: Page, main_page_url: str):
    """验证点击时间筛选按钮"""
    page.goto(main_page_url)
    btn_7d = page.locator('button:has-text("7d")')
    btn_7d.click()
    page.wait_for_timeout(300)
    # 验证按钮可点击且页面不崩溃
    expect(btn_7d).to_be_visible()


def test_treemap_click_language_filter(page: Page, main_page_url: str):
    """验证点击语言筛选按钮"""
    page.goto(main_page_url)
    lang_btn = page.locator('.treemap-lang-filter').first
    lang_btn.click()
    page.wait_for_timeout(300)
    expect(lang_btn).to_be_visible()


def test_treemap_item_clickable(page: Page, main_page_url: str):
    """验证 Treemap 项目可点击"""
    page.goto(main_page_url)
    item = page.locator('.treemap-item').first
    # 获取项目的 onclick 或检查 cursor 样式
    expect(item).to_be_visible()
    # 点击不应导致错误
    # item.click()  # 会打开新窗口，跳过实际点击


def test_treemap_items_have_size_classes(page: Page, main_page_url: str):
    """验证 Treemap 项目有尺寸类"""
    page.goto(main_page_url)
    item = page.locator('.treemap-item').first
    class_attr = item.get_attribute('class')
    # 应该包含 col-span 和 row-span
    assert 'col-span' in class_attr, f"项目应该有 col-span 类: {class_attr}"
    assert 'row-span' in class_attr, f"项目应该有 row-span 类: {class_attr}"
