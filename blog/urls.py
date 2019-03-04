from django.conf.urls.static import static
from django.views.generic import FormView
from django.conf.urls import url
from django.conf import settings
from django.urls import path
from .views import * 
from . import views

urlpatterns = [
    path('', posts_list, name="post_list_url"),

    path('post/create/', PostCreate.as_view(), name="post_create_url"),
    path('post/<int:id>/<str:slug>/', PostDetail.as_view(), name="post_detail_url"),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name="post_update_url"),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name="post_delete_url"),

    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('chat/', views.chat, name="chat"),
    path('room/', ChatRoom.as_view(), name="room"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)