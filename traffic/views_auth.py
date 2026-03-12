# File: C:\Users\Dell\Desktop\atms-vms-backend\traffic\views_auth.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    """User login endpoint"""
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'message': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to get user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Check password
        if not user.check_password(password):
            return Response({
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user is active
        if not user.is_active:
            return Response({
                'message': 'Account is inactive'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generate or get token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': 'Admin' if user.is_staff else 'User',
            },
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """Send password reset code to email"""
    
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'message': 'Email not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Generate 6-digit code
        code = ''.join(random.choices(string.digits, k=6))

        # Save code to user profile (create or update)
        # You need to create a Profile model or use a simple cache
        # For now, we'll store in session/cache
        from django.core.cache import cache
        cache.set(f'reset_code_{email}', code, 600)  # 10 minutes

        # Send email
        try:
            send_mail(
                subject='🔑 ATMS-VMS Password Reset Code',
                message=f'''
Hello {user.first_name or user.username},

Your password reset code is: {code}

This code will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
ATMS-VMS Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Error sending email: {e}')
            return Response({
                'message': 'Error sending email. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': 'Reset code sent to email'
        }, status=status.HTTP_200_OK)


class VerifyResetCodeView(APIView):
    """Verify reset code"""
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({
                'message': 'Email and code are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check code
        from django.core.cache import cache
        saved_code = cache.get(f'reset_code_{email}')

        if not saved_code or saved_code != code:
            return Response({
                'message': 'Invalid or expired code'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'message': 'Code verified successfully'
        }, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """Reset password with verification code"""
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')

        if not email or not code or not new_password:
            return Response({
                'message': 'Email, code, and new password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6:
            return Response({
                'message': 'Password must be at least 6 characters'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'message': 'Email not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verify code
        from django.core.cache import cache
        saved_code = cache.get(f'reset_code_{email}')

        if not saved_code or saved_code != code:
            return Response({
                'message': 'Invalid or expired code'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Reset password
        user.set_password(new_password)
        user.save()

        # Delete code from cache
        cache.delete(f'reset_code_{email}')

        return Response({
            'message': 'Password reset successfully'
        }, status=status.HTTP_200_OK)
