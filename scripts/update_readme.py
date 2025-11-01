#!/usr/bin/env python3
"""
README更新スクリプト
README.mdの更新日時とチャート画像を自動で書き換える
"""

import re
from datetime import datetime
from pathlib import Path


def update_readme():
    """README.mdの更新日時とチャート画像を書き換え"""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        return
    
    # 最新のチャートファイルを検索
    chart_dir = Path(__file__).parent.parent / "charts"
    chart_files = sorted(chart_dir.glob("chart_*.png"), reverse=True)
    
    if not chart_files:
        print("Warning: No chart files found")
        chart_filename = "chart_latest.png"
    else:
        chart_filename = chart_files[0].name
        print(f"Using chart: {chart_filename}")
    
    # 現在の日付 (ISO 8601形式)
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    # READMEを読み込み
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 日付部分を置換
    updated_content = re.sub(
        r"<!-- Last Updated: .* -->",
        f"<!-- Last Updated: {current_date} -->",
        content
    )
    
    # チャート画像のパスを置換
    updated_content = re.sub(
        r"!\[Stock Chart\]\(charts/.*?\.png\)",
        f"![Stock Chart](charts/{chart_filename})",
        updated_content
    )
    
    # 変更があった場合のみ書き込み
    if content != updated_content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"README.md updated: {current_date}")
        print(f"Chart updated: {chart_filename}")
    else:
        print("README.md is already up to date")


if __name__ == "__main__":
    update_readme()
