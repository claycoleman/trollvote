"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^nimda/', include(admin.site.urls)),
    url(r'^candidate_detail/(?P<pk>\d+)/$', 'app.views.candidate_detail_view', name='candidate_detail_view'),
    url(r'^candidate_list/$', 'app.views.candidate_list_view', name='candidate_list_view'),
    url(r'^candidate_delete/(?P<pk>\d+)/$', 'app.views.candidate_delete_view', name='candidate_delete_view'),
    url(r'^candidate_update/(?P<pk>\d+)/$', 'app.views.candidate_update_view', name='candidate_update_view'),
    url(r'^candidate_create/$', 'app.views.candidate_create_view', name='candidate_create_view'),
    url(r'^comment_detail/(?P<pk>\d+)/$', 'app.views.comment_detail_view', name='comment_detail_view'),
    url(r'^comment_list/$', 'app.views.comment_list_view', name='comment_list_view'),
    url(r'^user_detail/(?P<pk>\d+)/$', 'app.views.user_detail_view', name='user_detail_view'),
    url(r'^user_list/$', 'app.views.user_list_view', name='user_list_view'),
    url(r'^comment_delete/(?P<pk>\d+)/$', 'app.views.comment_delete_view', name='comment_delete_view'),
    url(r'^comment_update/(?P<pk>\d+)/$', 'app.views.comment_update_view', name='comment_update_view'),
    url(r'^political_party_detail/(?P<pk>\d+)/$', 'app.views.political_party_detail_view', name='political_party_detail_view'),
    url(r'^political_party_list/$', 'app.views.political_party_list_view', name='political_party_list_view'),
    url(r'^political_party_delete/(?P<pk>\d+)/$', 'app.views.political_party_delete_view', name='political_party_delete_view'),
    url(r'^political_party_update/(?P<pk>\d+)/$', 'app.views.political_party_update_view', name='political_party_update_view'),
    url(r'^political_party_create/$', 'app.views.political_party_create_view', name='political_party_create_view'),
    url(r'^user_update/(?P<pk>\d+)/$', 'app.views.user_update_view', name='user_update_view'),
    url(r'^user_delete/(?P<pk>\d+)/$', 'app.views.user_delete_view', name='user_delete_view'),
    url(r'^signup/$', 'app.views.signup', name='signup_view'),
    url(r'^login_view/$', 'app.views.login_view', name='login_view'),
    url(r'^logout_view/$', 'app.views.logout_view', name='logout_view'),
    url(r'^candidate_response/$', 'app.views.candidate_response', name='candidate_response'),
    url(r'^vote_up/$', 'app.views.vote_up', name='vote_up'),
    url(r'^vote_down/$', 'app.views.vote_down', name='vote_down'),
    url(r'^race_delete/(?P<pk>\d+)/$', 'app.views.race_delete_view', name='race_delete_view'),
    url(r'^race_update/(?P<pk>\d+)/$', 'app.views.race_update_view', name='race_update_view'),
    url(r'^race_create/$', 'app.views.race_create_view', name='race_create_view'),
    url(r'^race_detail/(?P<pk>\d+)/$', 'app.views.race_detail_view', name='race_detail_view'),
    url(r'^race_list/$', 'app.views.race_list_view', name='race_list_view'),
    url(r'^race_list/choose-state/$', 'app.views.choose_state_race_view', name='choose_state_race_view'),
    url(r'^race_list/(?P<slug>.+)/$', 'app.views.state_race_list_view', name='state_race_list_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
