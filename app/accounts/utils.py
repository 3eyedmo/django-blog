import string


from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers


def send_email(email, token = None, subject=None, current_site=None):
    if not current_site:
        current_site = "http://localhost:8000/"
    else:
        current_site = "http://" + current_site

    if not subject:
        subject = "account activation" 

    message = f"you need to click following link {current_site}"
    if token:
        message += f"?token={token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def valid_password(password1, password2):
    print(password1, password2)
    if password1 != password2:
        raise serializers.ValidationError("passwords are not same")

    if not 8<=len(password2)<=25:
        raise serializers.ValidationError("passwords must be between 8 and 25 charecters")
    
    if password2 == password2.lower():
        raise serializers.ValidationError("passwords must contain atleast one uppercase charecter")

    if password2 == password2.upper():
        raise serializers.ValidationError("passwords must contain atleast one lowercase charecter")

    digits = string.digits
    if not any(char in digits for char in password2):
        raise serializers.ValidationError("passwords must contain atleast one digit.")

    # for special charecters we can use punctuation: from string import punctuation