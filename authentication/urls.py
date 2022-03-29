from django.urls import path
from . import views

urlpatterns = [
    path('', views.HelloAuthView.as_view(), name="hello_auth"),
    path('signup/', views.UserCreateView.as_view(), name='sign_up'),
    path('email-verification/', views.verifyEmail.as_view(), name='email_verification'),  
    path('update-username/<int:user_id>', views.updateUsername.as_view(), name='update_username'),
]

