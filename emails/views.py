from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializers, send_otp_mail
from .models import Users
import time

# Create your views here.


class OtpApi(APIView):
    @staticmethod
    def post(request):
        data = request.data
        try:
            serializer = UserSerializers(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'status': 200, 'message': 'OTP sent successfully check mail'})
        except Exception as e:
            return Response({'status': 400, 'message': 'something went wrong',
                             'data': str(e)})


class VerifyOTP(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            user = Users.objects.filter(email=data.get('email'), otp=data.get('otp')).values('time').first()
            if not user:
                return Response({'status': 400, 'message': 'OTP Not Matched'})
            if time.time()-user.get('time') > 700:
                return Response({'status': 400, 'message': 'OTP Expired'})
            Users.objects.filter(email=data.get('email')).update(is_verified=True)
            return Response({'status': 200, 'message': 'Account Verified', 'data': {}})
        except Exception as e:
            return Response({'status': 400, 'message': 'something went wrong',
                             'data': str(e)})


class RegenerateOTP(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            otp = send_otp_mail(data.get('email'))
            user = Users.objects.filter(email=data.get('email')).update(otp=otp, time=time.time())
            return Response({'status': 200, 'message': 'OTP sent successfully check mail'})
        except Exception as e:
            return Response({'status': 400, 'message': 'something went wrong',
                             'data': str(e)})
