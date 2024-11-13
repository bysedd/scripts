import pandas as pd
import yfinance as yf

# Tickers e unidades
tickers = {
    "Ouro": {"ticker": "GC=F", "peso_unidade": 0.031103477},  # Onça troy para kg
    "Prata": {"ticker": "SI=F", "peso_unidade": 0.031103477},  # Onça troy para kg
    "Cobre": {"ticker": "HG=F", "peso_unidade": 0.45359237},  # Libra para kg
}

# Quantidades por material
dados = {
    "Ouro": {"talentos": 29, "siclos": 730},
    "Prata": {"talentos": 100, "siclos": 1775},
    "Cobre": {"talentos": 70, "siclos": 2400},
}

# Conversões de unidades
talento_para_kg = 34.2  # 1 talento ≈ 34,2 kg
siclo_para_kg = 0.0114  # 1 siclo ≈ 11,4 g

# Obter os preços atuais
tickers_yf = [info["ticker"] for info in tickers.values()]
precos = yf.download(tickers=tickers_yf, period="1d", progress=False)["Close"]

# Obter a taxa de câmbio USD/BRL
usd_brl = yf.Ticker("BRL=X")
usd_brl_rate = usd_brl.history(period="1d")["Close"].iloc[0]

# Criar DataFrame
df = pd.DataFrame.from_dict(dados, orient="index")
df["peso_kg"] = (df["talentos"] * talento_para_kg) + (df["siclos"] * siclo_para_kg)

# Adicionar preços ao DataFrame
for material in df.index:
    ticker = tickers[material]["ticker"]
    peso_unidade = tickers[material]["peso_unidade"]
    # Extrair o valor escalar do preço
    preco_unidade = precos[ticker].iloc[0]
    preco_kg = preco_unidade / peso_unidade
    df.loc[material, "preco_usd_kg"] = preco_kg

# Calcular custos
df["custo_usd"] = df["peso_kg"] * df["preco_usd_kg"]
df["custo_brl"] = df["custo_usd"] * usd_brl_rate

# Formatação
pd.options.display.float_format = "{:,.2f}".format

# Exibir resultados
print(df[["peso_kg", "custo_usd", "custo_brl"]])
print(f"\nTotal USD: ${df['custo_usd'].sum():,.2f}")
print(f"Total BRL: R${df['custo_brl'].sum():,.2f}")
