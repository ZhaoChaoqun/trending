"""Pytest fixtures for Playwright tests"""

import pytest
from pathlib import Path


@pytest.fixture
def main_page_url():
    """GitHub Trending 主页 URL"""
    path = Path(__file__).parent.parent / 'archives/2026/02/2026-02-07.html'
    return f'file://{path.absolute()}'


@pytest.fixture
def hn_page_url():
    """HN 页面 URL"""
    path = Path(__file__).parent.parent / 'archives/hn.html'
    return f'file://{path.absolute()}'
