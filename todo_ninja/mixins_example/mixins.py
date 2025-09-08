from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from urllib.parse import urlsplit

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url

class SoftDeleteMixin:
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.deleted_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(success_url)
    

class CacheControllMixin:
    cache_timeout = 60

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        user = request.user
        if user and user.is_authenticated:
            return response
        response['Cache-Control'] = f'max-age={self.cache_timeout}'
        return response



class ExampleChangePermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "mixins_example.change_examplemodel"
    login_url = '/admin/'

    def dispatch(self, request, *args, **kwargs):
        if request.user and not request.user.is_authenticated:
            return self.handle_no_authenticated()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас немає прав для перегляду сторінки")
    
    def handle_no_authenticated(self):
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())

        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlsplit(resolved_login_url)[:2]
        current_scheme, current_netloc = urlsplit(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )
    
    
    