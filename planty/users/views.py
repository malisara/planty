from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import (ProfileUpdateForm, UserRegisterForm,
                    UserReviewForm, UserUpdateForm)
from .models import Review
from .utils import user_reviews_statistics


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
def view_profile(request, pk):
    user_profile_owner = User.objects.get(id=pk)
    average_rating, num_all_reviews = user_reviews_statistics(
        user_profile_owner)
    context = {
        'user_profile_owner': user_profile_owner,
        'average_rating': average_rating,
        'num_all_reviews': num_all_reviews,
    }
    return render(request, 'users/view_profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save(commit=False)
            user_form.save()
            messages.success(request, "Your account is updated")
            return redirect('view_profile', pk=request.user.id)

        else:
            messages.error(request, "Error: Profile wasn't updated")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/update_profile.html', context)


@login_required
def reviews(request, pk):
    try:
        user_profile_owner = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    try:
        already_commented = \
            Review.objects.get(Q(comment_author=request.user) &
                               Q(comment_reciever=user_profile_owner.profile))
        first_comment = False
        review_form = UserReviewForm(instance=already_commented)
        last_rating = already_commented.rating
    except ObjectDoesNotExist:
        first_comment = True
        review_form = UserReviewForm()
        last_rating = None

    if request.method == "POST":
        review_form = UserReviewForm(request.POST)

        if review_form.is_valid():
            if not first_comment:
                # Override existing instance
                already_commented.review = review_form.cleaned_data['review']
                already_commented.rating = request.POST.get('rating')
                already_commented.date = timezone.now()
                already_commented.save()
            else:
                review_instance = review_form.save(commit=False)
                review_instance.comment_author = request.user
                review_instance.comment_reciever = user_profile_owner.profile
                review_instance.rating = request.POST.get('rating')
                review_instance.date = timezone.now()
                review_instance.save()
        else:
            messages.error(request, "Ooops! Invalid review")

    all_reviews = Review.objects.filter(
        comment_reciever=user_profile_owner.profile).order_by('-date')
    average_rating, num_all_reviews = user_reviews_statistics(
        user_profile_owner)

    context = {
        'review_form': review_form,
        'user_profile_owner': user_profile_owner,
        'all_reviews': all_reviews,
        'average_rating': average_rating,
        'num_all_reviews': num_all_reviews,
        'first_comment': first_comment,
        'last_rating': last_rating,
    }

    return render(request, 'users/reviews.html', context)
