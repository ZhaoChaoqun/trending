# GitHub Trending 每日精选

自动抓取 GitHub Trending 热门项目，生成每日精选报告。

## 功能特性

- 每日自动抓取 GitHub Trending 页面
- 智能分析项目：语言分布、技术栈、推荐评分
- 生成结构化 Markdown 报告
- 自动存档历史记录
- GitHub Actions 定时执行

## 项目结构

```
trending/
├── .github/workflows/
│   └── daily-trending.yml    # GitHub Actions 工作流
├── src/
│   ├── __init__.py
│   ├── scraper.py            # GitHub Trending 爬虫
│   ├── analyzer.py           # 项目分析模块
│   └── generator.py          # Markdown 生成器
├── archives/                 # 历史报告存档
│   └── YYYY/MM/YYYY-MM-DD.md
├── main.py                   # 入口文件
├── requirements.txt          # Python 依赖
└── README.md
```

## 使用方法

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

### 自动化

项目配置了 GitHub Actions，每天北京时间 09:00 自动执行并提交更新。

也可以在 Actions 页面手动触发运行。

## 报告格式

每日报告包含：

- **重点推荐**: Top 3 项目详细分析
- **完整列表**: 所有热门项目表格
- **项目信息**: Star 数、今日增长、语言、技术栈、推荐评分

## 评分标准

推荐评分 (1-10) 基于以下维度：

| 维度 | 权重 | 说明 |
|------|------|------|
| Star 增长 | 35% | 今日新增 Star 数 |
| 项目热度 | 25% | 总 Star 数 |
| 文档完整度 | 20% | 描述、标签、许可证 |
| 社区参与度 | 20% | Fork 数、贡献者数 |

## 依赖

- Python 3.11+
- requests
- beautifulsoup4
- lxml

## License

MIT
