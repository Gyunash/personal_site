from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.context_processors import csrf
from django.forms.models import modelformset_factory
from django.template.loader import render_to_string
from django.views.generic import FormView, View
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core import serializers
from django.contrib import auth
from django.urls import reverse
from django.db.models import Q
from django.views import View
from .models import *
from .forms import *
import json


""" ВЫВОД ПОСТОВ """
def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all() # взять все объекты из созданного DICT
    
    posts_quantity = 2
    paginator = Paginator(posts, posts_quantity)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    is_pagin = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page': page,
        'is_pagin': is_pagin,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, "blog/index.html", context=context)


""" ПОДРОБНОЕ ОТОБРАЖЕНИЕ ПОСТОВ """
class PostDetail(View):
    model = Post
    template = "blog/post_detail.html"

    def get(self, request, id, slug):

        post = get_object_or_404(Post, id=id, slug__iexact=slug)
        comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comment_form = CommentForm()

        context = {self.model.__name__.lower(): obj, 
                    "admin_object": obj, 
                    "detail": True, 
                    'comments': comments, 
                    'comment_form': comment_form}

        return render(request, self.template, context)

    def post(self, request, id, slug):

        post = get_object_or_404(Post, id=id, slug__iexact=slug)
        comments = Comment.objects.filter(post=post).order_by('-id')
        obj = get_object_or_404(self.model, slug__iexact=slug)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
                comment.save()
        else:
            comment_form = CommentForm()

        context = {self.model.__name__.lower(): obj, 
                    "admin_object": obj, 
                    "detail": True, 
                    'comments': comments, 
                    'comment_form': comment_form}

        if request.is_ajax():
            html = render_to_string('blog/comments.html', context, request=request)
            return JsonResponse({'form': html})

        return render(request, self.template, context)


""" СОЗДАНИЕ ПОСТОВ """

class PostCreate(View):
    template = 'blog/post_create_form.html'

    def get(self, request):
        form = PostForm()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
        else:
            form = PostForm()
            return redirect(new_post)
        return render(request, self.template, context={'form': bound_form})
    raise_exception = True


""" РЕДАКТИРОВАНИЕ ПОСТОВ """
class PostUpdate(View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})



""" УДАЛЕНИЕ ПОСТОВ """

class PostDelete(View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'post_list_url'
    raise_exception = True

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
    

''' ВЬЮХИ ДЛЯ РЕГИСТРАЦИИ ВХОДА И ВЫХОДА ПОЛЬЗОВАТЕЛЕЙ '''

def signup(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        if body['password'] == body['confirm_password']:
            user = User(username=body["username"])
            user.set_password(body['password'])
            user.save()
            username = body["username"]
            password = body["password"]  
            user_login = authenticate(username=username, password=password)

            if user_login is not None:
                auth.login(request, user_login)
                return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"password_error": "fail"})
    return JsonResponse({'status':'false'})


def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if request.method == 'POST':
        username = body["username"]
        password = body["password"]   
        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


def logout(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body["logout"] == "logout":
        auth.logout(request)
        return JsonResponse({"status": "logout"})
    return HttpResponseRedirect(reverse("/blog/#"))


''' ОБЩИЙ ЧАТ '''
def chat(request):
    model = Chat
    template = 'blog/chat_page.html'

    chat_messages = Chat.objects.all()

    if request.method == 'POST':
        chat_form = ChatForm(request.POST or None)
        if chat_form.is_valid():
            message = request.POST.get('message')
            messages = Chat.objects.create(user=request.user, message=message)
            messages.save()
    else:
        chat_form = ChatForm()

    context = {
            "detail": True, 
            'chat_messages': chat_messages, 
            'chat_form': chat_form}

    if request.is_ajax():
        html = render_to_string('blog/chat.html', context, request=request)
        return JsonResponse({'form': html})
    
    return render(request, template, context)
    

''' ЛИЧНЫЕ СООБЩЕНИЯ '''
class ChatRoom(View):
    model = RoomChat
    template = 'blog/room.html'
    cr_all = RoomChat.objects.all()

    def get(self, request):
        users_list = User.objects.all()
        room_form = RoomForm()
        com = User.objects.order_by('-id')

        if request.method == 'GET':

            user_auth = request.GET.get('user_auth',)
            value = request.GET.get('value',)

            if user_auth != None and value != None:
                if (self.cr_all.filter(user_1__id=user_auth) and self.cr_all.filter(user_2__id=value)) or (self.cr_all.filter(user_1__id=value) and self.cr_all.filter(user_2__id=user_auth)):

                    us_1 = int(user_auth)
                    us_2 = int(value)

                    for p in RoomChat.objects.raw('SELECT id FROM blog_roomchat WHERE (user_1_id=%s AND user_2_id=%s) OR (user_1_id=%s AND user_2_id=%s)', [us_1, us_2, us_2, us_1]):
                        active_room = p.id

                    messages = MessageChatRoom.objects.filter(room=active_room)
                    l = MessageChatRoom.objects.filter(room=active_room).count()
                    data = serializers.serialize('json', messages, fields=('content', 'user', 'timestamp'))

                    return JsonResponse(data, safe=False)

                else:
                    us_1 = int(user_auth)
                    us_2 = int(value)

                    user_auth = User.objects.get(id=us_1)
                    user_click = User.objects.get(id=us_2)

                    n = RoomChat.objects.create(user_1=user_auth, user_2=user_click)
                    n.save()
                    active_room = n.id

                    return JsonResponse({"active_room": active_room})

            else:
                print("Error")

        context = {
                "users_list": users_list,
                'room_form': room_form,
                'com': com,
                }

        return render(request, self.template, context)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        users_list = User.objects.all()
        com = User.objects.order_by('-id')

        if request.method == 'POST':
            
            if (self.cr_all.filter(user_1__id=body["user_auth"]) and self.cr_all.filter(user_2__id=body["value"])) or (self.cr_all.filter(user_1__id=body["value"]) and self.cr_all.filter(user_2__id=body["user_auth"])):
               
                us_1 = User.objects.get(id=int(body["user_auth"]))
                us_2 = User.objects.get(id=int(body["value"]))

                for p in RoomChat.objects.filter(user_1_id=us_1, user_2_id=us_2) | RoomChat.objects.filter(user_1_id=us_2, user_2_id=us_1):
                    active_room = p.id

                content = str(body["message"])
                message = MessageChatRoom.objects.create(room=p, user=us_1, content=content)
                message.save()
                user = str(message.user).title()
                timestamp = str(message.timestamp)[:19]

                return JsonResponse({"active_room": active_room, 'content': content, "user": user, "timestamp": timestamp})
        else:
            room_form = RoomForm()

        context = {
                "users_list": users_list,
                'room_form': room_form,
                'com': com,
                'active_room': active_room,
                }

        return render(request, self.template, context)