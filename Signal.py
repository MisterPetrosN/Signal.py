import requests
import time
import schedule
import os
import pandas as pd

# Replace <API_KEY> with your CoinMarketCap API key
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": "e7086cae-baa3-4f94-b329-c1cf7be25ac9",
    "convert": "USDT,ETH,BTC",
}


# Define the exchanges to compare prices on
exchanges = [
    "PancakeSwap",
    "Uniswap",
    "MEXC",
    "Gate.io",
    "Kucoin",
    "Bitmart",
    "Ascendex",
    "Binance",
    "Huobi",
    "OKEx",
    "Coinbase",
    "Kraken",
]


# Define the Telegram bot API token and chat ID to receive notifications
telegram_bot_token = "6038653758:AAHNMiGalKgZlNBz8WcBV5n-9K80uTK15Sg"
telegram_chat_id = "-894247839"


# Define a function to send a Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message}
    requests.post(url, data=data)
    print("checking for price changes")


# Define a function to compare the prices of tokens on different exchanges
def compare_prices():
    # Make an API request to get the latest listings on CoinMarketCap
    response = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
        headers=headers,
    )
    data = response.json()["data"]

    # Extract the symbols for all the listed tokens
    symbols = [d["symbol"] for d in data]

    # Make an API request to get the latest market quotes for the tokens
    response = requests.get(
        f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={','.join(symbols)}",
        headers=headers,
    )
    data = response.json()["data"]

    # Extract the prices for each token on each exchange
    prices = {}
    for symbol in symbols:
        prices[symbol] = {}
        for exchange in exchanges:
            try:
                if exchange == "PancakeSwap":
                    price = (
                        data[symbol]["quote"]["BUSD"]["price"]
                        * data[symbol]["quote"]["PANCAKESWAP-BUSD"]["price"]
                    )
                    prices[symbol]["BUSD-PancakeSwap"] = price
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["PANCAKESWAP-USDT"]["price"]
                    )
                    prices[symbol]["USDT-PancakeSwap"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["PANCAKESWAP-ETH"]["price"]
                    )
                    prices[symbol]["ETH-PancakeSwap"] = price
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["PANCAKESWAP-BTC"]["price"]
                    )
                    prices[symbol]["BTC-PancakeSwap"] = price
                elif exchange == "Uniswap":
                    price = (
                        data[symbol]["quote"]["USD"]["price"]
                        * data[symbol]["quote"]["UNI-USD"]["price"]
                    )
                    prices[symbol]["USD-Uniswap"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["UNI-ETH"]["price"]
                    )
                    prices[symbol]["ETH-Uniswap"] = price
                elif exchange == "MEXC":
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["MEXC-USDT"]["price"]
                    )
                    prices[symbol]["USDT-MEXC"] = price
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["MEXC-BTC"]["price"]
                    )
                    prices[symbol]["BTC-MEXC"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["MEXC-ETH"]["price"]
                    )
                    prices[symbol]["ETH-MEXC"] = price
                elif exchange == "Gate.io":
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["GATE-USDT"]["price"]
                    )
                    prices[symbol]["USDT-Gate.io"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["GATE-ETH"]["price"]
                    )
                    prices[symbol]["ETH-Gate.io"] = price
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["GATE-BTC"]["price"]
                    )
                    prices[symbol]["BTC-Gate.io"] = price
                elif exchange == "Kucoin":
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["KUCOIN-USDT"]["price"]
                    )
                    prices[symbol]["USDT-Kucoin"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["KUCOIN-ETH"]["price"]
                    )
                    prices[symbol]["ETH-Kucoin"] = price
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["KUCOIN-BTC"]["price"]
                    )
                    prices[symbol]["BTC-Kucoin"] = price
                elif exchange == "Bitmart":
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["BITMART-USDT"]["price"]
                    )
                    prices[symbol]["USDT-Bitmart"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["BITMART-ETH"]["price"]
                    )
                    prices[symbol]["ETH-Bitmart"] = price
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["BITMART-BTC"]["price"]
                    )
                    prices[symbol]["BTC-Bitmart"] = price
                elif exchange == "Ascendex":
                    price = (
                        data[symbol]["quote"]["USDT"]["price"]
                        * data[symbol]["quote"]["ASCENDEX-USDT"]["price"]
                    )
                    prices[symbol]["USDT-Ascendex"] = price
                    price = (
                        data[symbol]["quote"]["ETH"]["price"]
                        * data[symbol]["quote"]["ASCENDEX-ETH"]["price"]
                    )
                    price = (
                        data[symbol]["quote"]["BTC"]["price"]
                        * data[symbol]["quote"]["ASCENDEX-BTC"]["price"]
                    )
                    prices[symbol]["BTC-Ascendex"] = price
                else:
                    price = data[symbol]["quote"][convert]["price"]
                    prices[symbol][f"{convert}-{exchange}"] = price
            except:
                pass


# Create a DataFrame to store the prices
df = pd.DataFrame(prices)

# Transpose the DataFrame so that the tokens are in rows and the prices are in columns
df = df.T

# Convert the index to a column
df.reset_index(inplace=True)

# Rename the columns
df.columns = ["Token"] + [
    f"{exchange}-{convert}"
    for exchange in exchanges
    for convert in ["USDT", "ETH", "BTC"]
]

# Set the token symbol as the index
df.set_index("Token", inplace=True)

# Determine which tokens have the largest price changes on each exchange
changes = pd.DataFrame(columns=["Token", "Exchange", "Change"])
for exchange in exchanges:
    for convert in ["USDT", "ETH", "BTC"]:
        # Calculate the percent change in price for each token
        pct_changes = df[f"{exchange}-{convert}"].pct_change()

        # Determine the token with the largest price change
        max_change = pct_changes.abs().idxmax()
        change = pct_changes.loc[max_change]

        # Add the token with the largest price change to the DataFrame
        changes = changes.append(
            {"Token": max_change, "Exchange": exchange, "Change": change},
            ignore_index=True,
        )

# Sort the DataFrame by the largest price changes
changes = changes.sort_values(by="Change", ascending=False)

# Create a message to send via Telegram with the largest price changes
message = ""
for exchange in exchanges:
    message += f"Exchange: {exchange}\n"
    message += "Token | Change\n"
    message += "------|-------\n"
    for _, row in changes[changes["Exchange"] == exchange].iterrows():
        token = row["Token"]
        change = row["Change"]
        message += f"{token} | {change:.2%}\n"
    message += "\n"

# Send the message via Telegram
send_telegram_message(message)
