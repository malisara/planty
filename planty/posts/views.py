from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.urls import reverse_lazy

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
