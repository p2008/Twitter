from django.urls import path
from twitter_app.user_auth.views import LoginUserView, \
    LogoutUserView, CreateUserView, ResetPasswordView, ChangePasswordView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name="login"),
    path('logout/', LogoutUserView.as_view(), name="logout"),
    path('reset/<int:uid>/', ResetPasswordView.as_view(), name="reset"),
    path('change/<int:uid>/', ChangePasswordView.as_view(), name="change"),
    path('create_user/', CreateUserView.as_view(), name="create-user"),
]
