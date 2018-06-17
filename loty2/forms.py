from django import forms


class DateForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2100)))
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2100)))

