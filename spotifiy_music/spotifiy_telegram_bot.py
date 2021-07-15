import logging

from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

from spotifiy_music_adder_read import add_saved_track_by_id ,get_tracks_for_search_text

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# states for the conversion
SEARCH, ADD_TRACK = range(2)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.message.from_user.id

    # trivial way to make sure that only you can add new songs to your playlist
    if user_id != 1662492232:
        logger.warning(f"User {user_id} was trying to start a conversation.")
        update.message.reply_text("Only the owner of this bot is allowed to add new songs")

        return ConversationHandler.END

    logger.info(f"Converstation started with user {user_id}")
    update.message.reply_text(
        "Hi! I am the Spotifiy music Adder Bot. \n\n"
        "Simply tell me the name of the song that you want to add (e.g. PayPhone)\n"
        "I will then give you options and you can add it to your saved tracks!"
    )

    return SEARCH


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def search_track(update: Update, context: CallbackContext) -> None:
    """Get the user song name from the user and start the track adding process
    Send a numbered list with the possibly meant songs.
    """
    user_id = update.message.from_user.id
    song_name = update.message.text
    logger.info(f"User {user_id} is trying to add {song_name}.")

    # search for the possible tracks
    found_tracks = get_tracks_for_search_text(song_name)
    found_tracks_dict = {}

    reply_keyboard = []
    curr_row = []

    for index, track in enumerate(found_tracks):
        track_name = f"{track[0]} - {track[1]}"
        curr_row.append(track_name)

        # adding the track name to reference when a selection was made 
        found_tracks_dict[track_name] = track

        # after every second element, create a new entry  in the keyboard
        if index % 2 == 1:
            reply_keyboard.append(curr_row)
            curr_row = []

    # presist the dict in the context to be used in the next state
    context.user_data["found_tracks_dict"] = found_tracks_dict

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Please select the song that you are looking for", reply_markup=markup)
    

    return ADD_TRACK


def add_new_track(update: Update, context: CallbackContext) -> None:
    """" add the track that was selected by the user to the playlist"""

    #get the dict of tracks persisted in the previous search stage
    found_tracks_dict = context.user_data["found_tracks_dict"]

    selection = update.message.text
    user_id = update.message.from_user.id
    track = found_tracks_dict[selection]

    #create track name from artist and song 
    track_name = f"{track[0]} - {track[1]}"

    #trigger the request to add it to the saved tracks lists
    add_saved_track_by_id(track[2])

    logger.info(f"Added {track_name} to saved tracks for user {user_id}")
    update.message.reply_text(f"Added {track_name} to saved tracks")

    return SEARCH

def cancel(update: Update, context: CallbackContext) -> None:
    """Inform the user that the conversation was canceled"""
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation")
    update.message.reply_text("Bye! I look forward to talking to you again soon!!")

    return ConversationHandler.END
    


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1692062723:AAHaF4fCtpU1VYURk-Xuy-nh-sIgiYAetes", use_context=True)
    


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SEARCH: [MessageHandler(Filters.text, search_track)],
            ADD_TRACK: [MessageHandler(Filters.text, add_new_track)]
        
        },

        fallbacks=[CommandHandler("cancel", cancel)]
    )
    dispatcher.add_handler(conv_handler)


    # Start the polling process and run the bot until you press Ctrl-C 
    # or the process receives a termination signal.
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
