import unittest
import unittest.mock as mock
import chatbot
from dotenv import load_dotenv
from os.path import join, dirname
import os,datetime
import app

from chatbot import KEY_BOT_COMMAND, KEY_MESSAGE, KEY_IS_BOT
import models

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_FIRST_WORD = "first_word"
KEY_SECOND_WORD = "second_word"

class parsingLogicTestCase(unittest.TestCase):
    
    def setUp(self):

#### testing chatbot help

        self.chatbot_help_success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: {
                    KEY_MESSAGE: 'Enter the commands help: about, help, funtranslate <message>, date, joke',
                    KEY_IS_BOT: True
                    }
            },
        ]
#### testing chatbot about

        self.chatbot_about_success_test_params = [
            {
                KEY_INPUT: "!! about",
                KEY_EXPECTED: {
                    KEY_MESSAGE: "I am a chatbot! I can translate any sentence, a random joke and today's date. Don't forget to type '!!'"
                    }
            }
        ]

    def test_help_success(self):
        
        for test in self.chatbot_help_success_test_params:
            
            response = chatbot.switch(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response[KEY_MESSAGE], expected[KEY_MESSAGE])
            
    def test_about_success(self):
        
        for test in self.chatbot_about_success_test_params:
            
            response = chatbot.switch(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(response[KEY_MESSAGE], expected[KEY_MESSAGE])
            
    
if __name__ == '__main__':
    unittest.main()
