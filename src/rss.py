"""RSS Feed 生成器"""

from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from .analyzer import RepoAnalysis


def generate_rss(analyses: list[RepoAnalysis], date: datetime = None,
                 base_url: str = "https://github.com/trending") -> str:
    """
    生成 RSS 2.0 格式的 Feed

    Args:
        analyses: 项目分析结果列表
        date: 发布日期
        base_url: 基础 URL

    Returns:
        RSS XML 字符串
    """
    if date is None:
        date = datetime.now()

    date_str = date.strftime('%Y-%m-%d')
    pub_date = date.strftime('%a, %d %b %Y %H:%M:%S +0000')

    # 创建 RSS 根元素
    rss = Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

    channel = SubElement(rss, 'channel')

    # Channel 元数据
    title = SubElement(channel, 'title')
    title.text = 'GitHub Trending 每日热榜'

    link = SubElement(channel, 'link')
    link.text = base_url

    description = SubElement(channel, 'description')
    description.text = '每日追踪 GitHub Trending 热门项目，AI 智能解读'

    language = SubElement(channel, 'language')
    language.text = 'zh-CN'

    pub_date_elem = SubElement(channel, 'pubDate')
    pub_date_elem.text = pub_date

    last_build = SubElement(channel, 'lastBuildDate')
    last_build.text = pub_date

    # 添加每个项目作为 item
    for i, analysis in enumerate(analyses[:10], 1):  # Top 10
        repo = analysis.repo
        item = SubElement(channel, 'item')

        item_title = SubElement(item, 'title')
        item_title.text = f"#{i} {repo.name} (+{repo.stars_today} stars)"

        item_link = SubElement(item, 'link')
        item_link.text = repo.url

        item_desc = SubElement(item, 'description')
        desc_content = f"""
<![CDATA[
<p><strong>{repo.name}</strong></p>
<p>{repo.description}</p>
<p>⭐ {repo.stars} | +{repo.stars_today} today | 🔧 {repo.language or 'Unknown'}</p>
<p>推荐指数: {analysis.score}/10</p>
]]>
"""
        item_desc.text = desc_content

        item_guid = SubElement(item, 'guid')
        item_guid.text = f"{repo.url}#{date_str}"
        item_guid.set('isPermaLink', 'false')

        item_pub = SubElement(item, 'pubDate')
        item_pub.text = pub_date

    # 格式化 XML
    xml_str = tostring(rss, encoding='unicode')
    # 添加 XML 声明
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str

    return xml_str


def save_rss(content: str, base_dir: str, date: datetime = None) -> str:
    """
    保存 RSS 文件

    Args:
        content: RSS XML 内容
        base_dir: 基础目录
        date: 日期

    Returns:
        保存的文件路径
    """
    if date is None:
        date = datetime.now()

    base_path = Path(base_dir)
    base_path.mkdir(parents=True, exist_ok=True)

    # 保存为 rss.xml (固定文件名，便于订阅)
    rss_path = base_path / 'rss.xml'
    rss_path.write_text(content, encoding='utf-8')

    return str(rss_path)
