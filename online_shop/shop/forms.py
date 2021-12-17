from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Address


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.ImageField(required=False)
    store_owner = forms.BooleanField(required=False)
    birthdate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    country = forms.CharField(required=True)
    region = forms.CharField(required=True)
    town = forms.CharField(required=True)
    street = forms.CharField(required=True)
    house = forms.CharField(required=True)
    flat = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields["password"].label = "Password"
        self.fields['confirm_password'].label = "Confirm password"
        self.fields['email'].label = "Email"
        self.fields['first_name'].label = "First name"
        self.fields["last_name"].label = "Last name"
        self.fields["phone"].label = "Phone number"
        self.fields['country'].label = "Country"
        self.fields['region'].label = "Region"
        self.fields['town'].label = "Town"
        self.fields['street'].label = "Street"
        self.fields['house'].label = "House"
        self.fields['flat'].label = "Flat"

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain not in ['com', 'net', 'ru', 'by']:
            raise forms.ValidationError('Registration for domain"{}" is impossible'.format(domain))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username {} is already used'.format(username))
        return username

    # def clean_address(self):
    #     country = self.cleaned_data['country']
    #     region = self.cleaned_data['region']
    #     town = self.cleaned_data['town']
    #     street = self.cleaned_data['street']
    #     house = self.cleaned_data['house']
    #     flat = self.cleaned_data['flat']
    #     if Address.objects.filter(
    #             country=country,
    #             region=region,
    #             town=town,
    #             street=street,
    #             house=house,
    #             flat=flat).exists():
    #         return True
    #     return False

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'confirm_password',
            'email',
            'first_name',
            'last_name',
            'phone',
            'country',
            'region',
            'town',
            'street',
            'house',
            'flat'
        ]
