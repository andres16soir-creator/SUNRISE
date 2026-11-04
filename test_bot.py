import os
import django
import asyncio
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SUNRISE.settings')
django.setup()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 ¡Hola! Bot funcionando.')

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('📋 Esto es la ayuda')

async def citas_hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('📅 Mostrando citas de hoy...')

def setup():
    app = Application.builder().token(TOKEN).build()
    
    # REGISTRA LOS HANDLERS EN ORDEN CORRECTO
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('ayuda', ayuda))
    app.add_handler(CommandHandler('citas_hoy', citas_hoy))
    
    return app

async def main():
    app = setup()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print('✅ Bot listo')
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
