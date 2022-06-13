from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from planty.utils import crop_max_square


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default-profile-picture.jpg',
                              upload_to='profile_pictures')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        img_cropped = crop_max_square(img)

        if img_cropped.height > 200:
            img_cropped.thumbnail((200, 200))

        img_cropped.save(self.image.path)


# TODO Reviews model
