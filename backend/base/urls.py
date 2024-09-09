from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),

    path("profile/<int:pk>", views.user_profile, name="profile"),
    path("profile/update", views.update_user, name="update-user"),

    path('', views.home, name='home'),

    path("topics/", views.topics_page, name="topics"),
    path("activity/", views.activity_page, name="activity"),

    path('room/<int:pk>', views.room, name='room'),
    path('room/create/', views.create_room, name='create-room'),
    path('room/<int:pk>/update/', views.update_room, name='update-room'),
    path('room/<int:pk>/delete/', views.delete_room, name='delete-room'),
    path('room/message/<int:pk>/delete/',
         views.delete_message,
         name='delete-message'),
]
