from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import TIMProvider

urlpatterns = default_urlpatterns(TIMProvider)
