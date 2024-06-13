//@version=5
indicator("EMA Trend Cloud with SMI", overlay=true)

// Define EMA lengthskl;
ema1_length = 20
ema2_length = 50

// Calculate EMAs using ta.ema function
ema1 = ta.ema(close, ema1_length)
ema2 = ta.ema(close, ema2_length)

// Calculate cloud lines
upper_cloud = ema1 + (ema1 - ema2)
lower_cloud = ema1 - (ema1 - ema2)

// Calculate Stochastic Momentum Index (SMI)
rsiLength = 14
rsi = ta.rsi(close, rsiLength)
k = ta.sma(rsi, 1)
d = ta.sma(k, 3)
smi = (k - d) / (100 - d)

// Plot EMAs
plot(ema1, linewidth=2, color=color.blue)
plot(ema2, linewidth=2, color=color.orange)

// Plot SMI with alert conditions (optional)
plot(smi, linewidth=2, color=color.purple, title="SMI")

// Add horizontal lines for overbought/oversold levels (optional)
hline(0.8, color=color.red, linestyle=hline.style_dashed, title="Overbought")
hline(0.2, color=color.green, linestyle=hline.style_dashed, title="Oversold")
