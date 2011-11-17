from BeautifulSoup import BeautifulStoneSoup
from django.http import HttpResponse
import urllib2
import json

def home(request):
	return HttpResponse('Home')

def stories(request):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open('http://feeds.feedburner.com/elnuevodia/noticias')
	
	soup = BeautifulStoneSoup(f.read())

	stories = []
	for item in soup.findAll('item'):
		stories.append({
			'title':item.title.contents[0],
			'url':item.guid.contents[0],
			'id':item.guid.contents[0].split('/')[-1].split('.')[0].split('-')[-1],
			'comments':'/story/%s/comments/' % item.guid.contents[0].split('/')[-1].split('.')[0].split('-')[-1]
		})

	return HttpResponse(json.dumps(stories), mimetype='application/json')

def comments(request, story_id, page=None):
	base_url = 'http://www.elnuevodia.com/XStatic/endi/template/cargaListaComentarios.aspx?intConfigurationId=12275&intElementId=%s'
	print story_id
	print page
	print

	return HttpResponse('Comments')