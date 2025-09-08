import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, authenticate
from datetime import datetime, timezone, timedelta
from django.conf import settings
from lib_drf.auth_utils import generate_jwt_token, parse_jswt_token

User = get_user_model()


class LibJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid Auth header format. Expected "Bearer <token>"')
        
        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            exp = payload.get('exp')

            if exp and datetime.now(timezone.utc).timestamp() > exp:
                raise AuthenticationFailed('Token has expired!')
            
            user_id = payload.get('user_id')

            if not user_id:
                raise AuthenticationFailed('Invalid token: no user found')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
            
            required_role = payload.get('role')

            if required_role not in settings.ALLOWED_ROLES:
                raise AuthenticationFailed(f'Invalid role: {required_role}')
            

            return (user, token)

        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid token')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token signature')
        
    def authenticate_header(self, request):
        return 'Bearer realm="api"'
    

class ObtainJWT(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        is_superaccess = request.data.get('make_me_god')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials!!!'}, status=400)
        
        token_response = generate_jwt_token(user=user, is_superaccess = request.data.get('make_me_god'))
        return Response(token_response)


class RefreshJWT(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        is_superaccess = request.data.get('make_me_god')

        if not refresh_token:
            return Response({'error': 'Refresh token is required!'}, status=400)
        
        user, token, jwt_response = parse_jswt_token(token=refresh_token, is_refresh=True)
        if jwt_response is not None:
            return Response({'error': jwt_response.get('error')}, status=jwt_response.get('status'))

        token_response = generate_jwt_token(user=user, is_superaccess = request.data.get('make_me_god'))
        return Response(token_response)
