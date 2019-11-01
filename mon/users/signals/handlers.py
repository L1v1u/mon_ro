from django.contrib.auth.signals import user_logged_in
from django.contrib import messages


def add_message_for_unconfirmed(sender, user, request, **kwargs):
    if not user.is_confirmed:
        messages.info(request, 'Please confirm your email address to complete the registration')

user_logged_in.connect(add_message_for_unconfirmed)