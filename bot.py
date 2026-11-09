import time
import threading
import telebot
import yfinance as yf

# رمز البوت ومعرف المستخدم
TOKEN = "9290297831:AAHVPbdlGm-dJbTk-uvmFT2qd5uK6mWwezk"
CHAT_ID = "39576"

bot = telebot.TeleBot(TOKEN)

# قائمة الأسهم، الأهداف، ونوع العقد
WATCHLIST = [
    {"symbol": "AAPL", "target": 220.0, "type": "Call"},
    {"symbol": "NVDA", "target": 120.0, "type": "Call"},
    {"symbol": "TSLA", "target": 200.0, "type": "Put"},
    {"symbol": "AMD", "target": 150.0, "type": "Call"},
    {"symbol": "MSFT", "target": 400.0, "type": "Call"},
    {"symbol": "AMZN", "target": 180.0, "type": "Call"},
    {"symbol": "GOOGL", "target": 170.0, "type": "Call"},
    {"symbol": "LLY", "target": 800.0, "type": "Call"},
    {"symbol": "META", "target": 450.0, "type": "Put"},
    {"symbol": "GLD", "target": 220.0, "type": "Call"},
    {"symbol": "MU", "target": 100.0, "type": "Call"}
]

def check_prices():
    while True:
        try:
            for item in WATCHLIST:
                symbol = item["symbol"]
                target = item["target"]
                option_type = item["type"]
                
                ticker = yf.Ticker(symbol)
                todays_data = ticker.history(period="1d")
                
                if not todays_data.empty:
                    current_price = todays_data['Close'].iloc[-1]
                    
                    # التحقق من وصول السعر للهدف حسب نوع العقد
                    if option_type == "Call" and current_price >= target:
                        bot.send_message(CHAT_ID, f"🚨 تنبيه إيجابي (Call)!\nالسهم: {symbol}\nالسعر الحالي: {current_price:.2f}\nالهدف: {target}")
                    elif option_type == "Put" and current_price <= target:
                        bot.send_message(CHAT_ID, f"🚨 تنبيه هبوطي (Put)!\nالسهم: {symbol}\nالسعر الحالي: {current_price:.2f}\nالهدف: {target}")
        except Exception as e:
            print(f"Error: {e}")
        
        # الانتظار لمدة 5 دقائق قبل فحص الأسعار مرة أخرى
        time.sleep(300)

# تشغيل المراقبة في الخلفية
threading.Thread(target=check_prices, daemon=True).start()

if __name__ == "__main__":
    bot.infinity_polling()
