import telebot
import requests


class WeatherBot(object):
    def __init__(self, token, key):
        self.bot = telebot.TeleBot(token)
        self.api_key = key

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, 'Здравствуй, человек!')
            self.bot.send_message(message.chat.id, 'Напиши свой город, чтобы узнать погоду')

        @self.bot.message_handler(content_types=['text'])
        def get_message(message):
            city = message
            result = requests.get("http://api.openweathermap.org/data/2.5/find",
                                  params={'q': city.text, 'type': 'like', 'units': 'metric', 'APPID': self.api_key})
            result = result.json()
            try:
                self.bot.send_message(message.chat.id, "weather: %s" % result['list'][0]['weather'][0]['description'])
                self.bot.send_message(message.chat.id, "temperature: %s" % result['list'][0]['main']['temp'])
                self.bot.send_message(message.chat.id, "pressure: %s" % result['list'][0]['main']['pressure'])
                self.bot.send_message(message.chat.id, "humidity: %s" % result['list'][0]['main']['humidity'])
                self.bot.send_message(message.chat.id, "temp_max: %s" % result['list'][0]['main']['temp_max'])
                self.bot.send_message(message.chat.id, "temp_min: %s" % result['list'][0]['main']['temp_min'])
            except Exception:
                self.bot.send_message(message.chat.id, "Такого города нет в базе =(")
                self.bot.send_message(message.chat.id, "Попробуй ещё раз!")

        self.bot.polling(none_stop=True, interval=0)
        
