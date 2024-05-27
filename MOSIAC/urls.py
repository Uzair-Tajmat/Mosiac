"""
URL configuration for MOSIAC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('First/',views.First,name='First'),
    path('pausedContent/', views.pausedContent, name='pausedContent'),
    path('closingWindow/',views.closingWindow,name='closingWindow'),
    path('fetch_videos/', views.fetch_videos, name='fetch_videos'),
    path('First/Main/Main/handle_pause_time/', views.handle_pause_time, name='handle_pause_time'),
    path('First/Main/',views.Main,name='Main'),
    path('First/Main/Open',views.OpenMain,name='OpenMain'),
    path('First/Main/AllContent',views.AllContent,name='AllContent'),
    path('First/Upload/',views.Upload,name="Upload")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)