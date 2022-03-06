from lib2to3.pgen2.pgen import DFAState
import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
import requests

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='30m',limit=500)

df = pd.DataFrame(bars, columns=['time','open','high','low','close','volume'])
df = df.set_index('time')
df.index = pd.to_datetime(df.index,unit='ms')

adx = df.ta.adx()

macd = df.ta.macd()

rsi = df.ta.rsi()

#print(df)

#print(adx)


df = pd.concat([df,adx,macd,rsi], axis=1)

print(df)

last_row = df.iloc[-1]

print(last_row)

WEBHOOK_URL = 'https://discord.com/api/webhooks/949439426453438525/gGQ0AEBA19lvlmb5ViMYP_qw7Unc-ETM_OaVpkY5zO8MRN94q-gg_BnmPjfOqxzddkX8'

if last_row['ADX_14'] >= 25:
    
    
    if last_row['DMP_14'] > last_row['DMN_14']:
        message = f"STRONG UPTREND DETECTED: The ADX is {last_row['ADX_14']:.2f}"
    if last_row['DMN_14'] > last_row['DMP_14']:
        message = f"STRONG DOWNTREND DETECTED: The ADX is {last_row['ADX_14']:.2f}"
    print(message)

if last_row['ADX_14'] < 25:
    message = f"NO TREND DETECTED: The ADX is {last_row['ADX_14']:.2f}"
    print(message)

    


payload = {
    "username": "alertbot",
    "content": message
}

requests.post(WEBHOOK_URL, json=payload)