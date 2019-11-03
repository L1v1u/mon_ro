from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from .models import CustomUser, UserProfile, UserStatus
from django.contrib import messages
from django.forms.models import model_to_dict
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import logging
from celery import shared_task
from projects.models import Project, ProjectStatus

logger = logging.getLogger(__name__)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(model_to_dict(user), token):
        user.is_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. '
                                  'Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')


class UserProfileSaveView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        exists = getattr(request.user, 'userprofile', None)
        if exists:
            logger.error(request.user.userprofile)
        form = UserProfileForm
        context = {'form': form}
        return render(request, 'create_profile.html', context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST)
        if form.is_valid():
            user_profile = self.save_user_profile(request, form.cleaned_data)
            return render(request, 'project_created.html', {'user_profile': user_profile})
        return render(request, 'create_profile.html', {'form': form})

    def save_user_profile(self, request, data):
        user_profile = UserProfile(
            user=request.user,
            firstname=data['firstname'],
            lastname=data['lastname'],
            address_1=data['address_1'],
            address_2=data['address_2'],
            address_city=data['address_city'],
            phonenumber=data['phonenumber'],
            subscription_sms_alerts=data['subscription_sms_alerts'],
            subscription_newsletter=data['subscription_newsletter'],
            subscription_surveys=data['subscription_surveys'],
            user_type='user',
            status=UserStatus.COMPLETE.value)
        user_profile.save()
        self.change_projects_status.delay(model_to_dict(request.user))
        return user_profile

    @shared_task(bind=True)
    def change_projects_status(self, user):
        myuser = CustomUser.objects.filter(id=user['id']).first()

        projects = Project.objects.filter(user=myuser, status=ProjectStatus.INACTIVE.value)
        for project in projects:
            project.status = ProjectStatus.PROFILE_ACTIVE.value
            project.save()

