from django.urls import path

from users.views import LoginVeiw, RegisterView, UsersProfileView, LogoutView, EditProfile

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginVeiw.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UsersProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfile.as_view(), name='profile_edit'),
]
