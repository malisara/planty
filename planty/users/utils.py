
from .models import Review


def user_reviews_statistics(user_profile_owner):
    all_reviews = Review.objects.filter(
        comment_reciever=user_profile_owner.profile)
    sum_ratings = 0
    if len(all_reviews) > 0:
        for review in all_reviews:
            sum_ratings += review.rating

        average_rating = sum_ratings / len(all_reviews)
        num_all_reviews = len(all_reviews)
    else:
        average_rating = sum_ratings
        num_all_reviews = 0

    return average_rating, num_all_reviews
