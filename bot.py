import ccxt
import pandas as pd
import talib as ta
import requests
import re

#binance api "qelcTijpKdvgZxhBlObav3kwHGwO3jck6qgvpXnHuQmtrA3Fy1zJkVHMqlvQniYX"
#binance secret "nx7z2DBSaF2BP53dwg4L93HW7vktnzINiU8vdl3X9OEOkzsL1kdrAGI35H9eVniN"

api = "940aaf92-80da-4ebe-9e91-eab5ad662d43"
secret = "2933253BAEDD892AEE7A226B61BA7300"
okx_password = "Behsat075524525."

binance = ccxt.okx({
    'enableRateLimit': True,
    'apiKey': api,
    'secret': secret,
    
    "options": {'defaultType': 'futures'}
})

#Get pairs
markets = binance.load_markets()
pairs = []

for i in markets:
    x = re.search(":USDT$",i)
    if x:
        pairs.append(i)
        print(i)

#print(pairs)
#symbol = "BTC/USDT:USDT"
timeFrame = "15m"
limit = 500

signal = pd.DataFrame(index=pairs, columns=['lastsignal'])
#signal = ""

while True:
    for i in pairs:
        bars = binance.fetch_ohlcv(i, timeframe=timeFrame, limit=limit)
        df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
        df["timestamp"] = pd.to_datetime(df['timestamp'],unit='ms')


        #STOCK RSI CEKME

        # 1) ilk aşama rsi değerini hesaplıyoruz.
        rsi = ta.RSI(df["close"], 14)

        # 2) ikinci aşamada rsi arrayinden sıfırları kaldırıyoruz.
        #rsi = rsi[~np.isnan(rsi)]

        # 3) üçüncü aşamada ise ta-lib stoch metodunu uyguluyoruz.
        stochrsif, stochrsis = ta.STOCH(rsi, rsi, rsi, fastk_period=14, slowk_period=3, slowd_period=3)

        print(stochrsif,stochrsis)
        #Code

        signalgecici = ""
        message = ""
        if float(stochrsif[len(stochrsif)-3]) < float(stochrsis[len(stochrsis)-3]) and float(stochrsif[len(stochrsif)-2]) > float(stochrsis[len(stochrsis)-2]) and float(stochrsis[len(stochrsis)-2]) < 25 and float(stochrsif[len(stochrsif)-2]) < 25:
            signalgecici = str([[i,stochrsif[len(stochrsif)-2], stochrsis[len(stochrsis)-2], "buy"]])
            message = str([i," BUY"])

        if float(stochrsif[len(stochrsif)-3]) > float(stochrsis[len(stochrsis)-3]) and float(stochrsif[len(stochrsif)-2]) < float(stochrsis[len(stochrsis)-2]) and float(stochrsis[len(stochrsis)-2]) > 75 and float(stochrsif[len(stochrsif)-2]) > 75:
            signalgecici = str([[i,stochrsif[len(stochrsif)-2], stochrsis[len(stochrsis)-2], "sell"]])
            message = str([i," SELL"])

        print(signal)
        #Telegram

        if signal.loc[i,"lastsignal"] != signalgecici:
            requests.post(url="https://api.telegram.org/bot6211346923:AAEIFug7_BiaAspj_UukMpxvzC5WY3mDgd0/sendMessage",data={"chat_id":-615601352,"text":message}).json
            signal.loc[i,"lastsignal"] = signalgecici
        
        print(stochrsif, stochrsis, message)
        print(df)
