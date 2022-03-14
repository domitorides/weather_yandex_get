import datetime

input_data = [
            {'info_weather_text': 'Облачно', 'date_weather': datetime.datetime(2023, 12, 30, 0, 0),
             'temperature_day': '-2', 'temperature_night': '−3', 'pressure_day': '757 мм рт. ст.',
             'humidity': '91%',
             'speed_wind': '5.5 м/с ЮЗ', 'temp_water': '+1'},
            {'info_weather_text': 'Облачно', 'date_weather': datetime.datetime(2022, 12, 31, 0, 0),
             'temperature_day': '-2', 'temperature_night': '−3', 'pressure_day': '757 мм рт. ст.',
             'humidity': '91%',
             'speed_wind': '5.8 м/с ЮЗ', 'temp_water': '+1'},
        ]

# print(input_data[0]['date_weather'].year)
print(len(input_data))