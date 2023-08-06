from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class TIMProvider(OAuth2Provider):
    id = "tim"
    name = "TIM"
    account_class = ProviderAccount

    def get_default_scope(self):
        return ["profile"]

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("emails")[0]["email"],
            last_name=data.get("last_name"),
            first_name=data.get("given_name"),
            name=data.get("real_name"),
            username=data.get("username")
        )

    def extract_email_addresses(self, data):
        ret = []
        emails = data.get("emails")
        # First mail is automatically the primary one
        primary = True
        for email in emails:
            ret.append(EmailAddress(email=email.get("email"), verified=email.get("verified", False), primary=primary))
            primary = False
        return ret


provider_classes = [TIMProvider]
