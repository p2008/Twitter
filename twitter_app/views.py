from pprint import pprint

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DetailView, UpdateView

from twitter_app.forms import AddTweetForm, AddCommentForm, AddMessageForm, \
    UserProfileForm
from twitter_app.models import Tweet, Comment, Message
from twitter_app.user_auth.views import APP_NAME


class AllTweetsView(LoginRequiredMixin, View):
    """Show all tweets and add new tweet form"""
    tweets = Tweet.objects.all().order_by('-creation_date')
    ctx = {'tweets': tweets}

    def get(self, request):
        form = AddTweetForm()
        self.ctx['form'] = form
        return render(request, f'{APP_NAME}/all_tweets.html', self.ctx)

    def post(self, request):
        form = AddTweetForm(request.POST)

        if form.is_valid():
            new_tweet = Tweet()
            new_tweet.content = form.cleaned_data.get('content')
            new_tweet.author = request.user
            new_tweet.save()

            form.content = ''
            self.ctx['form'] = form

            return render(request, f'{APP_NAME}/all_tweets.html', self.ctx)
        return render(request, f'{APP_NAME}/all_tweets.html', self.ctx)


class UserTweetsView(LoginRequiredMixin, View):
    """Show user's all tweets and comments under every tweet.
    Message send button to that user"""
    def get(self, request, uid):
        form = AddMessageForm()
        tweets = Tweet.objects.filter(author=uid).order_by('-creation_date')
        ctx = {'tweets': tweets,
               'form': form}
        print(tweets)
        if tweets:
            return render(request, f'{APP_NAME}/all_tweets.html', ctx)
        messages.info(request, 'Nie masz jeszcze tweetów')
        return redirect(reverse('home-page'))

    def post(self, request, uid):
        form = AddMessageForm(request.POST)
        tweets = Tweet.objects.filter(author=uid).order_by('-creation_date')
        pprint(tweets)
        ctx = {'tweets': tweets,
               'form': form,
               'message': True}

        if form.is_valid():
            user_from = request.user
            user_to = get_object_or_404(User, id=uid)
            if user_from == user_to:
                form.add_error('user_to', 'Nie możesz wysłać wiadomości do siebie')
            else:
                new_message = Message()
                new_message.content = form.cleaned_data.get('content')
                new_message.user_from = user_from
                new_message.user_to = user_to
                new_message.read = False
                new_message.save()
                messages.success(request, 'Wiadomość wysłana')

                form.content = ''
                ctx['form'] = form

        return render(request, f'{APP_NAME}/all_tweets.html', ctx)


class TweetDetailView(LoginRequiredMixin, View):
    """Show post, author, comments, create comment form"""
    def get(self, request, tid):
        form = AddCommentForm()
        tweet = Tweet.objects.get(pk=tid)
        ctx = {'tweets': (tweet,),
               'form': form}

        return render(request, f'{APP_NAME}/all_tweets.html', ctx)

    def post(self, request, tid):
        form = AddCommentForm(request.POST)
        tweet = Tweet.objects.get(pk=tid)
        ctx = {'tweets': (tweet,),
               'form': form}

        if form.is_valid():
            new_comment = Comment()
            new_comment.content = form.cleaned_data.get('content')
            new_comment.author = request.user
            new_comment.tweet = tweet
            new_comment.save()

            form.content = ''
            ctx['form'] = form

            return render(request, f'{APP_NAME}/all_tweets.html', ctx)
        return render(request, f'{APP_NAME}/all_tweets.html', ctx)


class UserEditView(LoginRequiredMixin, View):
    """User edition page. Allowed for logged user"""

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        ctx = {'form': form}

        return render(request, f'{APP_NAME}/all_tweets.html', ctx)

    def post(self,request):
        form = UserProfileForm(request.POST, instance=request.user)
        ctx = {'form': form}

        if form.is_valid():
            form.save()
            return redirect(reverse('home-page'))

        return render(request, f'{APP_NAME}/all_tweets.html', ctx)


class UserMessagesView(LoginRequiredMixin, View):
    """Messages sent and received by user. Max length character limit 30
    Unread messages have to be marked"""

    def get(self, request):
        uid = request.user
        messages_all = Message.objects.filter(Q(user_to=uid) | Q(user_from=uid))
        ctx = {'messages_all': messages_all}
        return render(request, f'{APP_NAME}/all_messages.html', ctx)


class MessageDetailView(LoginRequiredMixin, View):

    def get(self, request, mid):
        uid = request.user

        message = Message.objects.get(pk=mid)
        if message.user_to == uid or message.user_from == uid:
            ctx = {'message': message}
            return render(request, f'{APP_NAME}/message_detail.html', ctx)
        else:
            return redirect(reverse('user-messages'))
