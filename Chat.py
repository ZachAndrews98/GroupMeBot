# Created by Zachary Andrews
# Github: ZachAndrews98

try:
    from chatterbot import ChatBot
except:
    print("Required packages not installed, please run pip3 install -r requirements.txt")
    quit()

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.conversations")

def chat(talk):
    # Get a response to an input statement
    return chatbot.get_response(talk)