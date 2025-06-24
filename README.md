# 🤖 Bitcoin Perpetual Futures Trading Bot

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

A sophisticated Bitcoin perpetual futures analysis bot with Telegram integration. Provides real-time market analysis using multiple trading strategies.

## ✨ Features

- **Real-time Bitcoin perpetual futures analysis**
- **4 Advanced Trading Strategies:**
  - 🚀 Momentum Breakout (Bollinger Bands + RSI)
  - 🔄 Mean Reversion (Statistical extremes)
  - ⚡ Funding Arbitrage (High funding rates)
  - 🎯 Liquidation Hunt (Liquidation cascades)
- **Telegram Bot Interface** with natural language support
- **Professional Risk Management** and position sizing
- **Multi-API Redundancy** (Binance, CoinGecko, Coinbase, CryptoCompare)
- **Secure Environment Variables** for API keys

## 🚀 Quick Deploy to Railway

### Method 1: One-Click Deploy (Recommended)

1. **Click the Deploy button above** or go to [Railway](https://railway.app)
2. **Fork this repository** to your GitHub account
3. **Connect Railway to your GitHub** and select this repository
4. **Set Environment Variables** in Railway dashboard:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```
5. **Deploy!** Railway will automatically build and run your bot

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Set environment variable
railway variables set TELEGRAM_BOT_TOKEN=your_bot_token_here

# Deploy
railway up
```

## 🔧 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bitcoin-trading-bot.git
   cd bitcoin-trading-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your TELEGRAM_BOT_TOKEN
   ```

4. **Run the bot:**
   ```bash
   python telegram_bot.py
   ```

## 🤖 Getting a Telegram Bot Token

1. **Message @BotFather** on Telegram
2. **Send `/newbot`**
3. **Choose a name** for your bot (e.g., "My Bitcoin Bot")
4. **Choose a username** that ends with 'bot' (e.g., "mybitcoin_bot")
5. **Copy the token** and use it as `TELEGRAM_BOT_TOKEN`

## 📱 Bot Commands

- `/start` - Welcome message and bot info
- `/analysis` - Complete Bitcoin futures analysis
- `/price` - Current Bitcoin price only
- `/funding` - Funding rate analysis
- `/help` - Show all commands

**Natural Language:** You can also just type:
- "analyze" or "analysis"
- "check btc" or "btc price"
- "what's the signal?"
- "should I buy?" or "should I sell?"

## 📊 Analysis Output

The bot provides:
- **Current market price** and 24h volume
- **Funding rate** analysis (annual percentage)
- **Multiple strategy signals** with confidence levels
- **Entry prices, stop losses, take profits**
- **Risk management** recommendations
- **Position sizing** calculations

## 🔒 Security Features

- ✅ **No hardcoded tokens** - uses environment variables
- ✅ **No synthetic data** - only real market data
- ✅ **Secure API handling** with multiple fallbacks
- ✅ **Error handling** for API failures

## 📈 Trading Strategies

### 1. Momentum Breakout
- **Bollinger Band breakouts**
- **RSI momentum confirmation**
- **Volume spike validation**
- **Multi-timeframe analysis**

### 2. Mean Reversion
- **Statistical z-score analysis**
- **RSI extreme levels**
- **Bollinger band position**
- **Price deviation from mean**

### 3. Funding Arbitrage
- **High funding rate opportunities**
- **Annual funding calculation**
- **Direction-based recommendations**
- **Funding income estimation**

### 4. Liquidation Hunt
- **Liquidation level estimation**
- **Volume spike confirmation**
- **Volatility analysis**
- **Cascade opportunity detection**

## ⚠️ Disclaimer

**This bot is for educational and informational purposes only.**

- **Not financial advice** - Always do your own research
- **No trading automation** - Manual decision making required
- **Risk management** - Never risk more than you can afford to lose
- **Market volatility** - Cryptocurrency markets are highly volatile

## 🛠️ Technical Details

- **Language:** Python 3.11+
- **Framework:** python-telegram-bot
- **APIs:** Multiple crypto exchange APIs
- **Deployment:** Railway.app ready
- **Data Sources:** Real-time market data only

## 📁 Project Structure

```
bitcoin-trading-bot/
├── telegram_bot.py          # Main Telegram bot
├── bitcoin_perp_trader.py   # Trading analysis engine
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway process definition
├── runtime.txt              # Python version
├── railway.json             # Railway configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | Your Telegram bot token from @BotFather |

## 📞 Support

If you encounter issues:

1. **Check the Railway logs** for error messages
2. **Verify your bot token** is correct
3. **Ensure environment variables** are set properly
4. **Check API connectivity** (some regions may have restrictions)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).