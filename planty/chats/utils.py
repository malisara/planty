
from .models import Message, Chat
from django.db.models import Q


def return_list_last_messages_in_chat(request):
    all_users_chats = Chat.objects.filter(Q(buyer=request.user) | Q(
        post__user=request.user))

    list_last_messages_in_chat = []
    for chat in all_users_chats:
        last_message = Message.objects.filter(
            chat=chat).order_by('-date')[0]

        if len(last_message.message_reply) > 18:
            last_message.short = last_message.message_reply[:15] + '...'
        else:
            last_message.short = last_message.message_reply

        list_last_messages_in_chat.append(last_message)
    list_last_messages_in_chat[::-1]
    return list_last_messages_in_chat
