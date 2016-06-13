# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.list import ListView
from el_pagination.views import AjaxListView

from forms import RegisterForm, CommentForm
from models import Ninegag, UserProfile, Joke, Youtube, PostComment


# from youtube_parsing import youtube_search

def index(request):
    left_8_items = Ninegag.objects.order_by('-pk')[:8]
    left_6_jokes = Joke.objects.order_by('-pk')[:6]
    left_4_videos = Youtube.objects.order_by('-pk')[:4]
    context = {
        'items': left_8_items,
        'jokes': left_6_jokes,
        'videos': left_4_videos,
    }
    return render(request, 'funfly/layout.html', context)

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'RegisterForm': form
        }
        return render(request, 'funfly/register.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            sex = form.cleaned_data["sex"]
            city = form.cleaned_data["city"]
            timezone = form.cleaned_data["timezone"]

            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            profile = UserProfile.objects.create(user=user, sex=sex, city=city, timezone=timezone)

            user_auth = authenticate(username=username, password=password)

            if user_auth is None:
                return redirect('login')
            else:
                login(request, user_auth)
                return redirect('index')
        else:
            context = {
                'RegisterForm': form
            }
            return render(request, 'funfly/register.html', context)


class VideoPostDetails(DetailView):
    model = Youtube

    def get_context_data(self, **kwargs):
        context = super(VideoPostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Youtube.objects.get(pk=pk).youtube_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            youtube_post = Youtube.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=youtube_post, user=user)
            return redirect(reverse('video_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('video_post_details', kwargs={'pk': self.kwargs['pk']}))


class JokePostDetails(DetailView):
    model = Joke

    def get_context_data(self, **kwargs):
        context = super(JokePostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Joke.objects.get(pk=pk).joke_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            joke_post = Joke.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=joke_post, user=user)
            return redirect(reverse('joke_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('joke_post_details', kwargs={'pk': self.kwargs['pk']}))


class NinegagPostDetails(DetailView):
    model = Ninegag

    def get_context_data(self, **kwargs):
        context = super(NinegagPostDetails, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            # context['comments'] = PostComment.objects.filter(content_type__postcomment__object_id=pk)
            comments = Ninegag.objects.get(pk=pk).nine_gag_comments.all()
            context['comments'] = comments
        context['CommentForm'] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            message = form.cleaned_data['text']
            pk = self.kwargs['pk']
            user = self.request.user
            ninegag_post = Ninegag.objects.get(pk=pk)
            PostComment.objects.create(text=message, content_object=ninegag_post, user=user)
            return redirect(reverse('ninegag_post_details', kwargs={'pk': pk}))
        else:
            return redirect(reverse('ninegag_post_details', kwargs={'pk': self.kwargs['pk']}))

class VideosList(ListView):
    model = Youtube
    context_object_name = 'videos'
    paginate_by = 5


class NinegagsList(ListView):
    model = Ninegag
    context_object_name = 'ninegags'
    paginate_by = 5

class JokesList(AjaxListView):
    model = Joke
    context_object_name = 'jokes'
    template_name = 'jokes.html'
    page_template = 'joke_list.html'

@login_required
def comment_approve(request, pk):
    comment = PostComment.objects.get(pk=pk)
    if request.user.has_perm('Can change post comment'):
        comment.approve()
    if comment.content_type.model == 'joke':
        return redirect('joke_post_details', pk=comment.object_id)
    elif comment.content_type.model == 'ninegag':
        return redirect('ninegag_post_details', pk=comment.object_id)
    return redirect('video_post_details', pk=comment.object_id)


@login_required
def comment_remove(request, pk):
    comment = PostComment.objects.get(pk=pk)
    post_pk = comment.object_id
    if request.user.has_perm(('Can change post comment')):
        comment.delete()
    if comment.content_type.model == 'joke':
        return redirect('joke_post_details', pk=comment.object_id)
    elif comment.content_type.model == 'ninegag':
        return redirect('ninegag_post_details', pk=comment.object_id)
    return redirect('video_post_details', pk=post_pk)
