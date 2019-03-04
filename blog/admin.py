from django.contrib import admin
from .models import Post, Comment, Chat, RoomChat, MessageChatRoom

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Chat)
admin.site.register(RoomChat)
admin.site.register(MessageChatRoom)
