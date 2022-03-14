
import datetime
import cv2
import os


class ImageMaker:

    def __init__(self, data_w, date_user):

        self.data = data_w
        self.date_user = date_user
        self.path_probe = 'python_snippets/external_data/probe.jpg'
        self.path_weather_img = 'python_snippets/external_data/weather_img/'
        self.path_dir = 'image_weather'

    def get_date_from_dict(self):

        norm_path = os.path.normpath(self.path_probe)
        image_wather = cv2.imread(norm_path, cv2.IMREAD_UNCHANGED)

        day, month, year = (int(x) for x in self.date_user.split('-'))

        self.date_user = datetime.datetime(year, month, day, 0, 0)

        for data in self.data:

            if data['date_weather'] == self.date_user:
                dict_info = data

        return image_wather, dict_info

    def do_gradient(self, path_k, i_plus, k_plus, rng, b, g, r, image_wather):

        path_all = self.path_weather_img + path_k
        norm_path_k = os.path.normpath(path_all)

        i = 0
        k = 0
        for _ in range(rng):
            if path_k == 'sun.jpg':
                image_wather[:, i:50 + i] = (b + k, g, r)
            elif path_k == 'rain.jpg':
                image_wather[:, i:50 + i] = (b, k, r + k)
            elif path_k == 'snow.jpg':
                image_wather[:, i:50 + i] = (b, g + k, k * 10)
            elif path_k == 'cloud.jpg':
                image_wather[:, i:50 + i] = (b + k, g + k, r + k)
            i += i_plus
            k += k_plus

        return norm_path_k, image_wather

    def choose_weather(self, dict_info, image_wather):

        k = 0
        if dict_info['info_weather_text'] == 'Солнечно':
            # от жёлтого к белому - солнечно
            path_k = 'sun.jpg'
            norm_path_k, image_wather = self.do_gradient(path_k, 40, 10, 20, 50, 250, 255, image_wather)

        elif dict_info['info_weather_text'] == 'Дождливо' or dict_info['info_weather_text'] == 'Дождь' or \
                dict_info['info_weather_text'] == 'Ливень':
            # от синего к белому - дождь
            path_k = 'rain.jpg'
            norm_path_k, image_wather = self.do_gradient(path_k, 40, 2, 20, 255, k, 60, image_wather)

        elif dict_info['info_weather_text'] == 'Снег':
            # от голубого к белому - снег
            path_k = 'snow.jpg'
            norm_path_k, image_wather = self.do_gradient(path_k, 40, 1, 20, 255, 230, k, image_wather)

        elif dict_info['info_weather_text'] == 'Облачно' or dict_info['info_weather_text'] == 'Сильно облачно':
            # от серого к белому - облачно
            path_k = 'cloud.jpg'
            norm_path_k, image_wather = self.do_gradient(path_k, 5, 1, 160, 111, 111, 111, image_wather)

        return norm_path_k, image_wather

    def add_page_weather(self, norm_path_k, image_wather):

        image_paste_weather = cv2.imread(norm_path_k, cv2.IMREAD_UNCHANGED)
        x = 412
        y = 0
        image1_alpha = image_paste_weather[:, :, 2] / 255.0
        height, width = image_paste_weather.shape[0], image_paste_weather.shape[1]
        for c in range(3):
            image_wather[y:y + height, x:x + width, c] = image1_alpha * image_paste_weather[:, :, c] + \
                                                         (1.0 - image1_alpha) * image_wather[y:y + height, x:x + width,
                                                                                c]

        cv2.line(image_wather, (412, 0), (412, 100), (0, 0, 0), 2)
        cv2.line(image_wather, (412, 100), (512, 100), (0, 0, 0), 2)

        return image_wather

    def put_text(self, dict_info, image_wather):

        cv2.putText(image_wather, f"Температура днем: {dict_info['temperature_day']}", (15, 0 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        cv2.putText(image_wather, f"Температура ночью: {dict_info['temperature_night']}", (15, 20 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        cv2.putText(image_wather, f"Давление: {dict_info['pressure_day']}", (15, 40 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        cv2.putText(image_wather, f"Влажность: {dict_info['humidity']}", (15, 60 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        cv2.putText(image_wather, f"Скорость ветра: {dict_info['speed_wind']}", (15, 80 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        cv2.putText(image_wather, f"Температура воды: {dict_info['temp_water']}", (15, 100 + 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

        return image_wather

    def create_dir(self):

        path = os.path.normpath(self.path_dir)
        if not os.path.isdir(path):
            os.mkdir(path)

    def save_page(self, data, image_wather):

        path_all = self.path_dir + '/' + data + '.jpg'
        path = os.path.normpath(path_all)
        cv2.imwrite(path, image_wather)

    def weather_draw(self):

        image_wather, dict_info = self.get_date_from_dict()

        # Закраска
        norm_path_k, image_wather = self.choose_weather(dict_info, image_wather)

        # добавление картинки погоды
        image_wather = self.add_page_weather(norm_path_k, image_wather)

        # вставим текст
        image_wather = self.put_text(dict_info, image_wather)

        date_put = dict_info['date_weather'].strftime('%d-%m-%Y')
        self.create_dir()
        self.save_page(date_put, image_wather)


# проверка работы
# check = ImageMaker(data_w=[{'info_weather_text': 'Облачно', 'date_weather': datetime.datetime(2021, 1, 1, 0, 0),
#         'temperature_day': '−1', 'temperature_night': '−4', 'pressure_day': '753 мм рт. ст.', 'humidity': '89%',
#         'speed_wind': '6.4 м/с ЮЗ', 'temp_water': '+1'}], date_user='01-01-2021')
# check.weather_draw()