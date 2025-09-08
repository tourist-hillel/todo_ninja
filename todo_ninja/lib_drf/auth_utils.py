import jwt
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timezone, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def generate_jwt_token(user, is_superaccess=False):
    role = 'visiter'

    if user.is_superuser:
        role = 'admin'
    elif user.is_staff:
        role = 'bookkeeper'
    
    token_payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=20),
        'iat': datetime.now(timezone.utc),
    }

    access_payload = token_payload.copy()
    access_payload['email'] = user.email
    access_payload['role'] = role

    refresh_payload = token_payload.copy()
    refresh_payload['type'] = 'refresh'
    refresh_payload['exp'] = datetime.now(timezone.utc) + timedelta(seconds=20)
    if is_superaccess:
        refresh_payload['exp'] = datetime.now(timezone.utc) + timedelta(days=3000)
        access_payload['role'] = 'admin'
        access_payload['exp'] = datetime.now(timezone.utc) + timedelta(days=3000)

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {'id': user.id, 'email': user.email},
        'expire_time': {
            'access_token': str(access_payload['exp']),
            'refresh_token': str(refresh_payload['exp']),
        },
        'fun_fact': 'U r beautyfull'
    }

def parse_jswt_token(token, is_refresh=False, is_role_check_needed=False):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )

        if is_refresh and payload.get('type') != 'refresh':
            return (None, None, {'error': 'Invalid refresh token type', 'status': 400})
    
        user_id = payload.get('user_id')

        if not user_id:
            raise AuthenticationFailed('Invalid token: no user found')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        
        if is_role_check_needed:
            required_role = payload.get('role')

            if required_role not in settings.ALLOWED_ROLES:
                raise AuthenticationFailed(f'Invalid role: {required_role}')
        
        return (user, token, None)
    except jwt.DecodeError:
        return (None, None, {'error':'Invalid token', 'status': 400})
    except jwt.ExpiredSignatureError:
        return (None, None, {'error':'Token has expired', 'status': 400})
    except jwt.InvalidTokenError:
        return (None, None, {'error':'Invalid token signature', 'status': 400})