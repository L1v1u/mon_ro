from django.urls import path, include
from .views import ProjectsView, CreateProjectView, ProjectCreatedView

urlpatterns = [
      path('', ProjectsView.as_view(), name="projects_listing"),
      path('create', CreateProjectView.as_view(), name="create_project"),
      path('success', ProjectCreatedView.as_view(), name="project_created"),



]
