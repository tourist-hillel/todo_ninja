from django.contrib import admin
from django import forms
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
import csv
from books.models import Book, UploadedFiles, Messages, Author


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'published_date': AdminDateWidget(),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 35})
        }
    
    cover_preview = forms.ImageField(required=False, label='Cover Preview')
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise forms.ValidationError('Title must be less or equal than 50 chars')
        return title
    
class PublishedYearFilter(admin.SimpleListFilter):
    title = 'Publication Year'
    parameter_name = 'published_date'


    def lookups(self, request, model_admin):
       years = Book.objects.values('published_date__year').distinct()
       return [(str(year['published_date__year']), str(year['published_date__year'])) for year in years]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(published_date__year=self.value())
        return queryset

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'published_date', 'description', 'price', 'is_available', 'cover_image_preview')
    list_editable = ('price', 'is_available')
    list_filter = ('is_available', 'author', PublishedYearFilter)
    search_fields = ('title', 'author')
    # fields = ('title', 'author', 'published_date', 'description', 'price', 'is_available', 'cover', 'cover_preview')

    fieldsets = (
        ('Basic info', {
            'fields': ('title', 'author'),
            'description': 'General information'
        }),
        ('Details', {
            'fields': ('published_date', 'price', 'description', 'is_available'),
            'classes': ('collapse',),
        }),
        ('Cover', {
            'fields': ('cover', 'cover_preview'),
            'description': 'Upload your book cover'
        }),
    )
    actions = ['mark_as_available', 'mark_as_unavailable', 'eport_to_csv']


    def cover_image_preview(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" width="50" height="50" />')
        return 'No image'
    cover_image_preview.short_description = "Cover"

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, 'Selected books marked as available')
    mark_as_available.short_description = 'Mark selected books as available'

    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, 'Selected books marked as unavailable')
    mark_as_unavailable.short_description = 'Mark selected books as unavailable'

    def eport_to_csv(self, request, queryset):
        response =  HttpResponse(content_type='text/cvs')
        response['Content-Disposition'] = 'attachment; filename="books_export.csv"'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Author', 'Published Date', 'Price', 'Available'])
        for book in queryset:
            writer.writerow([book.title, book.author, book.published_date, book.price, book.is_available])
        return response
    eport_to_csv.short_description = 'Export selected books to CSV'

    list_template = 'admin/books_list.html'
    change_list_template = 'admin/books_list.html'
    change_form_template = 'admin/book_change_form.html'

    class Media:
        css ={
            'all': ('admin/css/book_admin.css',),
        }
        js = ('admin/js/books_admin.js',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashbord/', self.admin_site.admin_view(self.dashboard_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        tootal_books = Book.objects.count()
        available_books = Book.objects.filter(is_available=True).count()
        context = {
            'title': 'Book Statistics Dashboard',
            'total_books': tootal_books,
            'available_books': available_books,
        }
        return TemplateResponse(request, 'admin/book_dashboard.html', context)


admin.site.register(UploadedFiles)
admin.site.register(Messages)
admin.site.register(Author)
