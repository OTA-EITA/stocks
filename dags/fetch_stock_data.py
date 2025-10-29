#!/usr/bin/env python3
"""
株価データ取得スクリプト
Yahoo Finance APIから株価情報を取得し、JSONファイルに保存する
"""

import json
import requests
import time
import random
from datetime import datetime
from pathlib import Path


# 取得対象のティッカーシンボル
TICKERS = [
    "AAPL",   # Apple
    "GOOGL",  # Google
    "MSFT",   # Microsoft
    "AMZN",   # Amazon
    "TSLA",   # Tesla
]

# Yahoo Finance API エンドポイント
YAHOO_API_BASE = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


def fetch_stock_price(ticker: str) -> dict:
    """
    指定されたティッカーの株価情報を取得
    
    Args:
        ticker: ティッカーシンボル (例: AAPL)
        
    Returns:
        株価情報を含む辞書
    """
    url = YAHOO_API_BASE.format(ticker=ticker)
    params = {
        "interval": "1d",
        "range": "1d",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # データ解析
        result = data["chart"]["result"][0]
        meta = result["meta"]
        quote = result["indicators"]["quote"][0]
        
        return {
            "ticker": ticker,
            "currency": meta.get("currency", "USD"),
            "regularMarketPrice": meta.get("regularMarketPrice"),
            "previousClose": meta.get("previousClose"),
            "open": quote.get("open", [None])[0],
            "high": quote.get("high", [None])[0],
            "low": quote.get("low", [None])[0],
            "close": quote.get("close", [None])[0],
            "volume": quote.get("volume", [None])[0],
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return {
            "ticker": ticker,
            "error": str(e)
        }


def main():
    """メイン処理"""
    print("Starting stock data fetch...")
    print(f"Target tickers: {', '.join(TICKERS)}")
    
    # データ取得
    results = []
    for i, ticker in enumerate(TICKERS):
        print(f"Fetching {ticker}...")
        stock_data = fetch_stock_price(ticker)
        results.append(stock_data)
        
        # レート制限対策: リクエスト間隔を空ける
        if i < len(TICKERS) - 1:
            sleep_time = random.uniform(1, 3)
            print(f"Waiting {sleep_time:.1f}s...")
            time.sleep(sleep_time)
    
    # タイムスタンプ追加
    output_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "stocks": results
    }
    
    # JSON保存
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "stock_prices.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {output_file}")
    print(f"Total stocks fetched: {len(results)}")
    
    # サマリー表示
    print("\n=== Summary ===")
    for stock in results:
        if "error" in stock:
            print(f"{stock['ticker']}: ERROR - {stock['error']}")
        else:
            price = stock.get("regularMarketPrice", "N/A")
            print(f"{stock['ticker']}: ${price}")


if __name__ == "__main__":
    main()
