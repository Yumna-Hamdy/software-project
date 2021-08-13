from django.http import request
from rest_framework import generics, status, views
from django.shortcuts import render, redirect
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import Account
from project.utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from project.utils import Util
from rest_framework import permissions,viewsets
from project.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes




class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = Account.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('accounts:email-verify')
        absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hi' + user.username + ' Use link to verify \n' + absurl
        data = {'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Verify Your Email'}
        Util.send_email(data)
        
        
        
        
        
        
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description',
        type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=["HS256"])
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Succesfully activated'},
                            status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CheckPassword(generics.GenericAPIView):
    serializer_class = CheckPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('accounts:password-reset-confirm',
                                    kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site+relative_link
            email_body = 'Hello,\n Use link below to reset your password  \n'
            + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset you password'}

            Util.send_email(data)
            return Response({'Success':
                            'We have sent you a link to reset password'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'fail': 'qwaqwa'}, status=status.HTTP_200_OK)


class PasswordTokenCheck(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid Token, Request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credential Valid',
                             'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
            # check that the user havent used token twice
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Invalid Token, Request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Success': True, 'message': 'Password Reset Success'},
                        status=status.HTTP_200_OK)

class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    
    def put(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            # Check the old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # Change to the new password
            user.set_password(serializer.data.get('new_password'))
            user.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }
            return Response(response, status = status.HTTP_200_OK)

    

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def DeleteAccount(request):
    user = request.user
    user=auth.authenticate(email=user.email, password=request.data['password'])
    if not user:
        return Response(
            {'stat': 'incorrect password'},status=status.HTTP_400_BAD_REQUEST)
    user.delete()
    return Response({'stat': 'ok'}, status=status.HTTP_200_OK)

    
