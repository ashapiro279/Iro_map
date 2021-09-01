from django.db import models


date_choices = [
                ('2021', '2021'),
                ('2020', '2020'),
                ('2019', '2019'),
                ('2018', '2018'),
                ('2017', '2017')
]




# Create your models here.
class Friend(models.Model):
    # NICK NAME should be unique
    nick_name = models.CharField(max_length=100, unique =  True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    likes = models.CharField(max_length = 250)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    lives_in = models.CharField(max_length=150, null = True, blank = True)

    def __str__(self):
        return self.nick_name

class Coords(models.Model):
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)

    def __str__(self):
        return (f'{self.lat}, {self.lon}')

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)


class DateTimesModel(models.Model):
    dates = models.CharField(max_length=5, choices=date_choices)