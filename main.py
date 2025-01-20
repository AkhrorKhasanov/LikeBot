import os
TOKEN = os.getenv("TOKEN")
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
user_scores = {}
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! You can send me only '👍' (like) or '👎' (dislike) emojis. I'll track your votes.")
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text
    if text == '👍':
        if user_id not in user_scores:
            user_scores[user_id] = {'like': 0, 'dislike': 0}
        user_scores[user_id]['like'] += 1
        await update.message.reply_text("Thank you for your like! 👍")
    elif text == '👎':
        if user_id not in user_scores:
            user_scores[user_id] = {'like': 0, 'dislike': 0}
        user_scores[user_id]['dislike'] += 1
        await update.message.reply_text("Thank you for your dislike! 👎")
    else:
        await update.message.reply_text("Error: Please send only '👍' (like) or '👎' (dislike) emojis.")
    like_count = user_scores[user_id].get('like', 0)
    dislike_count = user_scores[user_id].get('dislike', 0)
    await update.message.reply_text(f"Your current votes:\n👍 {like_count} Likes\n👎 {dislike_count} Dislikes")
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
if __name__ == '__main__':
    main()
