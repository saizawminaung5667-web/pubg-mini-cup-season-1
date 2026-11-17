
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6388650807

teams = {}
results = {}
TOTAL_MATCHES = 6

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 PUBG MINI CUP SEASON 1\n\n"
        "/addteam - Register team\n"
        "/teams - View teams\n"
        "/match - Match status\n"
        "/result - Submit result screenshot\n"
        "/leaderboard - Ranking\n"
        "/help - Help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 PUBG MINI CUP SEASON 1\n"
        "အသင်း 25 သင်း၊ Match 6 ပွဲ\n"
        "Result Screenshot ကို Admin ထံပို့ပါ။"
    )

async def addteam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Admin only!")
        return

    name = " ".join(context.args)
    if not name:
        await update.message.reply_text("အသင်းနာမည် ထည့်ပါ။")
        return

    if name in teams.values():
        await update.message.reply_text("အသင်းရှိပြီးသားပါ။")
        return

    if len(teams) >= 25:
        await update.message.reply_text("အသင်း 25 သင်း ပြည့်ပါပြီ။")
        return

    teams[len(teams) + 1] = name
    await update.message.reply_text(f"✅ {name} Registered!")

async def teamlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not teams:
        await update.message.reply_text("အသင်းမရှိသေးပါ။")
        return

    msg = "🏆 REGISTERED TEAMS\n\n"
    for number, name in teams.items():
        msg += f"{number}. {name}\n"

    await update.message.reply_text(msg)

async def match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 PUBG MINI CUP SEASON 1\n"
        "Total Matches: 6\n"
        "Result များကို Admin က အတည်ပြုပေးပါမည်။"
    )

async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Match Result Screenshot ပို့ပေးပါ။\n"
        "Admin က စစ်ဆေးပြီး အတည်ပြုပေးပါမည်။"
    )

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏆 LEADERBOARD\n\n"
        "Result အတည်ပြုပြီးပါက Ranking ပြသပါမည်။"
    )

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(
            "Screenshot လက်ခံရရှိပါပြီ။\n"
            "Result ကို စစ်ဆေးပြီး နောက်တစ်ဆင့် ဆက်လုပ်ပါ။"
        )
    else:
        await update.message.reply_text(
            "Screenshot လက်ခံရရှိပါပြီ။ Admin ထံ စစ်ဆေးရန် ပို့ပေးပါမည်။"
        )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("addteam", addteam))
    app.add_handler(CommandHandler("teams", teamlist))
    app.add_handler(CommandHandler("match", match))
    app.add_handler(CommandHandler("result", result))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
def placement_points(rank):
    points = {
        1: 10,
        2: 6,
        3: 5,
        4: 4,
        5: 3,
        6: 2,
        7: 1,
        8: 1
    }
    return points.get(rank, 0)

def calculate_total(rank, kills):
    return placement_points(rank) + kills
