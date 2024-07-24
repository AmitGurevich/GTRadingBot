//@version=5
strategy(title="Adaptive SMI Ergodic Strategy", shorttitle="Adaptive SMI Strategy", overlay = true)

// Inputs
longlen = input.int(3, minval=1, title="Long Length")
shortlen = input.int(6, minval=1, title="Short Length")
siglen = input.int(5, minval=1, title="Signal Line Length")
overS = input.float(-0.4, title = "Oversold Threshold", step = 0.01)
overB = input.float(0.4, title = "Overbought Threshold", step = 0.01)
cooldownMinutes = input.int(60, title="Cooldown Period (minutes)")

// Calculations
erg = ta.tsi(close, shortlen, longlen)
sig = ta.ema(erg, siglen)

// Plotting
emiPlot = plot(erg, color = color.blue, title = "SMI")
plot(sig, color = color.orange, title="Signal")
hline(0, title = "Zero", color = color.gray, linestyle = hline.style_dotted)
h0 = hline(overB, color = color.gray, title = "Overbought")
h1 = hline(overS, color = color.gray, title = "Oversold")
fill(h0, h1, color=color.rgb(25, 117, 192, 90), title = "Background")
midLinePlot = plot(0, color = na, editable = false, display = display.none)
fill(emiPlot, midLinePlot, 1, overB, top_color = color.new(#51b855, 0), bottom_color = color.new(#4cb04f, 100), title = "Overbought Gradient")
fill(emiPlot, midLinePlot, overS, -1, top_color = color.new(#fc5151, 100), bottom_color = color.new(#f54f4f, 0), title = "Oversold Gradient")

// Conditions
longEntry = ta.crossover(erg, overS) and erg > sig
shortEntry = ta.crossunder(erg, overB) and erg < sig

// Exit Conditions
longExit = ta.crossunder(erg, overB)
shortExit = ta.crossover(erg, overS)

// Cooldown logic(do not touch)
var float lastTradeTime = na
var float cooldownPeriod = cooldownMinutes * 60000  // convert minutes to milliseconds
canTrade = na(lastTradeTime) or (time - lastTradeTime > cooldownPeriod)

if longEntry and canTrade
    strategy.entry("Long", strategy.long)
    lastTradeTime := time

if shortEntry and canTrade
    strategy.entry("Short", strategy.short)
    lastTradeTime := time

if longExit
    strategy.close("Long")

if shortExit
    strategy.close("Short")
