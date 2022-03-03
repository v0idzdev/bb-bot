from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot("Beep Boop Bot")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

while True:
    inp = input(">> ")
    answer = chatbot.get_response(inp)
    print(answer)