from chatterbot import ChatBot as ChatBot_
from chatterbot.trainers import ChatterBotCorpusTrainer


def init_chatbot():
    """Creates a ChatBot instance and trains it.
    Returns the chatbot once training has finished.
    """

    chatbot = ChatBot_(
        "Beep Boop Bot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri="sqlite:///_chatbot_db/db.sqlite3"
    )

    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")

    return chatbot


async def get_response(chatbot_object: ChatBot_, input_: str):
    """Gets a response from a chatbot.
    This function exists because the default ChatBot.get_response method is
    not an async function
    """

    return chatbot_object.get_response(input_)