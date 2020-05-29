from django.urls import path
from . import views


urlpatterns = [
    #     path('', views.home, name='home'),
    path('', views.BoardListView.as_view(), name='home'),
    path('boards_topic/<int:pk>/', views.boards_topic, name='boards_topic'),
    path('boards_topic/<int:pk>/new/', views.new_topic, name='new_topic'),

    path('boards_topic/<int:pk>/topics/<int:topic_id>/',
         views.topic_posts, name='topic_posts'),

    path('boards_topic/<int:pk>/topics/<int:topic_id>/reply/',
         views.topic_reply, name='topic_reply'),

    path('boards_topic/<int:pk>/topics/<int:topic_id>/posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),


]
