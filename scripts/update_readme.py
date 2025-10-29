#!/usr/bin/env python3
"""
README更新スクリプト
README.mdの更新日時を自動で書き換える
"""

import re
from datetime import datetime
from pathlib import Path


def update_readme():
    """README.mdの更新日時を書き換え"""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        return
    
    # 現在の日付 (ISO 8601形式)
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    
    # READMEを読み込み
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 日付部分を置換 (2行目のコメント行)
    updated_content = re.sub(
        r"<!-- Last Updated: .* -->",
        f"<!-- Last Updated: {current_date} -->",
        content
    )
    
    # 変更があった場合のみ書き込み
    if content != updated_content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"README.md updated: {current_date}")
    else:
        print("README.md is already up to date")


if __name__ == "__main__":
    update_readme()
