from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class NewPostView(LoginRequiredMixin, CreateView):
    # Template name has to be: model_form.html, shares template with update view
    model = Post
    fields = ['title', 'price', 'description', 'plant_image', 'plant_category']

    # Model form views provide a form_valid() implementation that saves
    # the model automatically.
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    # Template name has to be model_viewtype.html
    model = Post
    #context_object_name = "post"

    # Add additinal context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
