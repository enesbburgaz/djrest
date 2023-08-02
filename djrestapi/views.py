from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from .models import UserAccessInfo, Book
from ipware import get_client_ip
from .authentication import token_expire_handler, expires_in
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_ip_address = get_client_ip(request)[0].strip()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data['password'])
        user.save()
        UserAccessInfo.objects.create(user=user, ipaddress=user_ip_address)
        return Response({"message":"User successfully created", "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = User.objects.get(username=request.data["username"])
    if not authenticate(username=request.data["username"], password=request.data["password"]):
        return Response({"detail":"Not found."},status=status.HTTP_404_NOT_FOUND)
    token, _  = Token.objects.get_or_create(user = user)
    is_expired, token = token_expire_handler(token)
    return Response({'token': token.key,'expires_in_minutes': expires_in(token)/60})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book(request):
    books = Book.objects.all().values()
    return Response(books)