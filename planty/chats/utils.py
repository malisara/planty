from .models import Message, Chat
from django.db.models import Q


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
