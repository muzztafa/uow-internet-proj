from django import forms
from myapp.models import Order, User


class OrderForm(forms.ModelForm):

    # client=forms.ModelChoiceField(label='Client Name', widget=forms.RadioSelect)
    # product=forms.ModelChoiceField()
    # num_units=forms.IntegerField(label='Quantity')

    class Meta:
        model = Order
        fields = ['client','product','num_units']
        widgets = {
            'client': forms.RadioSelect,
        }
        labels = {
            'client': 'Client Name',
            'num_units': 'Quantity'
        }
        # widgets = {
        #     'yes_or_no': forms.RadioSelect
        # }


class InterestForm(forms.Form):

    CHOICES_INT = (
        ("1", "Yes"),
        ("0", "No"),
    )

    interested = forms.ChoiceField(choices=CHOICES_INT, widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

        # labels = {
        #     'username': 'Client Name',
        #     'num_units': 'Quantity'
        # }
    # username = forms.CharField(required=True)
    # password = forms.PasswordInput(required=True)


class RegisterForm(forms.ModelForm):
    class Meta:
        models = User
        fields = ['username', 'password']

        # first_name
        # last_name
        # email
        # company
        # shipping_address
        # city
        # province
        # interested_in
