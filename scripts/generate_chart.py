#!/usr/bin/env python3
"""
株価グラフ生成スクリプト
JSONファイルから株価データを読み込み、棒グラフを生成する
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path


def generate_chart():
    """株価データを読み込んでグラフを生成"""
    # 最新のJSONファイルを検索
    data_dir = Path(__file__).parent.parent / "data"
    json_files = sorted(data_dir.glob("stock_prices_*.json"), reverse=True)
    
    if not json_files:
        print(f"Error: No stock_prices_*.json files found in {data_dir}")
        return
    
    data_file = json_files[0]  # 最新のファイル
    print(f"Using data file: {data_file.name}")
    
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # データ抽出
    tickers = []
    prices = []
    colors = []
    
    for stock in data["stocks"]:
        if "error" not in stock:
            ticker = stock["ticker"]
            price = stock.get("regularMarketPrice")
            
            if price is not None:
                tickers.append(ticker)
                prices.append(price)
                
                # 前日比で色分け
                prev_close = stock.get("previousClose")
                if prev_close and price >= prev_close:
                    colors.append("#2ecc71")  # 緑 (上昇)
                else:
                    colors.append("#e74c3c")  # 赤 (下落)
    
    if not tickers:
        print("No valid data to plot")
        return
    
    # グラフ作成
    plt.figure(figsize=(10, 6))
    bars = plt.bar(tickers, prices, color=colors, alpha=0.8, edgecolor='black')
    
    # ラベル設定
    plt.xlabel("Ticker", fontsize=12, fontweight='bold')
    plt.ylabel("Price (USD)", fontsize=12, fontweight='bold')
    plt.title("Stock Prices - Latest", fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 値をバーの上に表示
    for bar, price in zip(bars, prices):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 保存 - タイムスタンプベースのファイル名
    chart_dir = Path(__file__).parent.parent / "charts"
    chart_dir.mkdir(exist_ok=True)
    
    # JSONファイル名からタイムスタンプを抽出
    timestamp_str = data_file.stem.replace("stock_prices_", "")
    output_file = chart_dir / f"chart_{timestamp_str}.png"
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Chart saved to {output_file}")
    print(f"Plotted {len(tickers)} stocks: {', '.join(tickers)}")


if __name__ == "__main__":
    generate_chart()
