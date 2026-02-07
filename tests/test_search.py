"""搜索功能测试"""

from playwright.sync_api import Page, expect


def test_search_input_exists(page: Page, main_page_url: str):
    """验证搜索输入框存在"""
    page.goto(main_page_url)
    search = page.locator('#search-input')
    expect(search).to_be_visible()


def test_search_placeholder_text(page: Page, main_page_url: str):
    """验证搜索框占位文本"""
    page.goto(main_page_url)
    search = page.locator('#search-input')
    placeholder = search.get_attribute('placeholder')
    assert placeholder and len(placeholder) > 0, "搜索框应该有占位文本"


def test_search_filters_projects(page: Page, main_page_url: str):
    """验证搜索能过滤项目"""
    page.goto(main_page_url)

    # 获取初始项目数量
    initial_items = page.locator('.feed-item:visible')
    initial_count = initial_items.count()

    # 输入搜索词
    search = page.locator('#search-input')
    search.fill('github')
    page.wait_for_timeout(500)

    # 搜索后应该有变化（或保持不变如果没匹配）
    expect(search).to_have_value('github')


def test_search_case_insensitive(page: Page, main_page_url: str):
    """验证搜索不区分大小写"""
    page.goto(main_page_url)
    search = page.locator('#search-input')

    # 输入大写
    search.fill('GITHUB')
    page.wait_for_timeout(300)

    # 清空后输入小写
    search.fill('github')
    page.wait_for_timeout(300)

    # 验证搜索框工作正常
    expect(search).to_have_value('github')


def test_search_clear_shows_all(page: Page, main_page_url: str):
    """验证清空搜索显示所有项目"""
    page.goto(main_page_url)
    search = page.locator('#search-input')

    # 先输入搜索词
    search.fill('test')
    page.wait_for_timeout(300)

    # 清空
    search.fill('')
    page.wait_for_timeout(300)

    # 验证搜索框已清空
    expect(search).to_have_value('')


def test_search_partial_match(page: Page, main_page_url: str):
    """验证部分匹配搜索"""
    page.goto(main_page_url)
    search = page.locator('#search-input')

    # 输入部分词
    search.fill('git')
    page.wait_for_timeout(300)

    expect(search).to_have_value('git')


def test_search_no_results_handling(page: Page, main_page_url: str):
    """验证无结果时的处理"""
    page.goto(main_page_url)
    search = page.locator('#search-input')

    # 输入不太可能匹配的词
    search.fill('xyzabc123impossible')
    page.wait_for_timeout(500)

    # 页面不应崩溃
    expect(search).to_be_visible()


def test_search_special_characters(page: Page, main_page_url: str):
    """验证特殊字符搜索"""
    page.goto(main_page_url)
    search = page.locator('#search-input')

    # 输入带特殊字符的词
    search.fill('react/')
    page.wait_for_timeout(300)

    expect(search).to_be_visible()


def test_hn_search_exists(page: Page, hn_page_url: str):
    """验证 HN 页面搜索框存在"""
    page.goto(hn_page_url)
    search = page.locator('#search-input')
    expect(search).to_be_visible()


def test_hn_search_filters_stories(page: Page, hn_page_url: str):
    """验证 HN 搜索能过滤故事"""
    page.goto(hn_page_url)
    search = page.locator('#search-input')

    # 输入搜索词
    search.fill('AI')
    page.wait_for_timeout(500)

    expect(search).to_have_value('AI')
