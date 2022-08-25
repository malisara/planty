from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Min, Q
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .models import Post
from planty.utils import paginate

POST_FORM_FIELDS = ['title', 'price',
                    'description', 'plant_image', 'plant_category']


class NewPostView(LoginRequiredMixin, CreateView):
    # Template name has to be: model_form.html, shares template
    # with update view
    model = Post
    fields = POST_FORM_FIELDS

    # Model form views provide a form_valid() implementation that saves
    # the model automatically.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    # Template name has to be model_detail.html
    model = Post

    # Add additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class UserIsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class UpdatePostView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = Post
    fields = POST_FORM_FIELDS


class DeletePostView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = Post
    # Needs a url to redirect after deleted
    success_url = reverse_lazy('explore')


def explore(request):
    if request.method == 'POST':
        return HttpResponseBadRequest()

    class DateFilters:
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'

    DATE_FILTERS = [
        (DateFilters.DAY, 'Last day'),
        (DateFilters.WEEK, 'Last week'),
        (DateFilters.MONTH, 'Last month'),
    ]

    class SortBy:
        DATE_DESCENDING = "newer"
        DATE_ASCENDING = "older"
        PRICE_DESCENDING = "higher"
        PRICE_ASCENDING = "lower"

    SORT_BY = [
        (SortBy.DATE_DESCENDING, 'Oldest first'),
        (SortBy.DATE_ASCENDING, 'Newest first'),
        (SortBy.PRICE_DESCENDING, 'Price hight to low'),
        (SortBy.PRICE_ASCENDING, 'Price low to high'),
    ]

    # Categories
    user_categories = request.GET.getlist('category')

    if len(user_categories) == 0:  # No category checkbox is selected
        posts = Post.objects.all()
    else:
        q = Q()
        for user_category in user_categories:
            q = q | Q(plant_category=user_category)
        posts = Post.objects.filter(q)

    # Price range
    min_max_prices = Post.objects.all().aggregate(Min('price'), (Max('price')))
    max_price = min_max_prices['price__max']
    min_price = min_max_prices['price__min']

    user_max_price = request.GET.get('price_value')

    if user_max_price is not None:
        posts = posts.filter(price__lte=user_max_price)

    # Basic Search
    user_searched = request.GET.get('searched')
    if user_searched is not None and user_searched != "":
        posts = posts.filter(
            title__icontains=user_searched)

    # Date Posted (doesn't work for different timezones)
    user_date = request.GET.get('date')

    if user_date is not None:
        if user_date == DateFilters.DAY:
            date_filter = 1
        elif user_date == DateFilters.WEEK:
            date_filter = 7
        elif user_date == DateFilters.MONTH:
            date_filter = 30
        else:
            return HttpResponseBadRequest()

        posts = posts.filter(date_posted__gte=timezone.now() -
                             timedelta(days=date_filter))

    # Sort Results
    sort_by = request.GET.get('sort')

    if sort_by is None or sort_by == SortBy.DATE_ASCENDING:
        posts = posts.order_by('-date_posted')
    elif sort_by == SortBy.DATE_DESCENDING:
        posts = posts.order_by('date_posted')
    elif sort_by == SortBy.PRICE_DESCENDING:
        posts = posts.order_by('-price')
    elif sort_by == SortBy.PRICE_ASCENDING:
        posts = posts.order_by('price')
    else:
        return HttpResponseBadRequest()

    # Pagination
    posts = paginate(request, posts, 12)

    context = {
        'categories': Post.PLANT_CATEGORIES,
        'max_price': max_price,
        'min_price': min_price,
        'posts': posts,
        'date_filters': DATE_FILTERS,
        'sort_by': SORT_BY,
    }
    return render(request, 'posts/explore.html', context)
