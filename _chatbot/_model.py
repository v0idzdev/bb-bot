from chatterbot import ChatBot as ChatBot_
from chatterbot.trainers import ChatterBotCorpusTrainer


def init_chatbot():
    """Creates a ChatBot instance and trains it.
    Returns the chatbot once training has finished.
    """

    chatbot = ChatBot_("Beep Boop Bot")
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")

    return chatbot