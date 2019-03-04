from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from datetime import datetime, date, time
from django.utils.text import slugify
from django.shortcuts import reverse
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.db import models
from time import time


''' ПОСТЫ '''
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('post_detail_url', args=[self.id, self.slug])

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    # для автоматического создания слага
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title) # или return self.title

    # для пагинации постов
    class Meta:
        ordering = ["-date_pub"]

''' ИЗОБРАЖЕНИЯ К ПОСТАМ '''

class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.post.title + " Image"

''' ТЕГИ '''
class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title) # или return self.title

    class Meta:
        ordering = ["title"]


''' ГЕНЕРАТОР SLUG '''
def gen_slug(s):
    new_slug = slugify(s, allow_unicode = True)
    return new_slug + '-' + str(int(time()))


''' ПОЛЬЗОВАТЕЛИ '''
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30, default="pass")


from django.contrib.auth.models import User


''' ЧАТ '''
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(max_length=160, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    is_readed = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return "{}-{}".format(self.timestamp, str(self.user.username))


''' КОММЕНТАРИИ '''
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)
    content = models.TextField(max_length=160, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return "{}-{}".format(self.post.title, str(self.user.username))


''' ЛИЧНЫЕ СООБЩЕНИЯ '''
class RoomChat(models.Model):
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_id')

    def __str__(self):
        return str(self.id)

class MessageChatRoom(models.Model):
    room = models.ForeignKey(RoomChat, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=200, null=True)
    status = models.BooleanField("Read", default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    def __str__(self):
        return str(self.room) + ' - ' + str(self.user.username) + ' (' + str(self.timestamp) + ') - ' + str(self.content)