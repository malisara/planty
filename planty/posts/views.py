from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Max
from datetime import datetime, timedelta
from django.core.paginator import Paginator

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
    # TODO change url to explore page
    success_url = reverse_lazy('login')


def explore(request):
    if request.method == 'POST':
        # TODO: return BadRequest
        pass

    # Categories
    user_categories = request.GET.getlist('category')

    if len(user_categories) == 0:  # No category checkbox is selected
        posts_to_display = Post.objects.all()

    else:
        if 'ALL' in user_categories:
            posts_to_display = Post.objects.all()
        else:
            if 'O' in user_categories:
                cat1 = 'O'
            else:
                cat1 = None

            if 'I' in user_categories:
                cat2 = 'I'
            else:
                cat2 = None

            if 'F' in user_categories:
                cat3 = 'F'
            else:
                cat3 = None

            posts_to_display = Post.objects.filter(Q(plant_category=cat1)
                                                   | Q(plant_category=cat2)
                                                   | Q(plant_category=cat3))

    # Price range
    max_aggregated_value = Post.objects.all().aggregate(Max('price'))
    max_price = max_aggregated_value['price__max']

    user_max_price = request.GET.get('price_value', None)

    if user_max_price is not None:
        posts_to_display = posts_to_display.filter(price__lte=user_max_price)

    # Basic Search
    searched = request.GET.get('searched', None)
    if searched is not None and searched != "":
        posts_to_display = posts_to_display.filter(title__icontains=searched)

    # Date Posted (doesn't work for different timezones)
    last_day = datetime.now() - timedelta(days=1)
    last_week = datetime.now() - timedelta(days=7)
    last_month = datetime.now() - timedelta(days=30)

    user_date = request.GET.get('date', None)

    if user_date is not None:
        if user_date == "day":
            date_filter = last_day
        elif user_date == "week":
            date_filter = last_week
        else:
            date_filter = last_month

        posts_to_display = posts_to_display.filter(
            date_posted__gte=date_filter)

    # Sort Results
    sort_by = request.GET.get('sort-by', None)

    if sort_by is None or sort_by == "newer":
        posts = posts_to_display.order_by('-date_posted')
    elif sort_by == "older":
        posts = posts_to_display.order_by('date_posted')
    elif sort_by == "higher":
        posts = posts_to_display.order_by('-price')
    else:
        posts = posts_to_display.order_by('price')

    # Pagination
    post_list = posts
    paginator = Paginator(post_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Post.PLANT_CATEGORIES

    context = {
        'categories': categories,
        'max_price': max_price,
        'page_obj': page_obj
    }
    return render(request, 'posts/explore.html', context)
