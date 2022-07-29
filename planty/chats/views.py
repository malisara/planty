from django.shortcuts import redirect, render
from .models import Message, Chat
from .forms import MessageForm
from posts.models import Post
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from .utils import all_chats_last_message


@login_required
def first_message(request, pk):
    try:
        post_instance = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    try:  # Chat already exists
        chat = Chat.objects.get(Q(buyer=request.user) & Q(post=post_instance))
        return redirect('chat', pk=chat.id)
    except ObjectDoesNotExist:
        form = MessageForm()
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                chat = Chat(post=post_instance, buyer=request.user)
                chat.save()
                message = form.save(commit=False)
                message.chat = chat
                message.read_message_seller = False
                message.sender = request.user
                message.save()
                return redirect('chat', pk=chat.id)
            else:
                messages.error(
                    request, "Your message wasn't sent. Please try again.")

        context = {
            'form': form,
            'post': post_instance,
        }
        return render(request, 'chats/first_message.html', context)


@login_required
def chat(request, pk):
    try:
        chat = Chat.objects.get(Q(id=pk) & (
            Q(buyer=request.user) | Q(post__user=request.user)))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    all_messages_in_chat = Message.objects.filter(chat=chat).order_by('date')
    # Only needed for all chats in the sidebar
    side_messages = all_chats_last_message(request)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            if request.user == chat.buyer:
                message.read_message_seller = False
            else:
                message.read_message_buyer = False
            message.save()
        else:
            messages.error(
                request, "Your message wasn't sent. Please try again.")
    else:  # Mark messages as read when user opens the chat
        form = MessageForm()
        for message in all_messages_in_chat:
            if request.user == chat.buyer:
                message.read_message_buyer = True
            else:
                message.read_message_seller = True
            message.save()

    context = {
        'all_messages_in_chat': all_messages_in_chat,
        'form': form,
        'buyer': chat.buyer,
        'post': chat.post,
        'all_chats_last_message': side_messages
    }

    return render(request, 'chats/all-chats-selected.html', context)


@login_required
def list_of_all_chats(request):  # When no chat is opened
    side_messages = all_chats_last_message(request)
    return render(request, 'chats/all-chats-none-selected.html',
                  ({'all_chats_last_message': side_messages}))
