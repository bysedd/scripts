import pandas as pd
import yfinance as yf

# Material data
MATERIALS_DATA = {
    "Gold": {
        "ticker": "GC=F",
        "unit_weight": 0.031103477,  # Troy ounce to kg
        "talents": 29,
        "shekels": 730,
    },
    "Silver": {
        "ticker": "SI=F",
        "unit_weight": 0.031103477,  # Troy ounce to kg
        "talents": 100,
        "shekels": 1775,
    },
    "Copper": {
        "ticker": "HG=F",
        "unit_weight": 0.45359237,  # Pound to kg
        "talents": 70,
        "shekels": 2400,
    },
}

# Unit conversions
TALENT_TO_KG = 34.2  # 1 talent ≈ 34.2 kg
SHEKEL_TO_KG = 0.0114  # 1 shekel ≈ 11.4 g

# Create DataFrame from material data
materials_df = pd.DataFrame.from_dict(MATERIALS_DATA, orient="index")

# Calculate the total weight in kg for each material
materials_df["weight_kg"] = (
    materials_df["talents"] * TALENT_TO_KG + materials_df["shekels"] * SHEKEL_TO_KG
)

# Get the list of tickers
tickers_list = materials_df["ticker"].tolist()

# Download the current prices of materials
prices_df = yf.download(tickers=tickers_list, period="1d", progress=False)[
    "Close"
].iloc[0]

# Get the USD/BRL exchange rate
usd_brl_rate = yf.Ticker("BRL=X").history(period="1d")["Close"].iloc[0]

# Calculate the price per kg in USD for each material
materials_df["price_usd_per_kg"] = materials_df.apply(
    lambda row: prices_df[row["ticker"]] / row["unit_weight"], axis=1
)

# Calculate the cost in USD and BRL for each material
materials_df["cost_usd"] = materials_df["weight_kg"] * materials_df["price_usd_per_kg"]
materials_df["cost_brl"] = materials_df["cost_usd"] * usd_brl_rate

# Setting up float formatting
pd.options.display.float_format = "{:,.2f}".format

# Display results
print(materials_df[["weight_kg", "cost_usd", "cost_brl"]])
print(f"\nTotal USD: ${materials_df['cost_usd'].sum():,.2f}")
print(f"Total BRL: R${materials_df['cost_brl'].sum():,.2f}")
