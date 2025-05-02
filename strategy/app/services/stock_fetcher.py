import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Example tickers (extend these later)
NIFTY50 = ['RELIANCE.NS','TCS.NS','INFY.NS','HDFCBANK.NS','ICICIBANK.NS','KOTAKBANK.NS','ITC.NS','LARSEN.NS','MARUTI.NS','ULTRACEMCO.NS','ASIANPAINT.NS','HINDUNILVR.NS','NTPC.NS','POWERGRID.NS','BAJAJ-AUTO.NS','WIPRO.NS','M&M.NS','SBIN.NS','HDFC.NS','SUNPHARMA.NS','BHEL.NS','EICHERMOT.NS','JSWSTEEL.NS','HCLTECH.NS','TATAMOTORS.NS','HDFCLIFE.NS','BHARTIARTL.NS','TECHM.NS','GRASIM.NS','CIPLA.NS','ADANIPORTS.NS','DIVISLAB.NS','COALINDIA.NS','TITAN.NS','INDUSINDBK.NS','BOSCHLTD.NS','MCDOWELL-N.NS','RELIANCE.NS','HDFCBANK.NS', 'TCS.NS']
MID_CAP = ['ESCORTS.NS', 'CUMMINSIND.NS','ALKEM.NS','BAJAJFINSV.NS','IDFCFIRSTB.NS','HDFCAMC.NS','HDFC.NS','HINDZINC.NS','RELIANCE.NS','HCLTECH.NS','MARUTI.NS','BHEL.NS','DIVISLAB.NS']
SMALL_CAP = ['BALAMINES.NS', 'AARTIIND.NS', 'ABCAPITAL.NS', 'MSTCLND.NS', 'ADANIGREEN.NS', 'AMARARAJA.NS', 'INDOCOUNT.NS', 'SATYAMCOM.NS']


ALL_TICKERS = {
    "nifty50": NIFTY50,
    "midcap": MID_CAP,
    "smallcap": SMALL_CAP
}

def fetch_and_save_data():
    end = datetime.today()
    start = end - timedelta(days=365 * 2)

    os.makedirs("data/stocks", exist_ok=True)

    for category, tickers in ALL_TICKERS.items():
        for ticker in tickers:
            print(f"Fetching {ticker}...")
            try:
                df = yf.download(ticker, start=start, end=end)
                if not df.empty:
                    df.to_csv(f"data/stocks/{ticker.replace('.NS', '')}_{category}.csv")
            except Exception as e:
                print(f"❌ Error fetching {ticker}: {e}")
