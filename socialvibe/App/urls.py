from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('logout', views.logout_view, name='logout_view'),
    path('notifications', views.notifications_view, name='notifications'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('messages', views.messages_view, name='messages'),
    path('messages/<int:chat_user_id>/', views.messages_view, name='chat_with_user'),
    path('send_message/<int:receiver_id>/', views.send_message, name='send_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('profile', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='user_profile'),
    path('stories', views.stories_view, name='stories'),
    path('add_story', views.add_story, name='add_story'),
    path('settings', views.settings_view, name='settings'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]
