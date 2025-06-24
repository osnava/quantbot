# Bitcoin Perpetual Futures Trading Bot

## Features
- Real-time Bitcoin perpetual futures analysis
- 4 advanced trading strategies (Momentum, Mean Reversion, Funding Arbitrage, Liquidation Hunt)
- Telegram bot interface with natural language support
- Professional risk management and position sizing

## Usage
Send `/start` to the bot and use:
- `/analysis` - Complete trading analysis
- `/price` - Current Bitcoin price
- `/funding` - Funding rate info
- Or just type "analyze" or "check btc"

## Deployment
This bot is configured for Railway deployment with:
- `Procfile` - Defines worker process
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version

## Commands
- `/start` - Welcome message
- `/analysis` - Full market analysis
- `/price` - Current price only
- `/funding` - Funding rate analysis
- `/help` - Help and commands