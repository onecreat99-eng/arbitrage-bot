import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import telegram
from datetime import datetime

# 🔐 Telegram Bot Details
BOT_TOKEN = "7668611215:AAHoLluW3WtUWDYZTM-uSgO_QTjZF8Y1oPY"
CHAT_ID = "7244013092"

# ✅ Google Sheet Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 🔗 Sheet Connection
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1DYf0r2MtIvnX_VhUe0jrlMbukT0bMa0YD-JJPNTuwvU/edit").worksheet("Sheet1")

# 🟢 Telegram Bot Init
bot = telegram.Bot(token=BOT_TOKEN)

# ✅ Emoji Icons
green_circle = "🟢"   # Live
blue_circle = "🔵"    # Prematch
red_circle = "🔴"     # Same bookmaker
white_circle = "⚪"   # Default

# 🔁 Track Already Sent Rows
sent_rows = set()

while True:
    data = sheet.get_all_records()

    for idx, row in enumerate(data):
        if idx in sent_rows:
            continue

        match = row.get("Match", "Unknown Match")
        market = row.get("Market", "Unknown Market")
        side1 = row.get("Side1", "Team A")
        side2 = row.get("Side2", "Team B")
        bm1 = row.get("BM1", "Bookmaker 1")
        odds1 = row.get("Odds1", "")
        bm2 = row.get("BM2", "Bookmaker 2")
        odds2 = row.get("Odds2", "")
        profit = row.get("Profit %", "")
        match_type = row.get("Type", "")
        live_match = row.get("Live Match?", "")
        same_bookmaker = row.get("Same Bookmaker?", "")

        # 💚 Match Type Emoji
        if live_match.strip().lower() == "yes":
            match_type_emoji = green_circle
        elif match_type.strip().lower() == "prematch":
            match_type_emoji = blue_circle
        else:
            match_type_emoji = white_circle

        # 🔴 Same Bookmaker Emoji
        if same_bookmaker.strip().lower() == "yes":
            same_bookmaker_emoji = red_circle
        else:
            same_bookmaker_emoji = white_circle

        # 📅 Current Time
        now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        # 📩 Final Message
        message = f"""
📢 *Arbitrage अलर्ट!*

🏟️ *मैच:* {match}
🎯 *मार्केट:* {market}
📌 {side1} ({bm1}): {odds1}
📌 {side2} ({bm2}): {odds2}
💰 *प्रॉफिट %:* {profit}
{match_type_emoji} *टाइप:* {"Live" if live_match.lower() == "yes" else "Prematch"}
{same_bookmaker_emoji} *सेम बुकमेकर:* {"Yes" if same_bookmaker.lower() == "yes" else "No"}
🕒 *टाइम:* {now}
        """

        # 🚀 Send message
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

        sent_rows.add(idx)

    time.sleep(10)
