import json

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import datetime_to_epoch

from validators import ValidationFailure

User = get_user_model()


class VerficationPayload(Token):
    token_type = "verify"
    verify_secret = settings.VERIFICATION_EMAIL_PAYLOAD.get('SALTING', "secret")
    lifetime = settings.VERIFICATION_EMAIL_PAYLOAD.get('LIFETIME', None)

    def set_exp(self, claim='exp', from_time=None, lifetime=None):
        if not from_time:
            from_time = self.current_time
        
        if not lifetime:
            lifetime = self.lifetime
        self.payload[claim] = datetime_to_epoch(from_time + lifetime)

    @classmethod
    def for_user(cls, user: User, subject: str, value):
        user_id = user.id
        identity = {
            "user_id": user_id,
            "secret_key": cls.verify_secret,
            subject: value
        }
        identity = json.dumps(identity)
        token = cls()
        token['identity'] = identity
        return token
    
    def get_identity(self):
        identity = self.payload.get("identity", None)
        identity = json.loads(identity)
        return identity
    
    def for_registration_verify(self):
        identity = self.get_identity()
        user_id = identity.get("user_id", None)
        subject = identity.get("is_active", None)
        user = User.objects.get(id=user_id)
        is_active = user.is_active
        if not is_active and not subject:
            user.is_active = True
            user.save()
            return True
        raise ValidationFailure("information is fake.")