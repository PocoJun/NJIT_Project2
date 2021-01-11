import requests
from datetime import date

BOT_PREFIX = "!!"
KEY_IS_BOT = False
KEY_BOT_COMMAND = "bot_command"
KEY_MESSAGE = "message"
KEY_JOKE = ''

JOKE_URL = "https://joke3.p.rapidapi.com/v1/joke"
JOKE_HEADERS = {
    "x-rapidapi-host": "joke3.p.rapidapi.com",
    "x-rapidapi-key": "6bd46d61f2mshd2c80482e12a730p16f242jsn3b38dc8f3fb4",
}
FUNTRANSLATE_URL = "https://api.funtranslations.com/translate/leetspeak.json?text="

class Bot:
    def __init__(self):
        
        #self.message = ""
        self.help = "about, help, funtranslate <message>, date, joke"
        self.about_message = ''
        self.helpString = ""
        self.funt_message = ""
        self.date = ""
        self.rand_joke = ""

#### chatbot about 

    def about(self):
        about = "I am a chatbot! I can translate any sentence, a random joke and today's date. Don't forget to type '!!'"
        self.about_message = about
        
        return {KEY_MESSAGE: self.about_message, KEY_IS_BOT: True}

#### chatbot help
    def helper(self):
        
        helpStr = ("Enter the commands help: "+ self.help)
        self.helpString = helpStr
        
        return {KEY_MESSAGE: self.helpString, KEY_IS_BOT: True}

#### chatbot funtranslate
    def funtranslate(self, text):
        print("0000000", text)
        req = requests.get("https://api.funtranslations.com/translate/leetspeak.json?text=" + text)
        r = req.json()
        self.funt_message = r["contents"]["translated"]
        return {KEY_MESSAGE: self.funt_message, KEY_IS_BOT: True}

#### Today date
    def Today_dat(self):
        today = date.today()
        self.date = "Today's date is " + str(today)
        return {KEY_MESSAGE: self.date, KEY_IS_BOT: True}

#### chatbot joke
    def joke(self):
        #url = "https://joke3.p.rapidapi.com/v1/joke"
        #headers = {
        #    'x-rapidapi-host': "joke3.p.rapidapi.com",
        #    'x-rapidapi-key': "6bd46d61f2mshd2c80482e12a730p16f242jsn3b38dc8f3fb4",
        #    }
        #response = requests.request("GET", url, headers=headers)
        #respo = response.json()
        #self.rand_joke = respo['content']
        #return self.rand_joke
        response = requests.get(JOKE_URL, headers=JOKE_HEADERS).json()
        self.rand_joke = response["content"]
        return {KEY_MESSAGE: self.rand_joke, KEY_IS_BOT: True}


def switch(arg):
    chatbot = Bot()
    #command = arg[1]
    message_components = arg.split(" ")

    if message_components[0] != "!!":
        return {KEY_MESSAGE: arg, KEY_IS_BOT: False}

    if len(message_components) == 2:
        bot_cmd, rest_of_message = message_components[1], ""
    else:
        bot_cmd, rest_of_message = message_components[1], message_components[2:]
        print(rest_of_message)

    if bot_cmd == "funtranslate":
        
        if len(message_components) < 3:
            return "You forgot to enter what you wanted Try again!"
            
        t = " ".join(rest_of_message)
        return chatbot.funtranslate(t)

    elif bot_cmd == "help":
        return chatbot.helper()
        
    elif bot_cmd == "about":
        return chatbot.about()
        
    elif bot_cmd == "date":
        return chatbot.Today_dat()
        
    elif bot_cmd == "joke":
        return chatbot.joke()
        
    else:
        return {KEY_MESSAGE: "Invalid command! Enter '!! help' to see available commands!", KEY_IS_BOT: False}
