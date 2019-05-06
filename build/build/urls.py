"""build URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls.static import static
from buildsinfo import views
from vminfo import views as vminfo_views

# import mongonaut
# from mongonaut import urls

# admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.version),
    path(r'version/', views.version),
    re_path(r'^history/', views.history),
    re_path(r'^history/*', views.history_detail),
    path(r'versionlist.html', views.hf3wd),
    path(r'ats/versionlist.html', views.ats),
    path(r'vminfo/', vminfo_views.vminfo),

]
