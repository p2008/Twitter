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
    path('', include('twitter_app.user_auth.urls')),
    path('<int:uid>/tweets/', UserTweetsView.as_view(), name='user-tweets'),
    path('<int:tid>/tweet_detail/', TweetDetailView.as_view(), name='tweet-details'),
    path('user_edit/', UserEditView.as_view(), name='user-edit'),
    path('messages/', UserMessagesView.as_view(), name='user-messages'),
    path('<int:mid>/message_detail/', MessageDetailView.as_view(), name='message-detail'),

]
