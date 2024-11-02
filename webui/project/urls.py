"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),

    path('stats/', views.statsboard, name='statsboard'),
    path('stats/create/', views.add_statistic_page, name='add_statistic'),
    path('stats/delete/', views.delete_statistic_page, name='delete_statistic'),
    path('stats/v/<str:target_name>/', views.view_target_stats, name='view_target_stats'),

    path('api/ping/', views.ping, name='ping'),
    path('api/getstats/', views.getstats, name='get_stats'),
    path('api/add_statistic/', views.create_new_statistic, name='add_statistic'),
    path('api/delete_statistic/', views.delete_statistic, name='delete_statistic'),
    path('api/enter_stat_data/', views.enter_stat_data, name='enter_stat_data'),
    path('api/delete_stat_data/', views.delete_stat_data, name='delete_stat_data'),
]
