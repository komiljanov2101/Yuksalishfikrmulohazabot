import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin ID larni string ko'rinishidan list[int] ga aylantiramiz
ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id.strip()]
