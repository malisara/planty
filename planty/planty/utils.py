# Crop the central area of the image
def crop_center(img, cropped_width, cropped_height):
    img_width, img_height = img.size
    return img.crop(((img_width - cropped_width) // 2,
                    (img_height - cropped_height) // 2,
                    (img_width + cropped_width) // 2,
                    (img_height + cropped_height) // 2))


# Crop the largest square
def crop_max_square(img):
    min_dim = min(img.size)
    return crop_center(img, min_dim, min_dim)
