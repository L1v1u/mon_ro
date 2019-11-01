from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TradesmanForm
from .models import Tradesman, TraderType
from django.forms.models import model_to_dict
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import logging
from celery import shared_task
from projects.models import Project, ProjectStatus

logger = logging.getLogger(__name__)


class TradesmanSaveView(View):

    def get(self, request, *args, **kwargs):
        # exists = getattr(request.user, 'userprofile', None)
        # if exists:
        #     logger.error(request.user.userprofile)
        form = TradesmanForm
        context = {'form': form}
        return render(request, 'create_profile.html', context)

    def post(self, request, *args, **kwargs):
        form = TradesmanForm(data=request.POST)
        if form.is_valid():
            user_profile = self.save_tradesman(request, form.cleaned_data)
            return render(request, 'project_created.html', {'user_profile': user_profile})
        return render(request, 'create_profile.html', {'form': form})

    def save_tradesman(self, request, data):
        pass
        # user_profile = UserProfile(
        #     user=request.user,
        #     firstname=data['firstname'],
        #     lastname=data['lastname'],
        #     address_1=data['address_1'],
        #     address_2=data['address_2'],
        #     address_city=data['address_city'],
        #     phonenumber=data['phonenumber'],
        #     subscription_sms_alerts=data['subscription_sms_alerts'],
        #     subscription_newsletter=data['subscription_newsletter'],
        #     subscription_surveys=data['subscription_surveys'],
        #     user_type='user',
        #     status= 1)
        # user_profile.save()
        # self.change_projects_status.delay(model_to_dict(request.user))
        # return user_profile

    # @shared_task(bind=True)
    # def change_projects_status(self, user):
    #     myuser = CustomUser.objects.filter(id=user['id']).first()
    #
    #     projects = Project.objects.filter(user=myuser, status=ProjectStatus.INACTIVE.value)
    #     for project in projects:
    #         project.status = ProjectStatus.PROFILE_ACTIVE.value
    #         project.save()

