from django.urls import path
from mixins_example.views import ExampleDeleteView, SoftExampleDeleteView, ExampleListView


urlpatterns = [
    path('<int:pk>/file_delete/', ExampleDeleteView.as_view(), name='delete_example'),
    path('<int:pk>/file_delete_soft/', SoftExampleDeleteView.as_view(), name='delete_example_soft'),
    path('files_list/', ExampleListView.as_view(), name='files_list')
]