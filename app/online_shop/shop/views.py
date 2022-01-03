from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import RegistrationForm
from .models import Customer, Address


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            try:
                new_user = form.save(commit=False)
                new_user.username = form.cleaned_data['username']
                new_user.email = form.cleaned_data['email']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.save()
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
                country = form.cleaned_data['country']
                region = form.cleaned_data['region']
                town = form.cleaned_data['town']
                street = form.cleaned_data['street']
                house = form.cleaned_data['house']
                flat = form.cleaned_data['flat']
                address, is_created = Address.objects.get_or_create(
                    country=country,
                    region=region,
                    town=town,
                    street=street,
                    house=house,
                    flat=flat
                )

                customer = Customer.objects.create(
                    user=new_user,
                    birthdate=form.cleaned_data['birthdate'],
                    phone=form.cleaned_data['phone'],
                    image=form.cleaned_data['image'],
                    store_owner=form.cleaned_data['store_owner']
                )
                customer.address.add(address)
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
                return HttpResponseRedirect('/')
            except ValidationError as e:
                context = {
                    'errors': e.message,
                    'form': form
                }
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)
