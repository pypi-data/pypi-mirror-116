import requests
from allauth.socialaccount.app_settings import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import TIMProvider


class TIMOAuth2Adapter(OAuth2Adapter):
    provider_id = TIMProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})

    if "TIM_HOST" in settings:
        auth_host = settings.get("TIM_HOST")
        oauth_host = auth_host
    else:
        auth_host = "http://localhost"
        oauth_host = "http://tim:5000"

    access_token_url = f"{oauth_host}/oauth/token"
    authorize_url = f"{auth_host}/oauth/authorize"
    profile_url = f"{oauth_host}/oauth/profile"

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            headers={"Authorization": f"Bearer {token.token}"}
        )
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(TIMOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(TIMOAuth2Adapter)
