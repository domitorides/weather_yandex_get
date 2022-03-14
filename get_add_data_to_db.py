
import datetime
from models import *


class DatabaseUpdater:

    def check_dates(self):

        cnt_records = 0 # Тут идёт подсчёт количества записей
        for date in DataAll.select():
            cnt_records += 1

        cnt = 1
        for date in DataAll.select():
            if cnt == 1:
                st_day = date.date_weather
            if cnt == cnt_records:
                end_day = date.date_weather
            cnt += 1

        return st_day.strftime('%d-%m-%Y'), end_day.strftime('%d-%m-%Y')

    def get_weather_data(self, date_user):

        day, month, year = (int(x) for x in date_user.split('-'))

        date_user_ed = datetime.datetime(year, month, day, 0, 0)

        for date in DataAll.select():

            if date.date_weather == date_user_ed:
                return date

    def input_data_weather(self, input_data):

        print('Запись или обновление данных в базе за текущий год')

        for data in input_data:
            weather, created = DataAll.get_or_create(date_weather=data['date_weather'],
                    defaults={'info_weather_text': data['info_weather_text'],
                              'temperature_day': data['temperature_day'],
                              'temperature_night': data['temperature_night'],
                              'pressure_day': data['pressure_day'],
                              'humidity': data['humidity'],
                              'speed_wind': data['speed_wind'],
                              'temp_water': data['temp_water']})
            if not created:
                query = DataAll.update(
                    info_weather_text=data['info_weather_text'],
                    temperature_day=data['temperature_day'],
                    temperature_night=data['temperature_night'],
                    pressure_day=data['pressure_day'],
                    humidity=data['humidity'],
                    speed_wind=data['speed_wind'],
                    temp_water=data['temp_water']).where(DataAll.id == weather.id)
                query.execute()