from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django_filters.views import FilterView

from forms import CustomAuthenticationForm
from funfly.models import Joke, Youtube, Ninegag
from funfly.views import VideoPostDetails, VideosList, JokesList, JokePostDetails, NinegagPostDetails, NinegagsList
from . import views
from views import anonymous_required, ViewProfile



urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', anonymous_required(auth_views.login), {
                      'template_name': 'funfly/login.html',
                      'authentication_form': CustomAuthenticationForm
                  }, name='login'),
                  url(r'^logout/$', auth_views.logout,
                      {'next_page': reverse_lazy('index')}, name='logout'),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^about/$', views.about, name='about'),
                  url(r'^profile/(?P<pk>\d+)/$', ViewProfile.as_view(template_name='view_profile.html'),
                      name='view_profile'),
                  url(r'^profile/(?P<pk>\d+)/follow/$', views.follow_user, name='follow'),
                  url(r'^profile/edit/(?P<pk>\d+)/$',
                      login_required(views.UpdateProfile.as_view(template_name='update_profile.html')),
                      name='edit_profile'),
                  url(r'^$', views.index, name='index'),
                  url(r'.*search/', include('haystack.urls')),
                  url(r'^jokes/$', JokesList.as_view(model=Joke), name='jokes'),
                  url(r'^videos/$', VideosList.as_view(template_name='videos.html'), name='videos'),
                  url(r'ninegags/$', NinegagsList.as_view(), name='ninegags'),
                  url(r'^video_post/(?P<pk>\d+)/$', VideoPostDetails.as_view(template_name='video_post.html'),
                      name='video_post_details'),
                  url(r'joke_post/(?P<pk>\d+)/$', JokePostDetails.as_view(template_name='joke_post.html'),
                      name='joke_post_details'),
                  url(r'ninegag_post/(?P<pk>\d+)/$', NinegagPostDetails.as_view(template_name='ninegag_post.html'),
                      name='ninegag_post_details'),
                  url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
                  url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
                  url(r'add/$', views.add_item, name='add_item'),
                  url(r'saved_items/$', views.saved_items_list, name='saved_items_list'),
                  url(r'saved_items_settings/$', views.saved_items_list_settings, name='saved_items_list_settings'),
                  url(r'.*add_to_savelist/$', views.add_item_to_savelist, name='add_item_to_savelist'),
                  url(r'.*like/$', views.like_item, name='like_item'),
                  url(r'.*add_point/$', views.add_point, name='add_point'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
