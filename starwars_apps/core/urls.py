from django.urls import path

from starwars_apps.core.views import HomeView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
