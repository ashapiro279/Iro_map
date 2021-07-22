from django.shortcuts import render
from django.http import HttpResponseRedirect
import urllib.request
import json
from .forms import Nameform
import datetime

#weather url days syntax - "start_day=02-02&end_day=03-01"
BASE_WEATHER_URL = 'https://api.weatherbit.io/v2.0/normals?lat={}&lon={}&start_day={}&end_day={}&tp=daily&key=9d6779bced5b4349a063cb9c3db865bd'
MAPBOX_GET_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/-114.28125000002024%2C57.31093640737254.json?access_token=pk.eyJ1IjoiYXNoYXBpcm8yNzkiLCJhIjoiY2txM2NpZTA5MGFwejJvbncwZjg5eHloMiJ9.pOzgpqxmh3QSD0iew65rbg&cachebuster=1625549205587&autocomplete=false'

def default_map(request):
    needed_info = {'mapbox_access_token': 'pk.eyJ1IjoiYXNoYXBpcm8yNzkiLCJhIjoiY2txM2NsZXVqMHgxODJ3cXB3OGN1czA1cCJ9.1FDgqX2Rw6AbwJP4FfuMww'}
    return render(request, 'test_template.html', needed_info)

def searches(request):
    
    needed_info = {} #search = request.POST.get('search')
    return render(requst, 'maps/searches.html', )

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(form.cleaned_data())
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'test_template.html', {'form': form})

def home(request):
    if request.method == 'POST':
        print('its post')
        request_body = json.loads(request.body.decode('utf-8'))
        print(request_body['latitude'])
    if request.method == 'GET':
        print('its get')
        #get_position = request.GET['username']
        #get_data = json.loads(request.body.decode('utf-8'))
        #print(get_position)
        return render(request, 'test_template.html')
    else:
        return render(request, 'test_template.html', {'mapbox_access_token': 'pk.eyJ1IjoiYXNoYXBpcm8yNzkiLCJhIjoiY2txM2NsZXVqMHgxODJ3cXB3OGN1czA1cCJ9.1FDgqX2Rw6AbwJP4FfuMww'})
    '''if request.method == 'POST':
        data = request.POST.get('Location')

        lat_lon = str(data).split(', ') #for now assuming that the user types in lat lon coords
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        end_day = yesterday.strftime('%m-%d')
        start_day = (datetime.datetime.now() - datetime.timedelta(days=8)).date().strftime('%m-%d')
        url = BASE_WEATHER_URL.format(lat_lon[0], lat_lon[1], start_day, end_day)
        #with urllib.request.urlopen(url) as response:
        #    weather_dic = json.load(response)
        #    print(weather_dic)
        
        needed_info = {'get_position': get_position, 'data': data, 'mapbox_access_token': 'pk.eyJ1IjoiYXNoYXBpcm8yNzkiLCJhIjoiY2txM2NsZXVqMHgxODJ3cXB3OGN1czA1cCJ9.1FDgqX2Rw6AbwJP4FfuMww'}
        return render(request, 'test_template.html', needed_info)'''
    