from PIL import Image
from django.core.paginator import Paginator

IGNORED_IMAGES = ['default_plant_image.jpg', 'default-profile-picture.jpg']


def crop_center(img, cropped_width, cropped_height):
    # Crop the central area of the image
    img_width, img_height = img.size
    return img.crop(((img_width - cropped_width) // 2,
                    (img_height - cropped_height) // 2,
                    (img_width + cropped_width) // 2,
                    (img_height + cropped_height) // 2))


def crop_max_square(img):
    # Crop the largest square
    min_dim = min(img.size)
    return crop_center(img, min_dim, min_dim)


def save_cropped_image(image_path, cropped_dim):
    for ignored_image in IGNORED_IMAGES:
        if image_path.endswith(ignored_image):
            return

    img = Image.open(image_path)
    img_cropped = crop_max_square(img)

    if img_cropped.height > cropped_dim:
        img_cropped.thumbnail((cropped_dim, cropped_dim))

    img_cropped.save(image_path)


def paginate(request, instances, number_instances):
    paginator = Paginator(instances, number_instances)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
