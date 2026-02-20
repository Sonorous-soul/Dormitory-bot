import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")
ADMIN_UIDS = [583776424, 8300314322, 975531466]

START, NAME_AND_ID, BLOCK_AND_DORM_NO, ISSUE_REPORT, ISSUE_ALREADY_REPORT,LOST_AND_FOUND, FOUND_DESC, FOUND_PHOTO, FOUND_REPORTED, LOST_REPORTED = range(10)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Get Info", "Report an Issue", "Lost Item", "Found Item"]]


    await update.message.reply_text(
        "Hi! I'm 5kilo dormitory Bot. How can I help you? "
        "Send /cancel to stop talking to me.\n\n"
        "Do you want to get info or report an issue?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Info, Issue"
        ),
    )

    return START


async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s: chose %s", user.first_name, update.message.text)

    message = """
አዲስ አበባ ዩኒቨርስቲ \n\n
የአዲስ አበባ ቴክኖሎጂ ኢንስቲትዩት (AAiT) ዶርሚተሪ አስተዳደር
ውድ የኢንስቲትዩታችን ተማሪዎች፤
የዶርም ህይወት በዩኒቨርሲቲ ቆይታችሁ ትልቁን ድርሻ ይይዛል። በመሆኑም ቆይታችሁ ውጤታማ፣ ሰላማዊ እና ምቹ እንዲሆን በብሎካችን ውስጥ የሚከተሉትን የዲሲፕሊን መመሪያዎች ተግባራዊ እንድታደርጉ እናሳስባለን።

1. ጽዳትና ውበት (Hygiene & Sanitation)
የክፍል ንጽህና፦ እያንዳንዱ ተማሪ የገዛ ክፍሉን ንጽህና የመጠበቅ ኃላፊነት አለበት። ቆሻሻን በየኮሪደሩ ወይም በየመስኮቱ መጣል በጥብቅ የተከለከለ ነው።

የጋራ መጠቀሚያዎች፦ መጸዳጃ ቤቶችን እና የመታጠቢያ ክፍሎችን ስንጠቀም ለቀጣዩ ሰው በሚመች እና በንጹህ ሁኔታ መሆን አለበት።

የቆሻሻ አወጋገድ፦ ትላልቅ ቆሻሻዎችን እና የምግብ ትርፍራፊዎችን በየመታጠቢያ ገንዳው (Sink) ውስጥ ከመጣል እንቆጠብ፤ ይህ የቧንቧ መታፈንን ያስከትላል።

2. የደህንነት ጥበቃ (Security Awareness)
በርን መቆለፍ፦ ለጥቂት ደቂቃም ቢሆን ከክፍል ሲወጡ በርዎን መቆለፍዎን ያረጋግጡ።
ውድ ንብረቶች፦ ላፕቶፕ፣ ስልክ እና ሌሎች ኤሌክትሮኒክስ ዕቃዎችን በማይታይ ቦታ ወይም በሎከር ውስጥ ያስቀምጡ። ለሚጠፉ ንብረቶች ተማሪው ቀዳሚውን ኃላፊነት ይወስዳል።

እንግዶች፦ ወደ ብሎኩ የሚገቡ እንግዶችን የመቆጣጠር ኃላፊነት የሁላችንም ነው። ማንነቱ ያልታወቀ ሰው ሲያዩ ለጥበቃ ሰራተኞች ጥቆማ ይስጡ።

3. የእሳት እና የኤሌክትሪክ አደጋ ጥንቃቄ
የተከለከሉ እቃዎች፦ በዶርም ውስጥ የኤሌክትሪክ ምጣድ፣ ኮይል፣ የውሃ ማሞቂያ (Boiler) እና ከባድ ማሞቂያዎችን መጠቀም በህግ ያስቀጣል።

ጥንቃቄ፦ ክፍሉን ለቀው ሲወጡ ማንኛውንም አይነት ስዊች ማጥፋትዎን እና ቻርጀሮችን ከሶኬት መንቀልዎን ያረጋግጡ።

4. የሰላም እና የጥናት ድባብ
ፀጥታን መጠበቅ፦ ዶርም ተማሪዎች የሚያርፉበት እና የሚያጠኑበት ቦታ ነው። ከምሽቱ 2:00 ሰዓት በኋላ ጩኸት፣ ከፍተኛ የሙዚቃ ድምፅ እና ረብሻ መፍጠር ተገቢ አይደለም።
የአብሮነት ባህል፦ ከዶርም ጓደኞችዎ ጋር በመከባበር እና በመረዳዳት ይኑሩ። አለመግባባቶች ሲፈጠሩ በውይይት ወይም በፕሮክተር አማካኝነት ይፍቱ።

5. የዩኒቨርሲቲ ንብረት ጥበቃ
አያያዝ፦ አልጋዎች፣ ሎከሮች፣ ጠረጴዛዎች እና ወንበሮች የጋራ ንብረቶቻችን ናቸው። በእነዚህ ንብረቶች ላይ ጽሁፍ መጻፍ ወይም ጉዳት ማድረስ ያስጠይቃል።

ሪፖርት ማድረግ፦ የውሃ ቧንቧ ፍሳሽ፣ የኤሌክትሪክ መስመር ብልሽት ወይም የተሰበረ መስኮት ካለ በፍጥነት ለፕሮክተር ቢሮ ያሳውቁ።
"የእርስዎ ስነ-ምግባር ለሌሎች ምሳሌ ይሁን!"
ለጥያቄም ሆነ ለተጨማሪ መረጃ የፕሮክተር ቢሮ ሁልጊዜ ክፍት ነው።
መልካም የትምህርት ጊዜ!

የ AAiT ዶርሚተሪ አስተዳደር።
    """

    if update.message.text == "Get Info":
        reply_keyboard = [["Get Info", "Report an Issue", "Lost and Found", "Found Item"]]

        await update.message.reply_text(
        message
         )

        await update.message.reply_text(
        "What would you like to do next?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
        )

        return START


    elif update.message.text == "Report an Issue":
        context.user_data['username'] = update.message.from_user

        await update.message.reply_text(
            "You are now reporting an Issue!\nPlease enter name and id",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NAME_AND_ID

    elif update.message.text == "Lost Item":
        context.user_data['username'] = update.message.from_user

        await update.message.reply_text(
            "You are now in Report lost item!\nWhat did you lose?",
            reply_markup=ReplyKeyboardRemove(),
        )
        return LOST_AND_FOUND
    elif update.message.text == "Found Item":
        context.user_data['username'] = update.message.from_user

        await update.message.reply_text(
        "You are reporting a FOUND item.\n\n"
        "Please describe the item you found.",
        reply_markup=ReplyKeyboardRemove(),
    )
        return FOUND_DESC

    

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "You've canceled the conversation!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def lost_and_found(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Lost & Found report from %s: %s", user.first_name, update.message.text)

    context.user_data['lost_item'] = update.message.text

    await update.message.reply_text(
        "Thank you! Your lost item report has been received.\n"
        "If someone finds it, the administration will contact you.\n\n"
        "Send /start to go back to the main menu."
    )

    lost_report = {
        'username': user.username,
        'lost_item': context.user_data['lost_item'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    admin_message = (
        f"Lost & Found Report\n\n"
        f"Telegram Username: @{lost_report['username']}\n"
        f"Lost Item: {lost_report['lost_item']}\n"
        f"Submitted at: {lost_report['timestamp']}"
    )

    for admin_uid in ADMIN_UIDS:
        await context.bot.send_message(
            chat_id=admin_uid,
            text=admin_message
        )

    return LOST_REPORTED

async def lost_already_reported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Your lost item has already been reported.\n"
        "Send /start to return to the main menu."
    )
    return LOST_REPORTED

async def found_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Found item description from %s: %s", user.first_name, update.message.text)

    context.user_data['found_description'] = update.message.text

    await update.message.reply_text(
        "Thank you.\nNow please send a clear photo of the found item."
    )

    return FOUND_PHOTO
async def found_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user

    if not update.message.photo:
        await update.message.reply_text("Please send a photo of the item.")
        return FOUND_PHOTO

    photo_file_id = update.message.photo[-1].file_id
    context.user_data['found_photo'] = photo_file_id

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    admin_caption = (
        f"Found Item Report\n\n"
        f"Telegram Username: @{user.username}\n"
        f"Description: {context.user_data['found_description']}\n"
        f"Submitted at: {timestamp}"
    )

    for admin_uid in ADMIN_UIDS:
        await context.bot.send_photo(
            chat_id=admin_uid,
            photo=photo_file_id,
            caption=admin_caption
        )

    await update.message.reply_text(
        "Found item reported successfully.\n"
        "The administration will match it with lost item reports.\n\n"
        "Send /start to return to the main menu."
    )

    return FOUND_REPORTED
async def found_already_reported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "This found item has already been reported.\n"
        "Send /start to go back to the main menu."
    )
    return FOUND_REPORTED




async def name_and_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s Name and ID: %s", user.first_name, update.message.text)

    context.user_data['name_and_id'] = update.message.text

    await update.message.reply_text(
        "Please enter block and dorm number"
    )

    return BLOCK_AND_DORM_NO

async def block_and_dorm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s Block and Dorm: %s", user.first_name, update.message.text)

    context.user_data['block_and_dorm'] = update.message.text

    await update.message.reply_text(
        "What is the issue?"
    )

    return ISSUE_REPORT

async def issue_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Issue report: %s", update.message.text)

    context.user_data['issue'] = update.message.text

    await update.message.reply_text(
        "Message received!"
    )

    """
    New Complaint Received!

    Telegram Username: @username
    Name & ID: someone
    Block & Dorm: 000
    Issue: ...
    Submitted at: day-date
    """

    complaint = {
        'username': context.user_data['username'].username,
        'name_and_id': context.user_data['name_and_id'],
        'block_and_dorm': context.user_data['block_and_dorm'],
        'issue': context.user_data['issue'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    admin_message = (
        f"New complaint received!\n\n"
        f"Telegram Username: {complaint['username']}\n"
        f"Name & ID: {complaint['name_and_id']}\n"
        f"Block & Dorm: {complaint['block_and_dorm']}\n"
        f"Issue: {complaint['issue']}\n"
        f"Submitted at: {complaint['timestamp']}\n"
    )

    for admin_uid in ADMIN_UIDS:
        await context.bot.send_message(
            chat_id=admin_uid,
            # photo=complaint['photo_file_id'],
            text=admin_message,
            # reply_markup=reply_markup
        )

    return ISSUE_ALREADY_REPORT

async def issue_already_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Issue report: %s", update.message.text)
    await update.message.reply_text(
        "Message already received!\n /start to send another Issue!"
    )

    return ISSUE_ALREADY_REPORT

# async def skip_issue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     logger.info("የራስህ ጉዳይ ነዋ! %s", user.first_name)
#     await update.message.reply_text(
#         f'የራስህ ጉዳይ ነዋ! {user.first_name}',
#     )

#     return ISSUE

def run_health_server():
    port = int(os.environ.get("PORT", 8080))

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        def log_message(self, format, *args):
            pass  # suppress access logs

    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def main() -> None:
    """Run the bot."""
    # Start health check server in background thread for Render keep-alive
    threading.Thread(target=run_health_server, daemon=True).start()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
           START: [
                MessageHandler(
                filters.Regex("(?i)^(Get Info|Report an Issue|Lost item|Found Item)$"),
                 start_reply
                 )
            ],

            NAME_AND_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, name_and_id),
                CommandHandler("start", start)
            ],

            BLOCK_AND_DORM_NO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, block_and_dorm),
                CommandHandler("start", start)
            ],

            ISSUE_REPORT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, issue_report),
                CommandHandler("start", start)
            ],

            ISSUE_ALREADY_REPORT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, issue_already_report),
                CommandHandler("start", start)
            ],
            LOST_AND_FOUND: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lost_and_found),
                CommandHandler("start", start)
            ],
            LOST_REPORTED: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lost_already_reported),
                CommandHandler("start", start)
            ],
            FOUND_DESC: [
                 MessageHandler(filters.TEXT & ~filters.COMMAND, found_description),
                 CommandHandler("start", start)
            ],
            
            FOUND_PHOTO: [
                 MessageHandler(filters.PHOTO, found_photo),
                 MessageHandler(filters.TEXT & ~filters.COMMAND, found_photo),
                 CommandHandler("start", start)
            ],
            FOUND_REPORTED: [
                 MessageHandler(filters.TEXT & ~filters.COMMAND, found_already_reported),
                 CommandHandler("start", start)
            ],

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()