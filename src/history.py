"""历史数据管理模块 - 用于追踪排名变化"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RankingEntry:
    """排名条目"""
    name: str
    rank: int
    stars: str
    stars_today: str
    language: Optional[str]
    description: str


@dataclass
class RankChange:
    """排名变化信息"""
    name: str
    current_rank: int
    previous_rank: Optional[int]
    change: Optional[int]  # 正数表示上升，负数表示下降
    is_new: bool  # 是否是新上榜项目


def get_history_file_path(base_dir: str, date: datetime) -> Path:
    """获取历史数据文件路径"""
    dir_path = Path(base_dir) / date.strftime('%Y') / date.strftime('%m')
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path / f'{date.strftime("%Y-%m-%d")}.json'


def save_ranking_history(entries: list[RankingEntry], base_dir: str = 'archives',
                         date: datetime = None) -> str:
    """
    保存当日排名数据

    Args:
        entries: 排名条目列表
        base_dir: 存档基础目录
        date: 日期，默认为今天

    Returns:
        保存的文件路径
    """
    if date is None:
        date = datetime.now()

    file_path = get_history_file_path(base_dir, date)

    data = {
        'date': date.strftime('%Y-%m-%d'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'count': len(entries),
        'rankings': [asdict(e) for e in entries]
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(file_path)


def load_ranking_history(base_dir: str = 'archives', date: datetime = None) -> Optional[list[RankingEntry]]:
    """
    加载指定日期的排名数据

    Args:
        base_dir: 存档基础目录
        date: 日期，默认为今天

    Returns:
        排名条目列表，如果文件不存在返回 None
    """
    if date is None:
        date = datetime.now()

    file_path = get_history_file_path(base_dir, date)

    if not file_path.exists():
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return [RankingEntry(**entry) for entry in data.get('rankings', [])]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def load_yesterday_rankings(base_dir: str = 'archives', today: datetime = None) -> Optional[list[RankingEntry]]:
    """
    加载昨天的排名数据

    Args:
        base_dir: 存档基础目录
        today: 今天的日期，默认为当前日期

    Returns:
        昨天的排名条目列表，如果不存在返回 None
    """
    if today is None:
        today = datetime.now()

    yesterday = today - timedelta(days=1)
    return load_ranking_history(base_dir, yesterday)


def calculate_rank_changes(current_entries: list[RankingEntry],
                           previous_entries: Optional[list[RankingEntry]]) -> list[RankChange]:
    """
    计算排名变化

    Args:
        current_entries: 当前排名列表
        previous_entries: 前一天排名列表

    Returns:
        包含排名变化信息的列表
    """
    changes = []

    # 创建昨天排名的映射 (name -> rank)
    previous_ranks = {}
    if previous_entries:
        for entry in previous_entries:
            previous_ranks[entry.name] = entry.rank

    for entry in current_entries:
        previous_rank = previous_ranks.get(entry.name)

        if previous_rank is None:
            # 新上榜项目
            changes.append(RankChange(
                name=entry.name,
                current_rank=entry.rank,
                previous_rank=None,
                change=None,
                is_new=True
            ))
        else:
            # 计算排名变化 (previous_rank - current_rank，因为数字越小排名越高)
            change = previous_rank - entry.rank
            changes.append(RankChange(
                name=entry.name,
                current_rank=entry.rank,
                previous_rank=previous_rank,
                change=change,
                is_new=False
            ))

    return changes


def format_rank_change(change: RankChange) -> str:
    """
    格式化排名变化显示

    Returns:
        如 "↑3", "↓2", "NEW", "-" (无变化)
    """
    if change.is_new:
        return "NEW"

    if change.change is None:
        return "-"

    if change.change > 0:
        return f"↑{change.change}"
    elif change.change < 0:
        return f"↓{abs(change.change)}"
    else:
        return "-"
