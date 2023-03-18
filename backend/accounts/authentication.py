from django.conf import settings
from magic_admin import Magic
from magic_admin.error import DIDTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser

from dotenv import load_dotenv
import os
load_dotenv()

magic_secret = os.getenv("MAGIC_LINK_SECRET")
magic = Magic(api_secret_key=magic_secret)

class MagicAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        did_token = auth_header.split('Bearer ')[1]

        try:
            magic.Token.validate(did_token)
            issuer = magic.Token.get_issuer(did_token)
        except DIDTokenError as e:
            raise AuthenticationFailed('DID Token is invalid: {}'.format(e))

        user, _ = CustomUser.objects.get_or_create(email=issuer, did=issuer)
        return (user, None)
