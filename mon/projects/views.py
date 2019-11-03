from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, TemplateView
from .models import Project, ProjectStatus
from users.models import CustomUser
from .forms import CreateProjectForm
from django.urls import reverse_lazy
import random
from django.contrib.auth import login
from celery import shared_task
from anymail.exceptions import AnymailRequestsAPIError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.tokens import account_activation_token
from django.forms.models import model_to_dict
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


@shared_task(bind=True, max_retries=3)
def send_activation_email(self, domain, user):
    try:
        mail_subject = 'Activate your account.'
        message = render_to_string('emails/activate_user.html', {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user['id'])),
            'token': account_activation_token.make_token(user),
        })
        to_email = user['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
    except AnymailRequestsAPIError as exc:
        self.retry(exc=exc, countdown=180)


class ProjectsView(View):
    template_name = 'projects_index.html'

    def get(self, request, *args, **kwargs):
        project_list = Project.objects.all()
        projects_total = Project.objects.count()
        paginator = Paginator(project_list, 25)  # Show 25 contacts per page

        page = request.GET.get('page')
        projects = paginator.get_page(page)
        return render(request, self.template_name, {'projects_total': projects_total, 'projects': projects})


class CreateProjectView(View):
        form_class = CreateProjectForm
        success_url = reverse_lazy('project_created')
        template_name = 'create_project.html'

        def get(self, request, *args, **kwargs):
            form = CreateProjectForm(user=request.user)
            context = {'form': form}
            return render(request, 'create_project.html', context)

        def post(self, request, *args, **kwargs):
            form = CreateProjectForm(data=request.POST, user=request.user)
            if form.is_valid():
                project_id = self.save_project_user(request, form.cleaned_data)
                if project_id == 0:
                    messages.error(request, 'Please login again in order to publish a project')
                    return redirect('login')
                return render(request, 'project_created.html', {'id': project_id})
            return render(request, 'create_project.html', {'form': form})

        def save_project_user(self, request, data):
            if request.user.is_authenticated:
                user = request.user
            else:
                try:
                    user = CustomUser.objects.get(email=data['email'].lower())
                except CustomUser.DoesNotExist:
                    user = CustomUser(email=data['email'].lower(),
                                      username=self.generate_username(data['email'].lower()),
                                      accepted_terms_condition=True)
                    user.set_password(data['password'])
                    user.save()
                    login(request, user)
                    current_site = get_current_site(request)
                    send_activation_email.delay(current_site.domain, model_to_dict(user))
                else:
                    if user.check_password(data['password']):
                        login(request, user)
                    else:
                        return 0

            project = Project(title=data['name_project'],
                              description=data['descr_project'],
                              type=str(data['trader'].id),
                              loc=data['loc'],
                              status=ProjectStatus.INACTIVE.value,
                              user=user)
            project.save()
            return project.id

        def generate_username(self, email):
            username = email.split("@")[0]
            if CustomUser.objects.filter(username=username).exists():
                while True:
                    username = email.split("@")[0] + '_' + str(random.randrange(1, 9999))
                    if not CustomUser.objects.filter(username=username).exists():
                        break
            return username


class ProjectCreatedView(TemplateView):
    template_name = 'project_created.html'