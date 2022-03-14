import requests
from bs4 import BeautifulSoup
import re
import datetime


class WeatherMaker:

    def __init__(self):

        self.site_m = []
        self.dict_data_wather = []

        self.LIST_M = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

        self.LIST_M_Y = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

        for month in self.LIST_M_Y:
            self.site_m.append(f'https://yandex.ru/pogoda/saint-petersburg/month/{month}?via=cnav')

    def get_weather_lists(self, response):

        if response.status_code == 200:
            html_doc = BeautifulSoup(response.text, features='html.parser')
            list_day = html_doc.find_all(class_=re.compile("climate-calendar-day__detailed-day"))

            # Температура дня и ночи
            list_temp_day = html_doc.find_all('div', class_='temp climate-calendar-day__detailed-basic-temp-day')
            list_temp_night = html_doc.find_all('div', class_='temp climate-calendar-day__detailed-basic-temp-night')

            # Давление,  влажность, скорость ветра, температура воды
            list_humidity_sp = html_doc.find_all('td', class_='climate-calendar-day__detailed-data-table-cell '
                                                              'climate-calendar-day__detailed-data-table-cell_value_yes')

            list_all_dl = []
            for data in list_humidity_sp:
                list_all_dl.append(data.text)

            list_pressure = list_all_dl[::4]
            list_humidity = list_all_dl[1::4]
            list_wind_speed = list_all_dl[2::4]
            list_water_temp = list_all_dl[3::4]

            list_picture_сl = html_doc.find_all(class_=re.compile("icon_size_48 climate-calendar-day__icon"))
            list_picture = []
            for tag in list_picture_сl:

                if 'bkn_d' in tag.get('src'):
                    list_picture.append('Облачно')
                elif 'skc_d' in tag.get('src'):
                    list_picture.append('Солнечно')
                elif 'bkn_ra_d' in tag.get('src') or 'bkn_-ra_d' in tag.get('src'):
                    list_picture.append('Дождливо')
                elif 'ovc_-ra' in tag.get('src'):
                    list_picture.append('Дождь')
                elif 'ovc_ra' in tag.get('src'):
                    list_picture.append('Ливень')
                elif 'ovc_sn' in tag.get('src'):
                    list_picture.append('Снег')
                elif 'ovc' in tag.get('src'):
                    list_picture.append('Сильно облачно')

        return list_day, list_temp_day, list_temp_night, list_pressure, list_humidity, list_wind_speed, \
               list_water_temp, list_picture

    def write_weather_to_dict(self, list_day, list_temp_day, list_temp_night, list_pressure, list_humidity, list_wind_speed, \
            list_water_temp, list_picture, month_site):

        date_year = datetime.datetime.now().year
        for day, temp_day, temp_night, pr, hum, speed, water, wather_text in zip(list_day, list_temp_day,
                                                                                 list_temp_night, list_pressure,
                                                                                 list_humidity, list_wind_speed,
                                                                                 list_water_temp, list_picture):

            info_m = day.text.split(' ')
            info_m_month = info_m[1]
            info_m_day = int(info_m[0])
            month = self.LIST_M.index(info_m_month[:-1]) + 1

            date_all = datetime.datetime(year=date_year, month=month, day=info_m_day)

            ind_h = 0
            for _ in range(0, 12):
                if self.LIST_M_Y[ind_h] in month_site and self.LIST_M[ind_h] in day.text:
                    cur_all_dict = {'info_weather_text': wather_text, 'date_weather': date_all,
                                    'temperature_day': temp_day.text, 'temperature_night': temp_night.text,
                                    'pressure_day': pr, 'humidity': hum, 'speed_wind': speed,
                                    'temp_water': water}
                    self.dict_data_wather.append(cur_all_dict)
                    break
                ind_h += 1

    def get_weather(self):

        for month_site in self.site_m:

            response = requests.get(month_site)

            # получение листов
            list_day, list_temp_day, list_temp_night, list_pressure, list_humidity, list_wind_speed, \
            list_water_temp, list_picture = self.get_weather_lists(response)

            # запись данных по погоде в словарь
            self.write_weather_to_dict(list_day, list_temp_day, list_temp_night, list_pressure, list_humidity, list_wind_speed, \
            list_water_temp, list_picture, month_site)

        # for data in self.dict_data_wather:
        #     print(data)
        return self.dict_data_wather

# для проверки
# lol = WeatherMaker()
# lol.get_weather()