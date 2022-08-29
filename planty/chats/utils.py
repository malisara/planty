from django.db.models import Q

from .models import Chat, Message


def all_chats_last_message(request):
    all_users_chats = Chat.objects.filter(Q(buyer=request.user) | Q(
        post__user=request.user))

    last_messages = []
    for chat in all_users_chats:
        last_message = Message.objects.filter(
            chat=chat).order_by('-date')[0]

        if len(last_message.message_reply) > 18:
            last_message.short = last_message.message_reply[:15] + '...'
        else:
            last_message.short = last_message.message_reply
        last_messages.append(last_message)

    def sort_by_date(message):
        return message.date
    return sorted(last_messages, key=sort_by_date, reverse=True)


def user_has_unread_message_context_processor(request):
    unread = False
    if request.user.is_authenticated:
        unread_buyer = has_unread_message(
            request,
            Chat.objects.filter(buyer=request.user),
            user_is_buyer=True,
        )
        unread_seller = has_unread_message(
            request,
            Chat.objects.filter(post__user=request.user),
            user_is_buyer=False,
        )
        unread = unread_buyer or unread_seller
    return {'has_unread_messages': unread}


def has_unread_message(request, chats, user_is_buyer):
    for chat in chats:
        messages = Message.objects.filter(
            chat=chat).exclude(sender=request.user)
        for message in messages:
            if user_is_buyer and not message.read_message_buyer:
                return True
            elif not user_is_buyer and not message.read_message_seller:
                return True
    return False
