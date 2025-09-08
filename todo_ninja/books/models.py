import os
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip()


class Book(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    # cover = models.ImageField(upload_to='covers/', blank=True, null=True)

    class Meta:
        permissions = [
            ('can_administrate_lib', 'User can administrate the library'),
            ('can_approve_booking', 'User can approve the book booking')
        ]
        ordering = ['title']

    def __str__(self):
        return f'{self.title} by {self.author}'


class UploadedFiles(models.Model):
    file = models.FileField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    word_count = models.IntegerField()
    char_count = models.IntegerField()
    upladed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
    

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.exists(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)


class Messages(models.Model):
    message = models.TextField()


    def __str__(self):
        return self.message
