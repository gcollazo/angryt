from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
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
		story_id = item.guid.contents[0].split('/')[-1].split('.')[0].split('-')[-1]
		stories.append({
			'title':item.title.contents[0],
			'url':item.guid.contents[0],
			'id':story_id,
			'comments':'http://%s/story/%s/comments/' % (request.META['HTTP_HOST'], story_id)
		})

	return HttpResponse(json.dumps(stories), mimetype='application/json')

def comments(request, story_id, page=1):
	base_url = 'http://www.elnuevodia.com/XStatic/endi/template/cargaListaComentarios.aspx?intConfigurationId=12275&intElementId=%s&p=%s'
	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(base_url % (story_id, page))
	
	soup = BeautifulSoup(f.read())

	comentarios = soup.findAll('div', attrs={'class': 'comentarios'})

	comments = []
	for c in comentarios:
		username = c.findAll('h2')[0].contents[-1].replace('\r\n        ', '').replace('\r\n        ', '')
		comment = c.findAll('p', attrs={'class': 'copete clearfix'})[0].contents[0].replace('\r\n        ', '')
		
		comments.append({
			'username':username,
			'comment':comment
		})
		
	return HttpResponse(json.dumps(comments), mimetype='application/json')