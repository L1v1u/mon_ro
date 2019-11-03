from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TradesmanForm
from .models import Tradesman, TraderType
from django.forms.models import model_to_dict
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from users.models import CustomUser, UserProfile, UserTypes, UserStatus
from django.contrib.auth import login
from projects.views import send_activation_email


class TradesmanSaveView(View):
    def get(self, request, *args, **kwargs):
        form = TradesmanForm
        context = {'form': form}
        return render(request, 'create_tradesman.html', context)

    def post(self, request, *args, **kwargs):
        form = TradesmanForm(data=request.POST)
        if form.is_valid():
            tradesman_profile = self.save_tradesman(request, form.cleaned_data)
            return redirect("create-tradesman-step2")
        return render(request, 'create_tradesman.html', {'form': form})

    def save_tradesman(self, request, data):
        try:
            user = CustomUser.objects.get(email=data['email'].lower())
        except CustomUser.DoesNotExist:
            user = CustomUser(email=data['email'].lower(),
                              username=data['username'].lower(),
                              accepted_terms_condition=True)
            user.set_password(data['password'])
            user.save()
            login(request, user)
            current_site = get_current_site(request)
            send_activation_email.delay(current_site.domain, model_to_dict(user))
            user_profile = UserProfile(
                user=request.user,
                firstname=data['firstname'],
                lastname=data['lastname'],
                subscription_newsletter=data['subscription_newsletter'],
                user_type=UserTypes.TRADER.value,
                status=UserStatus.INCOMPLETE.value)
            user_profile.save()

