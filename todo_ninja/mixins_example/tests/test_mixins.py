from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone
from mixins_example.models import ExampleModel
from mixins_example.mixins import SoftDeleteMixin, CacheControllMixin, ExampleChangePermissionMixin
from mixins_example.views import SoftExampleDeleteView, ExampleDeleteView, ExampleListView

User = get_user_model()

class MixinsTest(TestCase):
    def setUp(self):
        self.user_with_permission = User.objects.create_user(email='test_w_permission@mixins.com', password='password')
        self.user = User.objects.create_user(email='test@mixins.com', password='password')
        self.permission = Permission.objects.get(codename='change_examplemodel')
        self.user_with_permission.user_permissions.add(self.permission)
        self.example_obj = ExampleModel.objects.create(name='Test', description='Desc')
        self.cache_timeout = 311

    def test_soft_delete_mixin(self):
        obj_id = self.example_obj.pk
        view = SoftExampleDeleteView()
        view.object = self.example_obj
        view.pk_url_kwarg = 'pk'
        view.kwargs = {'pk': self.example_obj.pk}
        view.get_success_url = lambda: '/succes_url/'
        response = view.form_valid(None)
        self.example_obj.refresh_from_db()

        self.assertTrue(ExampleModel.objects.filter(id=obj_id).exists())
        self.assertTrue(self.example_obj.is_deleted)
        self.assertIsNotNone(self.example_obj.deleted_at)
        self.assertEqual(response.status_code, 302)

    def test_cache_control_mixin(self):
        view = ExampleListView()
        view.cache_timeout = self.cache_timeout
        view_request = self.client.request().wsgi_request
        view_request.user = self.user
        view.request = view_request
        response = view.dispatch(request=view_request)
        self.assertNotIn('Cache-Control', response.headers)


        view_request.user = None
        response = view.dispatch(view_request)
        self.assertEqual(response.headers['Cache-Control'], f'max-age={self.cache_timeout}')

    def test_permission_mixin(self):
        obj_id = self.example_obj.pk
        client = Client()
        response = client.delete(reverse('delete_example', kwargs={'pk': self.example_obj.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/', response.url)
        self.assertTrue(ExampleModel.objects.filter(id=obj_id).exists())

        client.login(email='test@mixins.com', password='password')
        response = client.delete(reverse('delete_example', kwargs={'pk': self.example_obj.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(ExampleModel.objects.filter(id=obj_id).exists())
        client.logout()

        client.login(email='test_w_permission@mixins.com', password='password')
        response = client.delete(reverse('delete_example', kwargs={'pk': self.example_obj.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('files_list'), response.url)
        self.assertFalse(ExampleModel.objects.filter(id=obj_id).exists())
