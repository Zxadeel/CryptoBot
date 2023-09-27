# CryptoBot - Discord Cryptocurrency Price Bot

CryptoBot is a Discord bot that provides real-time cryptocurrency price information using the CoinMarketCap API. It allows users to easily check the current prices of various cryptocurrencies within their Discord server.

## Features

- Retrieve real-time cryptocurrency prices.
- Support for a wide range of cryptocurrencies available on CoinMarketCap.
- Easy-to-use commands for accessing cryptocurrency price data.
- Customizable notifications and alerts for specific cryptocurrency price changes.

## Getting Started

To get CryptoBot up and running in your Discord server, follow these steps:

1. **Clone the Repository:**
```
  git clone https://github.com/Zxadeel/CryptoBot.git
```
3. **Install Dependencies:**
  Make sure you have python and pip installed. Run these commands in a terminal:
   **Discord.py**
    Windows:
   ```
   py -3 -m pip install -U discord.py
   ```
    Other:
   ```
   python3 -m pip install -U discord.py
    ```
5. **Configuration:**
- Create a Discord Bot on the [Discord Developer Portal](https://discord.com/developers/applications).
- Generate an API key on the [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/).
- Configure your bot token and CoinMarketCap API key in a `.env` file.

4. **Run the Bot:**
```
py CryptoBot.py
```

## Usage

CryptoBot offers various commands to interact with the bot. Here are some examples:

- Check the price of Bitcoin: !price <name of coin>

