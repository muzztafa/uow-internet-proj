from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.forms import PasswordInput, EmailInput, BaseModelFormSet
from myapp.models import Order, User, Client, Category


class OrderForm(forms.ModelForm):
    # client=forms.ModelChoiceField(label='Client Name', widget=forms.RadioSelect)
    # product=forms.ModelChoiceField()
    # num_units=forms.IntegerField(label='Quantity')

    class Meta:
        model = Order
        fields = ['client','product', 'num_units']
        # exclude = ["client"]

        # widgets = {
        #     'client': forms.RadioSelect,
        # }
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
        fields = ['username', 'password']
        widgets = {'password': forms.PasswordInput}
        help_texts = {"username": None, "password": None}

        # labels = {
        #     'username': 'Client Name',
        #     'num_units': 'Quantity'
        # }
    # username = forms.CharField(required=True)
    # password = forms.PasswordInput(required=True)


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')

    # class Meta:
    #   model = User
    #  fields = ["email"]


# Task 3 creating a registration form.
class RegisterForm(UserCreationForm):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'), ]

    email = forms.EmailField(required=True)
    interested_in = forms.ModelMultipleChoiceField(required=True, queryset=Category.objects.all())
    city = forms.CharField(required=True)
    province = forms.ChoiceField(required=True, choices=PROVINCE_CHOICES)

    class Meta:
        model = Client
        fields = (
            "username", "first_name", "last_name", "email", "password1", "password2", "interested_in", "city",
            "province",
            "photo")
