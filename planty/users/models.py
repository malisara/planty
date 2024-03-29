from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from planty.utils import save_cropped_image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default-profile-picture.jpg',
                              upload_to='profile_pictures')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_cropped_image(self.image.path, 200)


class Review(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_reciever = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review = models.CharField(max_length=250)
    rating = models.IntegerField(default=5, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)
