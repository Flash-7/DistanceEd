from django import forms
from django.forms import SelectDateWidget
from myappF23.models import Order



class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]

    interested = forms.TypedChoiceField(
        choices=INTEREST_CHOICES, widget=forms.RadioSelect, coerce=int
    )
    levels = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'label': 'Additional Comments'}),
        required=False
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['students', 'courses', 'levels', 'order_date']
        widgets = {
            'student': forms.RadioSelect(),
            'order_date': SelectDateWidget(),
        }
