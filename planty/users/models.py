from django.db import models
from django.contrib.auth.models import User
from planty.utils import save_cropped_image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default-profile-picture.jpg',
                              upload_to='profile_pictures')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_cropped_image(self.image.path, 200)


# TODO Reviews model
