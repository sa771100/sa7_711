import os
import io
import urllib.parse
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك 👋\nأنا بوت مجاني 100% لإنشاء الصور.\n\n"
        "أرسل الأمر بهذا الشكل:\n"
        "`/imagine قطة فضائية`", parse_mode="Markdown"
    )

async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args).strip()
    if not prompt:
        await update.message.reply_text("يرجى كتابة وصف الصورة. مثال:\n/imagine شروق الشمس في الصحراء")
        return

    msg = await update.message.reply_text("⏳ جاري رسم الصورة... يرجى الانتظار")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        
        response = requests.get(image_url)
        
        if response.status_code == 200:
            await update.message.reply_photo(
                photo=io.BytesIO(response.content), 
                caption=f"🎨 {prompt}"
            )
        else:
            await update.message.reply_text("❌ حدث خطأ أثناء توليد الصورة، جرب وصفاً آخر.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")
    finally:
        await msg.delete()

def main():
    if not TELEGRAM_TOKEN:
        print("خطأ: تأكد من إضافة TELEGRAM_TOKEN")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("imagine", imagine))

    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
