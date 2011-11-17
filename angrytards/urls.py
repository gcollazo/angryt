from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('core',
	url(r'^$', 'views.home', name='home'),
	url(r'^story/$', 'views.stories', name='stories'),
	url(r'^story/(?P<story_id>\d+)/comments/$', 'views.comments', name='comments'),
	url(r'^story/(?P<story_id>\d+)/comments/(?P<page>\d+)/$', 'views.comments', name='comments_page'),
)
