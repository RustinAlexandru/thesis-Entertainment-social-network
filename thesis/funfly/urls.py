from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from forms import CustomAuthenticationForm
from funfly.models import Joke
from funfly.views import VideoPostDetails, VideosList, JokesList, JokePostDetails, NinegagPostDetails, NinegagsList
from . import views

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', auth_views.login, {
                      'template_name': 'funfly/login.html',
                      'authentication_form': CustomAuthenticationForm
                      }, name='login'),
                  url(r'^logout/$', auth_views.logout,
                      {'next_page': reverse_lazy('index')}, name='logout'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^$', views.index, name='index'),
                  url(r'^jokes/$', JokesList.as_view(model=Joke), name='jokes'),
                  url(r'^videos/$', VideosList.as_view(template_name='videos.html'), name='videos'),
                  url(r'ninegags/$', NinegagsList.as_view(template_name='ninegags.html'), name='ninegags'),
                  url(r'^video_post/(?P<pk>\d+)/$', VideoPostDetails.as_view(template_name='video_post.html'),
                      name='video_post_details'),
                  url(r'joke_post/(?P<pk>\d+)/$', JokePostDetails.as_view(template_name='joke_post.html'),
                      name='joke_post_details'),
                  url(r'ninegag_post/(?P<pk>\d+)/$', NinegagPostDetails.as_view(template_name='ninegag_post.html'),
                      name='ninegag_post_details'),
                  url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
                  url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
