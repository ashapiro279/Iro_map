from .models import Friend
from django import forms
import datetime
from .models import DateTimesModel


date_choices = [
                ('2021', '2021'),
                ('2020', '2020'),
                ('2019', '2019'),
                ('2018', '2018'),
                ('2017', '2017')
]



class FriendForm(forms.ModelForm):
    ## change the widget of the date field.
    dob = forms.DateField(
        label='What is your birth date?', 
        # change the range of the years from 1980 to currentYear - 5
        widget=forms.SelectDateWidget(years=range(1980, datetime.date.today().year-5))
    )
    
    def __init__(self, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Friend
        fields = ("__all__")


class DatetmeModelForm(forms.Form):
    choose_date = forms.ChoiceField(choices=date_choices)