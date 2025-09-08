from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from users_app.forms import UserPermissionsForm
from books.models import Book

User = get_user_model()

@login_required
@permission_required('auth.change_permission', raise_exception=True)
def manage_user_permissions(request):
    users = User.objects.all()
    form = None
    selected_user = None

    # user_id = request.GET.get('user_id')
    # if user_id:
    #     pass
    if request.method == 'POST':
        if user_id:= request.POST.get('user_id'):
            selected_user = get_object_or_404(User, id=user_id)
            form = UserPermissionsForm(request.POST, user=selected_user)
            if form.is_valid():
                selected_user.user_permissions.clear()
                permissions = form.cleaned_data['permissions']
                for permission_id in permissions:
                    permission = Permission.objects.get(id=permission_id)
                    selected_user.user_permissions.add(permission)
                messages.success(request, f'Дозволи для {selected_user} оновлено')
                return redirect('manage_user_permissions')
        form = UserPermissionsForm(user=None)
    else:
        if user_id:= request.GET.get('user_id'):
            selected_user = get_object_or_404(User, id=user_id)
            form = UserPermissionsForm(user=selected_user)
        else:
            form = UserPermissionsForm(user=None)
    context = {
        'users': users,
        'selected_user': selected_user,
        'form': form
    }
    return render(request, 'manage_permission.html', context)


@login_required
@permission_required('books.can_administrate_lib', raise_exception=True)
def check_permission(request):
    books = Book.objects.all()
    return render(request, 'simple_books_list.html', {'books': books})
