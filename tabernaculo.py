import pandas as pd
import yfinance as yf

# Tickers and units
tickers = {
    "Gold": {"ticker": "GC=F", "unit_weight": 0.031103477},  # Troy ounce to kg
    "Silver": {"ticker": "SI=F", "unit_weight": 0.031103477},  # Troy ounce to kg
    "Copper": {"ticker": "HG=F", "unit_weight": 0.45359237},  # Pound to kg
}

# Quantities per material
data = {
    "Gold": {"talents": 29, "shekels": 730},
    "Silver": {"talents": 100, "shekels": 1775},
    "Copper": {"talents": 70, "shekels": 2400},
}

# Unit conversions
talent_to_kg = 34.2  # 1 talent ≈ 34.2 kg
shekel_to_kg = 0.0114  # 1 shekel ≈ 11.4 g

# Get current prices
tickers_yf = [info["ticker"] for info in tickers.values()]
prices = yf.download(tickers=tickers_yf, period="1d", progress=False)["Close"]

# Get USD/BRL exchange rate
usd_brl = yf.Ticker("BRL=X")
usd_brl_rate = usd_brl.history(period="1d")["Close"].iloc[0]

# Create DataFrame
df = pd.DataFrame.from_dict(data, orient="index")
df["weight_kg"] = (df["talents"] * talent_to_kg) + (df["shekels"] * shekel_to_kg)

# Add prices to DataFrame
for material in df.index:
    ticker = tickers[material]["ticker"]
    unit_weight = tickers[material]["unit_weight"]
    # Extract scalar price value
    unit_price = prices[ticker].iloc[0]
    price_usd_per_kg = unit_price / unit_weight
    df.loc[material, "price_usd_per_kg"] = price_usd_per_kg

# Calculate costs
df["cost_usd"] = df["weight_kg"] * df["price_usd_per_kg"]
df["cost_brl"] = df["cost_usd"] * usd_brl_rate

# Formatting
pd.options.display.float_format = "{:,.2f}".format

# Display results
print(df[["weight_kg", "cost_usd", "cost_brl"]])
print(f"\nTotal USD: ${df['cost_usd'].sum():,.2f}")
print(f"Total BRL: R${df['cost_brl'].sum():,.2f}")
