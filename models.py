
import os
import peewee

path_db = '/Users/dmitrijelizarov/PycharmProjects/weather/python_snippets/external_data/weather_database.db'
norm_path_db = os.path.normpath(path_db)

database_weather = peewee.SqliteDatabase(norm_path_db)


class BaseTable(peewee.Model):
    class Meta:
        database = database_weather


class DataAll(BaseTable):
    info_weather_text = peewee.CharField()
    date_weather = peewee.DateTimeField()
    temperature_day = peewee.CharField()
    temperature_night = peewee.CharField()
    pressure_day = peewee.CharField()
    humidity = peewee.CharField()
    speed_wind = peewee.CharField()
    temp_water = peewee.CharField()
