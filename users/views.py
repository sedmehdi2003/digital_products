import random
import uuid

from django.core.cache import cache

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Device


# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone number')
        if not phone_number:
            return Response({'error': 'Phone number required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number)


        device = Device.objects.create(user=user)
        code = random.randint(100000, 999999)

        cache.set(str(phone_number), code, 2 * 60)

        return Response({'code':code})


class GetTokenView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone number')
        code = request.data.get('code')

        cached_code = cache.get(str(phone_number))
        if cached_code is None or str(code) != str(cached_code):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = str(uuid.uuid4())
        return Response({'token':token})



class LoginView(APIView):
    pass