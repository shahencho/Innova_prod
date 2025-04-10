from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Create a button that requests the user's phone number
    keyboard = [[KeyboardButton("Share Phone Number", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Please verify your identity by sharing your phone number:",
        reply_markup=reply_markup
    )

async def phone_number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number
    
    # Store the phone number in your database associated with the user's ID
    user_id = update.effective_user.id
    
    # Here you would verify the phone number however you need
    # For example, check if it's in your allowed users database
    
    await update.message.reply_text(f"Thank you! Your phone number {phone} has been verified.")
    # Continue with authenticated experience...

def main():
    app = ApplicationBuilder().token("xxxx").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, phone_number_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
