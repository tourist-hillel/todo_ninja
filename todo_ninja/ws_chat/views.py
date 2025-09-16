from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from ws_chat.forms import ChatUserCreationForm


@login_required
def index(request, room_name):
    return render(request, 'chat/index.html', {'room_name': room_name})


def register(request):
    if request.method == 'POST':
        form = ChatUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successfull!!!')
            return redirect('chat', room_name='start-room')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ChatUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
