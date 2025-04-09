import asyncio
import nest_asyncio

from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ApplicationHandlerStop, ContextTypes
)
import telegram
import json
import logging
from telegram import Update
from telegram.error import TimedOut
import httpx
import os
from dotenv import load_dotenv

from handlers import start, handle_text, handle_phone_number
from database_operations import initiate_connection

# Load environment variables
load_dotenv()

# ✅ Maintenance flag
MAINTENANCE_MODE = False  # Set to False when done with updates

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


# ✅ Maintenance mode response
async def maintenance_reply(update: Update):
    if update.message:
        await update.message.reply_text("Ողջույն: Ես Իննովա Մենեջմենթի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ համատիրության ընթացիկ պարտքի կամ կանխավճարի, վճարումների մասին և այլ օգտակար ինֆորմացիա համատիրության աշխատանքների մասին։⛔ Այս պահին մեր տելեգրամյան բոտի վրա կատարվում են տեխնիկական աշխատանքներ, խնդրում ենք փորձել ավելի ուշ։")
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Ողջույն: Ես Իննովա Մենեջմենթի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ համատիրության ընթացիկ պարտքի կամ կանխավճարի, վճարումների մասին և այլ օգտակար ինֆորմացիա համատիրության աշխատանքների մասին։⛔ Այս պահին մեր տելեգրամյան բոտի վրա կատարվում են տեխնիկական աշխատանքներ, խնդրում ենք փորձել ավելի ուշ։")


# ✅ Global error handler
async def global_exception_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Unhandled exception: {context.error}")

    if isinstance(context.error, (telegram.error.TimedOut, httpx.Timeout)):
        logger.error("Timeout detected.. Restarting interaction.")
        if isinstance(update, Update):
            await start(update, context)

    raise ApplicationHandlerStop()


# ✅ Wrapper to check for maintenance
def wrap_with_maintenance(handler_func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if MAINTENANCE_MODE:
            await maintenance_reply(update)
            return
        await handler_func(update, context)
    return wrapper


async def main():
    """Start the bot."""
    # Load bot token from credentials.json
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            BOT_TOKEN = credentials.get("bot_token")
            if not BOT_TOKEN:
                raise ValueError("Bot token not found in credentials.json")
            logger.info("Successfully loaded bot token from credentials.json")
    except Exception as e:
        logger.error(f"Failed to load bot token: {str(e)}")
        raise

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", wrap_with_maintenance(start)))
    
    # Add contact message handler
    application.add_handler(MessageHandler(filters.CONTACT, wrap_with_maintenance(handle_phone_number)))
    
    # Add text message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wrap_with_maintenance(handle_text)))

    # Register global exception handler
    application.add_error_handler(global_exception_handler)

    # Start the Bot
    logger.info("Starting bot...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot stopped successfully!")


def run_bot():
    """Run the bot with proper error handling."""
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Patch the running event loop
        nest_asyncio.apply()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {str(e)}")
        raise


if __name__ == '__main__':
    run_bot()
