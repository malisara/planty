from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f"Account for {username} is created")
            return redirect('login')
        else:
            messages.error(request, "User creation unsuccessful")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, pk):
    user_page_owner = User.objects.get(id=pk)
    context = {
        'user_page_owner': user_page_owner,
    }
    return render(request, 'users/profile.html', context)


# TODO Update Profile
