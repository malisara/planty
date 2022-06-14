from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator
from django.urls import reverse
from planty.utils import crop_max_square
from PIL import Image


class Post(models.Model):

    OUTDOOR = 'O'
    INDOOR = 'I'
    FLOWERS = 'F'
    NO_CATEGORY = 'ALL'

    PLANT_CHOICES = [
        (OUTDOOR, 'Outdoor'),
        (INDOOR, 'Indoor'),
        (FLOWERS, 'Flower'),
        (NO_CATEGORY, 'No category')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_category = models.CharField(
        max_length=3,
        choices=PLANT_CHOICES,
        default=NO_CATEGORY,
    )
    title = models.CharField(max_length=30)
    date_posted = models.DateTimeField(
        default=datetime.now)
    description = models.CharField(max_length=100)
    plant_image = models.ImageField(
        default='default_plant_image.jpg', upload_to='plant_pics')
    price = models.FloatField(
        default='0.00', verbose_name='Price in €',
        validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.title

    # Don’t need to provide a success_url for CreateView or UpdateView
    # they will use get_absolute_url() on the model
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def shorten_title(self):
        if len(self.title) > 30:
            self.short_title = f" {self.title[:30]} ..."
        else:
            self.short_title = self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.plant_image.path)
        img_cropped = crop_max_square(img)

        if img_cropped.height > 400:
            img_cropped.thumbnail((400, 400))

        img_cropped.save(self.plant_image.path)
