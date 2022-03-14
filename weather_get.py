# -*- coding: utf-8 -*-

import datetime
import weather_maker
import image_maker
import get_add_data_to_db
from models import *


class RequestHandler:

    def __init__(self, dict_w):
        self.dict_w = dict_w

    def print_message(self):

        print('1 - Получение карточки прогноза по введённой дате за текущий год')
        print('2 - Вывод полученных прогнозов по введённой дате за текущий год')
        print('3 - Добавление данных в базу данных за год')
        print('4 - Получение прогноза из базы данных по дате')
        print('0 - Завершение работы программы')

        print('Введите номер вашего выбора: ')

        user_choose = input()

        return user_choose

    def choose_1(self, date):

        print('Карточка прогнозов сохранена в image_weather')
        weather_1 = image_maker.ImageMaker(self.dict_w, date)
        weather_1.weather_draw()

    def choose_2(self, date):

        day, month, year = (int(x) for x in date.split('-'))

        date_user = datetime.datetime(year, month, day, 0, 0)

        for data in self.dict_w:

            if data['date_weather'] == date_user:
                print('Данные за введённую дату: ')
                print(f"Погода: {data['info_weather_text']}\n"
                      f"Дата: {date}\n"
                      f"Температура днём: {data['temperature_day']}\n"
                      f"Температура вечером: {data['temperature_night']}\n"
                      f"Давление: {data['pressure_day']}\n"
                      f"Влажность: {data['humidity']}\n"
                      f"Скорость ветра: {data['speed_wind']}\n"
                      f"Температура воды: {data['temp_water']}\n")

    def choose_4(self, db_3):

        st, end = get_add_data_to_db.DatabaseUpdater().check_dates()
        print(f"Вы можете получить данные по дате в диапозоне от {st} до "
              f"{end}\n")

        date_user = input('Введите интересующую дату в формате dd-mm-yyyy: ')

        info = db_3.get_weather_data(date_user)

        print('\nДанные за введённую дату: ')
        print(f"Погода: {info.info_weather_text}\n"
              f"Дата: {date_user}\n"
              f"Температура днём: {info.temperature_day}\n"
              f"Температура вечером: {info.temperature_night}\n"
              f"Давление: {info.pressure_day}\n"
              f"Влажность: {info.humidity}\n"
              f"Скорость ветра: {info.speed_wind}\n"
              f"Температура воды: {info.temp_water}\n")

    def do_choose(self):

        db_3 = get_add_data_to_db.DatabaseUpdater()

        while True:

            user_choose = self.print_message()

            if user_choose == '1' or user_choose == '2':

                date = input('Введите интересующую дату в формате dd-mm-yyyy за текущий год: ')

                if user_choose == '1':

                    self.choose_1(date)

                elif user_choose == '2':

                    self.choose_2(date)

            elif user_choose == '3' or user_choose == '4':

                if user_choose == '3':
                    db_3.input_data_weather(self.dict_w)

                elif user_choose == '4':

                    self.choose_4(db_3)

            elif user_choose == '0':
                return False


if __name__ == '__main__':

    weather = weather_maker.WeatherMaker()
    dict_w = weather.get_weather()

    handler = RequestHandler(dict_w)
    handler.do_choose()