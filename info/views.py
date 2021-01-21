from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth


class IndexView(View):
    template_name = 'info/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class AccountView(LoginRequiredMixin, View):
    template_name = 'info/account.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, View):
    template_name = 'info/account_settings.html'

    def get(self, request):
        user = request.user

        try:
            github_login = user.social_auth.get(provider='github')
        except UserSocialAuth.DoesNotExist:
            github_login = None

        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None
        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
        context = {
            'github_login': github_login,
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        }
        return render(request, self.template_name, context)
