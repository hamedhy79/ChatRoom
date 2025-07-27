from django.urls import path # type: ignore
from .import views

urlpatterns = [
    path('login/',views.LoginUser, name='login'),
    path('logout/',views.LogoutUser, name='logout'),
    path('register/',views.RegisterUser, name='register'),
     
    path('', views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path('create-room/', views.CreateRoom, name='create_room'),
    path('user-profile/<str:pk>/', views.UserProfile, name='user_profile'),
    path('update-room/<str:pk>/', views.UpdateRoom, name='update_room'),
    path('delete-room/<str:pk>/', views.DeleteRoom, name='delete_room'),
    path('delete-message/<str:pk>/', views.DdeleteMessage, name='delete_message'),
    path('update-user/', views.updateUser, name='update_user'),
    
    path('topics/', views.topicspage, name='topics'),
    path('activity/', views.activities, name='activity'),
]