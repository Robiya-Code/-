from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "SENING_TOKENING"

# Savollar
questions = [
    {
        "question": "Choose correct answer: She ___ to school every day.",
        "options": ["A) go", "B) goes", "C) going"],
        "answer": "B"
    },
    {
        "question": "Choose correct answer: I ___ my homework yesterday.",
        "options": ["A) did", "B) do", "C) done"],
        "answer": "A"
    }
]

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to IELTS Bot!\n\n/start_test ni bosing test boshlash uchun."
    )

# Test boshlash
async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["q_index"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)

# Savol yuborish
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q_index = context.user_data["q_index"]

    if q_index < len(questions):
        q = questions[q_index]
        keyboard = [[opt] for opt in q["options"]]

        await update.message.reply_text(
            q["question"],
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
    else:
        score = context.user_data["score"]
        await update.message.reply_text(f"✅ Test tugadi!\nSizning natijangiz: {score}/{len(questions)}")

# Javobni tekshirish
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text[0]  # A, B, C
    q_index = context.user_data.get("q_index", 0)

    if q_index < len(questions):
        correct = questions[q_index]["answer"]

        if user_answer == correct:
            context.user_data["score"] += 1
            await update.message.reply_text("✅ To‘g‘ri!")
        else:
            await update.message.reply_text(f"❌ Noto‘g‘ri! To‘g‘ri javob: {correct}")

        context.user_data["q_index"] += 1
        await send_question(update, context)

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start_test", start_test))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

app.run_polling()
