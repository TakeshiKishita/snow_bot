# -*- coding: utf-8 -*-
import requests
import pandas as pd

class msg_analysis:
    """docstring for generate."""
    def __init__(self):
        self.yuzawa = ["36.911323", "138.812822"]
        self.hakuba = ["36.685895", "137.828257"]
        self.myoko = ["36.863743", "138.154234"]
        self.kagura = ["36.863438", "138.726449"]

    def get_place(self,obj):
        """
        メッセージから場所の取得
        """

        place = 0
        if obj == "湯沢":
            place = 1
        elif obj == "白馬":
            place = 2
        elif obj == "妙高":
            place = 3
        elif obj == "かぐら":
            place = 4

        return place

    def get_lat_lon(self,place):
        """
        場所から緯度経度取得
        """

        lat_lon = ""
        if place == 1:
            lat_lon = self.yuzawa
        elif place == 2:
            lat_lon = self.hakuba
        elif place == 3:
            lat_lon = self.myoko
        elif place == 4:
            lat_lon = self.kagura

        return lat_lon

class get_weather:
    """
    APIから天気を取得
    """
    def __init__(self):
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.api_key = "{OPEN_WEATHER_API_KEY}"
        self.kelvin = 273.15

    def get_api(self,lat_lon):
        """
        apiからjsonを取得
        (list)lat_lon[lat,lon]
        """
        url = self.base_url + "lat="+lat_lon[0]+"&lon="+lat_lon[1]+"&APPID="+self.api_key

        #APIからjsonを取得
        response = requests.get(url)

        return response

    def  get_5days_weather(self,response):
        """
        jsonデータから必要な天候データの抽出
        (json)response: APIjson https://openweathermap.org/current
        """
        #jsonから日別の天気を辞書へ変換
        day_weather = {}
        h_weather = {}
        seq = 0
        new_day = ""
        temp_max = 0
        temp_min = 0
        for lst in response.json()['list']:
            day = lst['dt_txt'][8:10]+"日"
            if new_day == "":
                new_day = day

            if new_day == day:
                h_weather[seq] = lst
                seq += 1

                if temp_max < lst['main']['temp_max']: temp_max = round(lst['main']['temp_max']-self.kelvin,0)
                if (temp_min > lst['main']['temp_min']) or (temp_min == 0): temp_min = round(lst['main']['temp_min']-self.kelvin,0)

            else:
                day_weather[new_day] = h_weather
                day_weather[new_day]['temp_max'] = temp_max
                day_weather[new_day]['temp_min'] = temp_min
                h_weather = {}
                seq = 0
                temp_max = 0
                temp_min = 0
                new_day = day

        else:
            day_weather[new_day] = h_weather
            day_weather[new_day]['temp_max'] = temp_max
            day_weather[new_day]['temp_min'] = temp_min

        w_temp_df = pd.DataFrame(day_weather)


        return w_temp_df

def get_conditions(dlf_json):

    action = dlf_json["result"]["action"]
    ma = msg_analysis()

    if action == "weekly_weather":
        place = ma.get_place(dlf_json["result"]["contexts"][0]["parameters"]["SkiResort"])
        date = "weekly"
        return get_5days_max_min_message(place)
    elif action == "daily_weather":
        place = ma.get_place(dlf_json["result"]["contexts"][0]["parameters"]["SkiResort"])
        date = dlf_json["result"]["contexts"][0]["parameters"]["date"]
        return get_dayly_weather(date,place)
    else:
        return dlf_json["result"]["fulfillment"]["speech"]

def get_dayly_weather(date,place):
    rep = get_weather()
    ma = msg_analysis()
    let_lon = ma.get_lat_lon(place)
    response = rep.get_api(let_lon)
    weather_df = rep.get_5days_weather(response)
    date_flg = False
    for c in range(len(weather_df.columns)):
        if date[-2:] == weather_df.columns[c][:2]:
            date_flg = True
            break

    if not date_flg:
        return "ちょっと"+str(date[-2:])+"日はわからないや..."


    return_message = date[-2:]+"日の天気だよ！\n"
    for lst in weather_df[date[-2:]+"日"]:
        if type(lst) == dict:
            return_message += str(lst['dt_txt'][11:13])+"時"+str(round(lst['main']['temp']-rep.kelvin,0))+"℃\n"
    return return_message

def get_5days_max_min_message(place):
    rep = get_weather()
    ma = msg_analysis()
    let_lon = ma.get_lat_lon(place)
    response = rep.get_api(let_lon)
    weather_df = rep.get_5days_weather(response)

    return_message = "5日間の天気だよ！\n" + str(weather_df.loc[["temp_max","temp_min"],:])
    return return_message
