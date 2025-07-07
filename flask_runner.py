from flask import Flask
import threading
import asyncio
from bot import main  # sizning telegram bot funksiyangiz

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti ✅"

# Telegram botni alohida thread ichida ishga tushuramiz
def run_bot():
    asyncio.run(main())

threading.Thread(target=run_bot).start()
