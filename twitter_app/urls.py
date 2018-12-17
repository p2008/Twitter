"""Twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from twitter_app.views import *

urlpatterns = [
    path('index/', AllTweetsView.as_view(), name='home-page'),
    path('/', include('twitter_app.user_auth.urls')),
    path('<int:uid>/posts/', UserPostsView.as_view(), name='user-posts'),
    path('<int:pid>/', PostDetailView.as_view(), name='post-details'),
    path('<int:uid>/edit/', UserEditView.as_view(), name='user-edit'),
    path('<int:uid>/messages/', UserMessagesView.as_view(), name='user-messages'),
    path('<int:mid>/', MessageDetailView.as_view(), name='message-details'),

]
