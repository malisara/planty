from django.shortcuts import render, redirect
from .forms import (UserRegisterForm, UserUpdateForm,
                    ProfileUpdateForm, UserReviewForm)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Reviews
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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


def average_number_reviews(user_profile_owner):
    all_reviews = Reviews.objects.filter(
        comment_reciever_id=user_profile_owner.profile)
    sum_ratings = 0
    if len(all_reviews) > 0:
        for review in all_reviews:
            sum_ratings += review.rating

        reviews_average = sum_ratings / len(all_reviews)
        num_all_reviews = len(all_reviews)
    else:
        reviews_average = sum_ratings
        num_all_reviews = 0

    return reviews_average, num_all_reviews


@login_required
def view_profile(request, pk):
    user_profile_owner = User.objects.get(id=pk)
    reviews_average, num_all_reviews = average_number_reviews(
        user_profile_owner)
    context = {
        'user_profile_owner': user_profile_owner,
        'reviews_average': reviews_average,
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
def review(request, pk):
    user_profile_owner = User.objects.get(id=pk)
    try:
        already_commented = \
            Reviews.objects.get(Q(comment_author=request.user) &
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
                already_commented.date = datetime.now()
                already_commented.save()
            else:
                review_instance = review_form.save(commit=False)
                review_instance.comment_author = request.user
                review_instance.comment_reciever = user_profile_owner.profile
                review_instance.rating = request.POST.get('rating')
                review_instance.date = datetime.now()
                review_instance.save()
        else:
            messages.error(request, "Ooops! Invalid review")

    all_reviews = Reviews.objects.filter(
        comment_reciever_id=user_profile_owner.profile).order_by('-date')
    reviews_average, num_all_reviews = average_number_reviews(
        user_profile_owner)

    context = {
        'review_form': review_form,
        'user_profile_owner': user_profile_owner,
        'all_reviews': all_reviews,
        'reviews_average': reviews_average,
        'num_all_reviews': num_all_reviews,
        'first_comment': first_comment,
        'last_rating': last_rating,
    }

    return render(request, 'users/reviews.html', context)
