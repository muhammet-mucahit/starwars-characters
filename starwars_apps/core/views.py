from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(TemplateView, LoginRequiredMixin):
    """Homepage of the website"""

    template_name = 'core/home.html'
