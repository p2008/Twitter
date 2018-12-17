from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import FormView, ListView

from twitter_app.models import Tweet


class AllTweetsView(ListView):
    """Show all tweets"""
    model = Tweet
    template_name = 'twitter_app/all_tweets.html'


class UserPostsView(FormView):
    """Show user's all tweets and comments under every tweet.
    Message send button to that user"""
    pass


class PostDetailView(FormView):
    """Show post, author, comments, create comment form"""
    pass


class UserEditView(FormView):
    """User edition page. Allowed for logged user"""
    pass


class UserMessagesView(View):
    """Messages sent and received by user. Max length character limit 30
    Unread messages have to be marked"""
    pass


class MessageDetailView(View):
    """May be integrated with UserMessages"""
    pass
