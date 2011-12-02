from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('core',
	url(r'^$', 'views.home', name='home'),
    url(r'^api/$', 'views.api_doc', name='api_doc'),
	url(r'^story/$', 'views.stories', name='stories'),
    url(r'^story.(?P<format>json)$', 'views.stories', name='stories'),
	url(r'^story/(?P<story_id>\d+)/comments/$', 'views.comments', name='comments'),
	url(r'^story/(?P<story_id>\d+)/comments/(?P<page>\d+)/$', 'views.comments', name='comments_page'),
    url(r'^story/(?P<story_id>\d+)/comments/(?P<page>\d+).(?P<format>json)$', 'views.comments', name='comments_page'),
)
