#!/usr/bin/env python3
"""
Bitcoin Perpetual Futures Telegram Bot
Telegram bot that provides Bitcoin perpetual futures analysis on demand
"""

import asyncio
import logging
import os
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import io
import sys
from datetime import datetime
import traceback

# Load environment variables from .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip (Railway loads env vars automatically)
    pass

# Import our trading system
from bitcoin_perp_trader import BitcoinPerpTrader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramTradingBot:
    def __init__(self, token: str):
        self.token = token
        self.trader = BitcoinPerpTrader(initial_capital=10000)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 **Bitcoin Perpetual Futures Trading Bot**

Welcome! I can provide real-time Bitcoin perpetual futures analysis.

**Available Commands:**
• `/analysis` - Get complete trading analysis
• `/price` - Get current Bitcoin price
• `/funding` - Get current funding rate
• `/help` - Show this help message

**Quick Analysis:**
Just type "analyze", "check btc", or "what's the signal?" and I'll run the analysis for you!

The system analyzes:
• Momentum breakout opportunities
• Mean reversion signals  
• Funding rate arbitrage
• Liquidation hunt setups

⚠️ **Disclaimer:** This is for educational purposes only. Always do your own research before trading.
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📊 **Bitcoin Perpetual Futures Bot - Help**

**Commands:**
• `/start` - Welcome message and bot info
• `/analysis` - Complete trading analysis
• `/price` - Current Bitcoin price only
• `/funding` - Current funding rate info
• `/help` - This help message

**Natural Language:**
You can also just type:
• "analyze" or "analysis"
• "check btc" or "btc price"
• "what's the signal?"
• "funding rate"
• "should I buy?" or "should I sell?"

**About the Analysis:**
The bot runs 4 advanced trading strategies:
1. **Momentum Breakout** - Bollinger bands + RSI
2. **Mean Reversion** - Statistical extremes
3. **Funding Arbitrage** - High funding rates
4. **Liquidation Hunt** - Liquidation cascades

Each strategy includes proper risk management and position sizing recommendations.

⚡ **Response Time:** Analysis takes 5-10 seconds to fetch real-time data and calculate indicators.
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analysis command - run complete analysis"""
        await self.run_complete_analysis(update)
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /price command - get current price only"""
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            market_data = self.trader.fetch_perpetual_data()
            
            if market_data:
                price_message = f"""
💰 **Bitcoin Perpetual Futures Price**

**Current Price:** ${market_data.price:,.2f}
**24h Volume:** ${market_data.volume_24h:,.0f}
**Open Interest:** ${market_data.open_interest:,.0f}
**Funding Rate:** {market_data.funding_rate:.6f} ({market_data.funding_rate*365*3*100:.1f}% annually)

*Last updated: {datetime.now().strftime('%H:%M:%S UTC')}*

Type `/analysis` for complete trading analysis!
                """
                await update.message.reply_text(price_message, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ Failed to fetch price data. Please try again.")
                
        except Exception as e:
            logger.error(f"Error in price command: {e}")
            await update.message.reply_text("⚠️ Error fetching price data. Please try again later.")
    
    async def funding_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /funding command - get funding rate info"""
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            market_data = self.trader.fetch_perpetual_data()
            
            if market_data:
                annual_rate = market_data.funding_rate * 365 * 3 * 100
                daily_rate = market_data.funding_rate * 3 * 100
                
                # Determine funding direction
                if market_data.funding_rate > 0:
                    direction = "📈 **Longs pay Shorts**"
                    recommendation = "Consider SHORT positions for funding income"
                elif market_data.funding_rate < 0:
                    direction = "📉 **Shorts pay Longs**"
                    recommendation = "Consider LONG positions for funding income"
                else:
                    direction = "⚖️ **Neutral Funding**"
                    recommendation = "No funding arbitrage opportunity"
                
                # Funding analysis
                if abs(annual_rate) > 20:
                    opportunity = "🔥 **EXTREME** - High arbitrage opportunity"
                elif abs(annual_rate) > 10:
                    opportunity = "⚡ **HIGH** - Good arbitrage opportunity"
                elif abs(annual_rate) > 5:
                    opportunity = "📊 **MODERATE** - Moderate opportunity"
                else:
                    opportunity = "😐 **LOW** - Normal funding levels"
                
                funding_message = f"""
⚡ **Bitcoin Funding Rate Analysis**

**Current Rate:** {market_data.funding_rate:.6f}
**Daily Rate:** {daily_rate:.3f}%
**Annualized:** {annual_rate:.1f}%

{direction}

**Opportunity Level:** {opportunity}

**Recommendation:** {recommendation}

**Next Funding:** ~{market_data.funding_countdown // (1000 * 60 * 60)} hours

*Funding is paid every 8 hours*
                """
                await update.message.reply_text(funding_message, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text("❌ Failed to fetch funding data. Please try again.")
                
        except Exception as e:
            logger.error(f"Error in funding command: {e}")
            await update.message.reply_text("⚠️ Error fetching funding data. Please try again later.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural language messages"""
        text = update.message.text.lower()
        
        # Keywords that trigger analysis
        analysis_keywords = ['analyze', 'analysis', 'signal', 'should i buy', 'should i sell', 
                           'trade', 'trading', 'strategy', 'recommendation']
        
        price_keywords = ['price', 'btc', 'bitcoin', 'current price', 'check btc']
        
        funding_keywords = ['funding', 'funding rate', 'arbitrage', 'funding income']
        
        if any(keyword in text for keyword in analysis_keywords):
            await self.run_complete_analysis(update)
        elif any(keyword in text for keyword in price_keywords):
            await self.price_command(update, context)
        elif any(keyword in text for keyword in funding_keywords):
            await self.funding_command(update, context)
        else:
            # Default response for unrecognized messages
            await update.message.reply_text(
                "🤔 I didn't understand that. Try:\n"
                "• `/analysis` for complete analysis\n"
                "• `/price` for current price\n"
                "• `/help` for all commands\n"
                "• Or just type 'analyze' for quick analysis!"
            )
    
    async def run_complete_analysis(self, update: Update):
        """Run the complete Bitcoin perpetual futures analysis"""
        try:
            # Show typing indicator
            await update.message.reply_text("🔄 Analyzing Bitcoin perpetual futures... This may take a few seconds.")
            
            # Capture the output from our trading system
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            try:
                # Run the analysis
                result = self.trader.run_analysis()
                
                # Get captured output
                captured_text = captured_output.getvalue()
                
                # Restore stdout
                sys.stdout = old_stdout
                
                # Check if we got valid results
                if not result or len(result) != 2:
                    await update.message.reply_text(
                        "⚠️ Failed to fetch market data. This could be due to:\n"
                        "• API connectivity issues\n"
                        "• Market data unavailable\n"
                        "• Network problems\n\n"
                        "Please try again in a few moments."
                    )
                    return
                
                strategies, market_data = result
                
                # Validate data
                if not strategies or not market_data:
                    await update.message.reply_text(
                        "⚠️ Incomplete market data received. Please try again."
                    )
                    return
                
                # Format the analysis for Telegram
                telegram_message = self.format_analysis_for_telegram(strategies, market_data)
                
                # Send the analysis
                await update.message.reply_text(telegram_message, parse_mode=ParseMode.MARKDOWN)
                
            except Exception as e:
                sys.stdout = old_stdout
                logger.error(f"Error running analysis: {e}")
                traceback.print_exc()
                await update.message.reply_text(
                    f"⚠️ Error running analysis: {str(e)}\n"
                    "Please try again later or contact support."
                )
                
        except Exception as e:
            logger.error(f"Error in run_complete_analysis: {e}")
            await update.message.reply_text("❌ Failed to run analysis. Please try again.")
    
    def format_analysis_for_telegram(self, strategies, market_data):
        """Format the analysis output for Telegram"""
        
        # Get best strategy
        best_strategy = self.trader.select_best_strategy(strategies)
        
        # Header
        message = f"""
📊 **Bitcoin Perpetual Futures Analysis**
*{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*

💰 **Market Data:**
• **Price:** ${market_data.price:,.2f}
• **24h Volume:** ${market_data.volume_24h:,.0f}
• **Open Interest:** ${market_data.open_interest:,.0f}
• **Funding Rate:** {market_data.funding_rate:.6f} ({market_data.funding_rate*365*3*100:.1f}% annually)

📈 **Strategy Analysis:**
        """
        
        # Add each strategy
        strategy_emojis = {
            'momentum': '🚀',
            'mean_reversion': '🔄', 
            'funding_arbitrage': '⚡',
            'liquidation_hunt': '🎯'
        }
        
        for name, signal in strategies.items():
            emoji = strategy_emojis.get(name, '📊')
            strategy_name = name.replace('_', ' ').title()
            
            message += f"\n{emoji} **{strategy_name}:**\n"
            message += f"   Action: **{signal.action}**\n"
            message += f"   Confidence: {signal.confidence:.1%}\n"
            
            if signal.action != 'HOLD':
                message += f"   Leverage: {signal.leverage:.1f}x\n"
                message += f"   Risk/Reward: {signal.risk_reward_ratio:.2f}\n"
            
            # Add main reasoning
            if signal.strategy_reasoning:
                message += f"   Reason: {signal.strategy_reasoning[0]}\n"
        
        # Best recommendation
        message += f"\n🎯 **RECOMMENDED ACTION:**\n"
        message += f"**Strategy:** {best_strategy.strategy_name}\n"
        message += f"**Action:** {best_strategy.action}\n"
        
        if best_strategy.action != 'HOLD':
            message += f"**Entry:** ${best_strategy.entry_price:,.2f}\n"
            message += f"**Leverage:** {best_strategy.leverage:.1f}x\n"
            message += f"**Stop Loss:** ${best_strategy.stop_loss:,.2f}\n"
            
            if best_strategy.take_profit:
                tp_levels = [f"${tp:,.2f}" for tp in best_strategy.take_profit[:2]]
                message += f"**Take Profits:** {', '.join(tp_levels)}\n"
            
            message += f"**Confidence:** {best_strategy.confidence:.1%}\n"
            message += f"**Max Risk:** ${best_strategy.max_risk:.2f}\n"
            
            if best_strategy.funding_cost != 0:
                cost_type = "Income" if best_strategy.funding_cost < 0 else "Cost"
                message += f"**Funding {cost_type}:** ${abs(best_strategy.funding_cost):.2f}\n"
        
        # Add reasoning
        message += f"\n💡 **Reasoning:**\n"
        for reason in best_strategy.strategy_reasoning[:2]:  # Limit to 2 reasons for Telegram
            message += f"• {reason}\n"
        
        # Add disclaimer
        message += f"\n⚠️ **Disclaimer:** Educational purposes only. DYOR before trading."
        
        return message
    
    def run_bot(self):
        """Run the Telegram bot"""
        # Create application
        application = Application.builder().token(self.token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("analysis", self.analysis_command))
        application.add_handler(CommandHandler("price", self.price_command))
        application.add_handler(CommandHandler("funding", self.funding_command))
        
        # Add message handler for natural language
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Set bot commands for menu
        async def set_commands():
            commands = [
                BotCommand("start", "Welcome message and bot info"),
                BotCommand("analysis", "Complete Bitcoin futures analysis"),
                BotCommand("price", "Current Bitcoin price"),
                BotCommand("funding", "Current funding rate info"),
                BotCommand("help", "Show help and available commands")
            ]
            await application.bot.set_my_commands(commands)
        
        # Run the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    
    # Get bot token from environment variable
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
        print("\n📋 To set your bot token:")
        print("1. Get a token from @BotFather on Telegram:")
        print("   - Message @BotFather")
        print("   - Send /newbot")
        print("   - Choose a name and username for your bot")
        print("   - Copy the token")
        print("\n2. Set the environment variable:")
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("   # OR for Windows:")
        print("   set TELEGRAM_BOT_TOKEN=your_token_here")
        print("\n3. Then run: python3 telegram_bot.py")
        print("\n🔒 This keeps your token secure and out of the code!")
        return
    
    # Create and run bot
    bot = TelegramTradingBot(BOT_TOKEN)
    
    print("🤖 Starting Bitcoin Perpetual Futures Telegram Bot...")
    print("📱 Bot is running! Send /start to begin.")
    print("🌐 Deployed on Railway - Running 24/7")
    print("🛑 Press Ctrl+C to stop the bot")
    
    try:
        bot.run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()