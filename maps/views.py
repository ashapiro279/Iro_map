from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import urllib.request
import json
import io, base64
from . import forms
import datetime
import re
from django.core import serializers
import pprint
from django.http import JsonResponse
from .forms import FriendForm, DatetmeModelForm
from .models import Friend, Coords
import pandas as pd
from statistics import mean
from math import ceil
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from .utils import get_graph, get_plot, get_plotly_graph
import plotly

#weather url days syntax - "start_day=02-02&end_day=03-01"
#key1 = '9d6779bced5b4349a063cb9c3db865bd'
#key2 = '817cf89869664a96880b17d3c8ecbe71'
#key3 = '2161818004a54e4a8aa40226af21c455'
BASE_WEATHER_URL = 'https://api.weatherbit.io/v2.0/history/daily?lat={}&lon={}&start_date={}&end_date={}&key=2161818004a54e4a8aa40226af21c455'
MAPBOX_GET_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/-114.28125000002024%2C57.31093640737254.json?access_token=pk.eyJ1IjoiYXNoYXBpcm8yNzkiLCJhIjoiY2txM2NpZTA5MGFwejJvbncwZjg5eHloMiJ9.pOzgpqxmh3QSD0iew65rbg&cachebuster=1625549205587&autocomplete=false'

def index(request):
    return render(request, 'test_template.html', {})



def home(request):
    this_year = datetime.datetime.today().year
    YEARS = [this_year - i for i in range(21)]
    context = {'years_lst': YEARS, 'period': ['Daily', 'Weekly', 'Monthly', 'Year']}
    print(YEARS)
    if request.is_ajax():
        print('IT IS AJAX')
    if request.method == 'POST':
        print('its post')
        #lat lng
        request_body = request.POST.get('realData')
        select_year = request.POST.get('year')
        select_period = request.POST.get('period')
        if select_year == str(this_year):
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
            end_day = yesterday.strftime('%Y-%m-%d')
            #start_day = (datetime.datetime.now() - datetime.timedelta(days=8)).date().strftime('%Y-%m-%d')
            start_day = f'{this_year}-01-01'
        else:
            start_day = f'{select_year}-01-01'
            end_day = f'{int(select_year)+1}-01-01'



        lat_lon_dict = (eval(request_body))
        print(lat_lon_dict)
        lat = lat_lon_dict['lat']
        lng = lat_lon_dict['lng']
        #datetime
        
        #weather request
        print(start_day, end_day)
        url = BASE_WEATHER_URL.format(lat, lng, start_day, end_day)
        print(url)
        #data = None
        #with urllib.request.urlopen(url) as response:
        #    data = json.load(response)

        #with open('sample_data.json') as f:
            #data = json.load(f)


        with open('year_weather.json') as f:
            data = json.load(f)


        city = data['city_name']
        context['static_var'] = city






        #average data
        iterate = 0
        weather_df = pd.DataFrame(data['data'])
        weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
        weather_df = weather_df.fillna(0)
        print(weather_df['datetime'])
        if select_period == 'Daily':
            context['daily'] = True
        elif select_period == 'Weekly':
            iterate = ceil(len(weather_df)/7)
            starter = 0
            seconder = 7
            pd_lst = []
            week_lst = []
            week_lst2 = []
            counter = 8
            for item in range(iterate):
                counter += 1
                week_lst.append(weather_df[starter:seconder]['datetime'].iloc[0])
                week_lst2.append(weather_df[starter:seconder]['datetime'].iloc[-1])
                weather_df.iloc[starter:seconder]['datetime'] = weather_df.iloc[starter:seconder]['datetime']
                pd_lst.append((weather_df.iloc[starter: seconder]))
                starter += 7
                seconder += 7

            for index, week in enumerate(week_lst):
                week = pd.Timestamp.to_pydatetime(week).strftime('%m-%d')
                week_end = pd.Timestamp.to_pydatetime(week_lst2[index]).strftime('%m-%d')
                week_lst[index] = pd.Series([f'{week}-{week_end}'], index=['datetime'])
                
            starter = 0
            seconder = 7
            for index, df in enumerate(pd_lst):
                x = df.mean().round(2)
                x = x.append(week_lst[index])
                #print(week_lst[index].iloc[0])
                pd_lst[index] = x
                #print(weather_df[starter:seconder]['datetime'])
                starter += 7
                seconder += 7

            context['pd_lst'] = pd_lst
        elif select_period == 'Monthly':
            month_len_lst = []
            for index, date in enumerate(weather_df['datetime'].dt.to_period('M')):
                if month_len_lst:
                    if date != weather_df['datetime'].dt.to_period('M')[index-1]:
                        month_len_lst.append(date.days_in_month)
                else:
                    month_len_lst.append(date.days_in_month)


            starter = 0
            seconder = month_len_lst[0]
            pd_lst_monthly = []
            month_lst = []
            for item in range(len(month_len_lst)):
                month_lst.append(weather_df.iloc[starter:seconder]['datetime'].iloc[0])
                weather_df.iloc[starter:seconder]['datetime'] = weather_df.iloc[starter:seconder]['datetime']
                pd_lst_monthly.append((weather_df[starter: seconder]))
                #rint(weather_df[starter: seconder])
                try:
                    starter += month_len_lst[item]
                    seconder += month_len_lst[item+1]
                except:
                    break

            for index, month in enumerate(month_lst):
                month_lst[index] = pd.Series([month], index=['datetime']).dt.strftime('%B')

            starter = 0
            seconder = 7
            for index, df in enumerate(pd_lst_monthly):
                x = df.mean().round(2)
                x = x.append(month_lst[index])
                #print(week_lst[index].iloc[0])
                pd_lst_monthly[index] = x
                #print(weather_df[starter:seconder]['datetime'])
                starter += 7
                seconder += 7


            context['pd_lst_monthly'] = pd_lst_monthly
        elif select_period == 'Year':
            year_mean = weather_df.mean().round(2)
            year_mean['datetime'] = select_year
            context['year_mean'] = year_mean
            context['year_mean_bool'] = True
        

        
        #chart = get_plot(weather_df, 'rh')
        #chart2 = get_plot(weather_df, 'min_temp')
        #chart3 = get_plot(weather_df, 'min_temp')
        #chart4 = get_plot(weather_df, 'min_temp')
        #chart5 = get_plot(weather_df, 'max_temp')
        
        #fig1, ax1 = plt.subplots()
        #fig2, ax2 = plt.subplots()
        #ax1.plot(weather_df['datetime'], weather_df['rh'], label='rh')
        #ax2.plot(weather_df['datetime'], weather_df['min_temp'], label='min_temp')



        #chart_lst = [get_plot(weather_df, cat) for cat in weather_df.columns]
        #context['chart'] = [fig1, fig2]
        #imgdata = StringIO()
        #img_graph = fig1.savefig(imgdata, format='svg')
        #imgdata.seek(0)
        #img_graph_data = imgdata.getvalue() 
        #context['test_chart'] = img_graph_data


        plotly_graph = get_plotly_graph(weather_df)
        context['plotly_graph'] = plotly_graph






        #form = Coords(lat=lat, lon=lng)
        #form.save()
        #print(Coords.objects.all())
        lat = round((lat), 5) 
        lng = round((lng), 5) 
        context['data'] = data
        context['coords'] = f'{lat}, {lng}'
        #print(pd_lst)
        print(request.POST.get('year'))
        print(request.POST.get('period'))
        context['chosen_period'] = select_period
        context['chosen_year'] = select_year
        context['labels'] = ['label', 'label2', 'label3', 'label4']
        return render(request, 'test_template.html', context)
    print(context)
    if request.method == 'GET':
        print('its get')
        context['labels'] = ['label', 'label2', 'label3', 'label4']
    return render(request, 'test_template.html', context)