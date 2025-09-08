from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mixins_example.models import ExampleModel
from mixins_example.mixins import SoftDeleteMixin, CacheControllMixin, ExampleChangePermissionMixin



class SoftExampleDeleteView(SoftDeleteMixin, DeleteView):
    model = ExampleModel
    success_url = reverse_lazy('files_list')

class ExampleDeleteView(ExampleChangePermissionMixin, DeleteView):
    model = ExampleModel
    success_url = reverse_lazy('files_list')
    template_name = 'mixins_example/examplemodel_confirm_delete.html'


class ExampleListView(CacheControllMixin, ListView):
    model = ExampleModel
    template_name = 'mixins_example/list_example.html'
    context_object_name = 'examples'
    queryset = ExampleModel.objects.filter(is_deleted=False)
    cache_timeout = 311

    def get_queryset(self):
        qs =  super().get_queryset()
        search_name = self.request.GET.get('example_name')
        search_description = self.request.GET.get('example_description')
        if search_name:
            qs = qs.filter(name__icontains=search_name)
        if search_description:
            qs = qs.filter(description__icontains=search_description)
        return qs
    
