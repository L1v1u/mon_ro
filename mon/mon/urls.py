"""mon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from search.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("projects/", include("projects.urls")),
    path("cauta/", include("search.urls")),
    path("c/", include("cms.urls")),
    path("customer/", include("users.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='home'),
    path("mester/", include("traders.urls")),

    # path("traders/", include("traders.urls")),
    # path("users/", include("users.urls")),
    # path('api/trigger_build/', BuildTrigger.as_view()),

]
