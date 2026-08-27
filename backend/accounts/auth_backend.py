from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """Allows users to authenticate with either their email address or username."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        if username is None or password is None:
            return None

        try:
            user = User.objects.filter(Q(email__iexact=username) | Q(username__iexact=username)).first()
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None
        return None
