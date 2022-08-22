from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from planty.utils import save_cropped_image


class Post(models.Model):

    class Category:
        OUTDOOR = 'O'
        INDOOR = 'I'
        FLOWERS = 'F'
        NO_CATEGORY = 'ALL'

    PLANT_CATEGORIES = [
        (Category.OUTDOOR, 'Outdoor'),
        (Category.INDOOR, 'Indoor'),
        (Category.FLOWERS, 'Flower'),
        (Category.NO_CATEGORY, 'No category')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_category = models.CharField(
        max_length=3,
        choices=PLANT_CATEGORIES,
        default=Category.NO_CATEGORY,
    )
    title = models.CharField(max_length=30)
    date_posted = models.DateTimeField(
        default=timezone.now)
    description = models.CharField(max_length=100)
    plant_image = models.ImageField(
        default='default_plant_image.jpg', upload_to='plant_pics')
    price = models.FloatField(
        default=0.00, verbose_name='Price in €',
        validators=[MinValueValidator(0.0)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shorten_title()

    def __str__(self):
        return self.title

    # Don’t need to provide a success_url for CreateView or UpdateView
    # they will use get_absolute_url() on the model
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def shorten_title(self):
        if len(self.title) > 30:
            self.short_title = f" {self.title[:30]} ..."
        else:
            self.short_title = self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_cropped_image(self.plant_image.path, 400)
