import asyncio, sys, base64
from telethon import TelegramClient, functions, types
import qrcode
from aiogram import Bot

try:
    if not (sys.stdout.encoding or '').lower().startswith('utf'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# -----------------------------
# Settings
# -----------------------------
api_id = 64352356
api_hash = 'a09d05a5j50a1d1123cc10gg01e9532l'
session = "SessionName"

sleep_time = 300 #seconds
username = "@AlertEnjoyer"

bot_token = "6452356266:AAH6rTXyDFGVcbsdf542FDD32c"

bot = Bot(token=bot_token)
# channel username (bot must be admin)
notify_chat = "@NotiffdsfdsyRedteqwerisska87Chan"

# -----------------------------
client = TelegramClient(session, api_id, api_hash)

def token_to_url(token: bytes) -> str:
    b64 = base64.urlsafe_b64encode(token).decode().rstrip('=')
    return f"tg://login?token={b64}"

async def qr_login_flow():
    qr_login = await client.qr_login()
    url = getattr(qr_login, 'url', None)

    if not url and hasattr(qr_login, 'token'):
        t = qr_login.token
        url = token_to_url(t) if isinstance(t, bytes) else f"tg://login?token={t}"

    print("\nScan QR code by phone Telegram:\n")

    # Генерация ASCII QR
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    wait = getattr(qr_login, 'wait', None) or getattr(qr_login, 'wait_login', None)
    if callable(wait):
        await wait()

async def checkUser(username, notify_chat):
    first_start = True
    user_amount = 0

    while True:
        res = await client(functions.messages.SearchGlobalRequest(
            q=username,
            filter=types.InputMessagesFilterEmpty(),
            min_date=None,
            max_date=None,
            offset_rate=0,
            offset_peer=types.InputPeerEmpty(),
            offset_id=0,
            limit=2147483647
        ))

        if user_amount != len(res.messages):
            count = len(res.messages) - user_amount
            user_amount = len(res.messages)

            if not first_start and count > 0:
                text = f"New notify: {username[1:]}: {count} times"
                print(text)
                await bot.send_message(chat_id=notify_chat, text=text)
            else:
                first_start = False

        await asyncio.sleep(sleep_time)

async def main():
    await client.connect()

    if not await client.is_user_authorized():
        print("Not autorized")
        await qr_login_flow()

    print("Authorized:", await client.is_user_authorized())

    asyncio.create_task(checkUser(username, notify_chat))
    await client.run_until_disconnected()
    

try:
    asyncio.run(main())
except Exception as e:
    print(f"Error:\n{e}")
