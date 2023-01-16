from rest_framework import serializers
from .models import Users
import random
from django.core.mail import send_mail
from django.conf import settings


def send_otp_mail(email):
    subject = 'Registration Mail'
    otp = random.randint(10000, 100000)
    message = f'Your OTP is {otp}'
    from_email = settings.EMAIL_HOST
    send_mail(
        subject,
        message,
        from_email,
        [email],
        fail_silently=False,
    )
    return otp


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'is_verified', 'otp']

    def validate(self, attrs):
        attrs['otp'] = send_otp_mail(attrs['email'])
        return attrs
