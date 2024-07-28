//@version=5
strategy(title="Enhanced Adaptive SMI Ergodic Strategy", shorttitle="Enhanced SMI Strategy", overlay=true)

// Inputs
longlen = input.int(6, minval=1, title="Long Length")
shortlen = input.int(6, minval=1, title="Short Length")
siglen = input.int(5, minval=1, title="Signal Line Length")
overS = input.float(-0.2, title="Oversold Threshold", step=0.01)
overB = input.float(0.2, title="Overbought Threshold", step=0.01)
cooldownMinutes = input.int(30, title="Cooldown Period (minutes)")
useATR = input.bool(true, title="Use ATR for Stop Loss and Take Profit")
atrPeriod = input.int(14, title="ATR Period")
atrMultiplierSL = input.float(1.5, title="ATR Multiplier for Stop Loss", step=0.1)
atrMultiplierTP = input.float(2, title="ATR Multiplier for Take Profit", step=0.1)
rsiPeriod = input.int(14, title="RSI Period")
rsiOversold = input.int(40, title="RSI Oversold Level")
rsiOverbought = input.int(60, title="RSI Overbought Level")

// Calculations
erg = ta.tsi(close, shortlen, longlen)
sig = ta.ema(erg, siglen)
atr = ta.atr(atrPeriod)
rsi = ta.rsi(close, rsiPeriod)

// Plotting
plot(erg, color=color.blue, title="SMI")
plot(sig, color=color.orange, title="Signal")
hline(0, title="Zero", color=color.gray, linestyle=hline.style_dotted)
h0 = hline(overB, color=color.gray, title="Overbought")
h1 = hline(overS, color=color.gray, title="Oversold")
fill(h0, h1, color=color.rgb(25, 117, 192, 90), title="Background")

// Conditions
longCondition = erg < overS and erg > sig and rsi < rsiOversold
shortCondition = erg > overB and erg < sig and rsi > rsiOverbought

// Exit Conditions
longExit = erg > overB or rsi > rsiOverbought
shortExit = erg < overS or rsi < rsiOversold

// Cooldown logic
var float lastTradeTime = na
cooldownPeriod = cooldownMinutes * 60000 // convert minutes to milliseconds
canTrade = na(lastTradeTime) or (time - lastTradeTime > cooldownPeriod)

// Stop Loss and Take Profit Calculations
stopLoss = atr * atrMultiplierSL
takeProfit = atr * atrMultiplierTP

if longCondition and canTrade
    strategy.entry("Long", strategy.long)
    strategy.exit("Long TP/SL", "Long", stop=strategy.position_avg_price - stopLoss, limit=strategy.position_avg_price + takeProfit)
    lastTradeTime := time

if shortCondition and canTrade
    strategy.entry("Short", strategy.short)
    strategy.exit("Short TP/SL", "Short", stop=strategy.position_avg_price + stopLoss, limit=strategy.position_avg_price - takeProfit)
    lastTradeTime := time

if longExit
    strategy.close("Long")

if shortExit
    strategy.close("Short")
