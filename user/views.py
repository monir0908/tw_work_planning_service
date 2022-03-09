import datetime

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

import jwt

from user.helpers import create_tokens
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsAdmin
from base.exceptions import UnprocessableEntity


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registration(request: Request) -> Response:
    email = request.data.get('email')
    try:
        User.objects.get(email=email)
        raise UnprocessableEntity(detail='email already exists', code=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        user = User()
        user.email = email
        user.set_password(raw_password=request.data.get('password'))
        user.mobile = request.data.get('mobile')
        user.alternative_mobile = request.data.get('alternative_mobile', None)
        user.address_one = request.data.get('address_one', None)
        user.address_two = request.data.get('address_two',None)
        user.dob = request.data.get('dob',None)
        user.nid = request.data.get('nid')
        user.is_worker = request.data.get('is_worker',False)
        user.date_joined = request.data.get('date_joined',None)
        user.gender = request.data.get('gender', 1)
        user.is_superuser = False
        user.is_staff = False
        user.is_active = False
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name', None)
        user.save()
        return Response(data={'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        raise ValidationError(detail='email and password required', code=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email__exact=email)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='invalid password', code=status.HTTP_400_BAD_REQUEST)
        access_token, refresh_token = create_tokens(user=user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='user not found', code=status.HTTP_404_NOT_FOUND)


class GetUsers(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.filter()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refreshed_token(request: Request) -> Response:
    if not request.user.is_active:
        raise ValidationError(detail='user is not active', code=status.HTTP_401_UNAUTHORIZED)
    access_token, refresh_token = create_tokens(user=request.user)
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    return Response(data=data, status=status.HTTP_201_CREATED)