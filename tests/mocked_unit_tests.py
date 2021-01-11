import unittest
import unittest.mock as mock

import app
import models
from dotenv import load_dotenv

from freezegun import freeze_time
from os.path import join, dirname
import datetime, os
import requests
import chatbot
from chatbot import KEY_BOT_COMMAND, KEY_MESSAGE


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_EMIT = "emit"
KEY_CHANNEL = "channel"
KEY_ID = 0

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']

botty = chatbot.Bot()
db = app.db

freezer = freeze_time("2020-10-28 11:35:00")
freezer.start()

chat_message = models.Messages("Hi my name is Chatbot", 1)
user = models.user_info("chatbot@gmail.com", "chatbot", "picture")

class MockedDateResponse:
    def __init__(self, date):
        self.date = date
        
class MockedCountEmitResponse:
    def __init__(self, user_count):
        self.user_count = user_count
        
class MockedMessagesEmitResponse:
    def __init__(self, all_messages):
        self.all_messages = all_messages

class MockedUserEmitResponse:
    def __init__(self, all_users):
        self.all_users = all_users

class logicTestCase(unittest.TestCase):
    
    def setUp(self):
        self.date_success_test_params = [
            {
                KEY_INPUT: "!! date",
                KEY_EXPECTED: "2020-10-28 11:35:00"
            }
        ]
        self.models_messages_success_test_params = [
            {
                KEY_INPUT: chat_message.message,
                KEY_EXPECTED: "Hi my name is Chatbot"
            }
        ]
        self.app_emit_count_success_test_params = [
            {
                KEY_INPUT: 'emit_user_count',
                KEY_EXPECTED: 0
            }
        ]
        self.app_emit_users_success_test_params = [
            {
                KEY_INPUT: 'emit_all_users',
                KEY_CHANNEL: "text",
                KEY_EXPECTED: []
            }
        ]
        self.app_emit_messages_success_test_params = [
            {
                KEY_INPUT: 'emit_all_messages',
                KEY_CHANNEL: "text",
                KEY_EXPECTED: []
            }
        ]

    def mocked_api_search(self, q):
        return [
            MockedDateResponse("2020-10-27 21:24:00"),
            MockedUserEmitResponse(
                
                { KEY_CHANNEL: {"all_users": app.all_users}}
            ),
            MockedCountEmitResponse(
                
                { KEY_CHANNEL: {"user_count": app.user_count}}
            ),
            MockedMessagesEmitResponse( 
                
                { KEY_CHANNEL: {"all_messages": app.all_messages}}
            )
            ]

    def test_bot_date_success(self):
        
        for test_case in self.date_success_test_params:
            
            with mock.patch('datetime.date'):
               
                response = str(datetime.datetime.today())
                freezer.stop()
            
            expected = test_case[KEY_EXPECTED]
            print(response)
            print(expected)

            self.assertEqual(response, expected)


    def test_models_messages_success(self):
        
        for test_case in self.models_messages_success_test_params:
            
            with mock.patch('models.Messages.__repr__', self.mocked_api_search):
                response = chat_message.message
            
            expected = test_case[KEY_EXPECTED]
            print(response)
            print(expected)
            
            self.assertEqual(response, expected)

    def test_app_emit_count_success(self):
        
        for test_case in self.app_emit_count_success_test_params:
            
            with mock.patch('app.emit_user_count'):
                response = app.user_count
            
            expected = test_case[KEY_EXPECTED]
            print(response)
            print(expected)
            
            self.assertEqual(response, expected)

    def test_emit_users_success(self):
        
        for test_case in self.app_emit_users_success_test_params:
            
            with mock.patch('app.emit_all_users', self.mocked_api_search):
                response = app.all_users
               
            expected = test_case[KEY_EXPECTED]
             #print(response)
            #print(expected)
            
            self.assertEqual(response, expected)

    def test_emit_messages_success(self):
        
        for test_case in self.app_emit_messages_success_test_params:
            with mock.patch('app.emit_all_messages', self.mocked_api_search):
                response = app.all_messages
               
            expected = test_case[KEY_EXPECTED]
            print(response)
            #print(expected)
            
            self.assertEqual(test_case[KEY_EXPECTED], expected)

if __name__ == '__main__':
    unittest.main()
