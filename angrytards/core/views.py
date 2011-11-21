# encoding: utf-8
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
from django.shortcuts import render, redirect
from django.http import HttpResponse
import urllib2
import json
from datetime import datetime

def home(request):
	date = datetime.now()
	page_title = 'El Día: Los commentarios de elnuevodia.com: lo peor del internet, fácil de leer'
	return render(request,'home.html', locals())


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


def comments(request, story_id, page=None):
	date = datetime.now()
	page_title = 'El Día: Los commentarios de elnuevodia.com: lo peor del internet, fácil de leer'

	if page == None:
		return redirect('/story/%s/comments/1/' % story_id)
	
	count = get_comment_count(story_id)
	pages = count / 10
	if count % 10 > 0:
		pages = pages + 1
	
	comments = get_comment_page(story_id, count, page, pages, request.META['HTTP_HOST'])
	story = get_story_with_id(story_id)
	print story

	return render(request, 'comments.html', locals())

# Helpers
def get_story_with_id(story_id):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open('http://feeds.feedburner.com/elnuevodia/noticias')
	
	soup = BeautifulStoneSoup(f.read())

	for item in soup.findAll('item'):
		_story_id = item.guid.contents[0].split('/')[-1].split('.')[0].split('-')[-1]

		if _story_id == story_id:
			return {
				'title':item.title.contents[0],
				'url':item.guid.contents[0],
				'id':story_id,
			}


def get_comment_count(story_id):
	count_url = 'http://www.elnuevodia.com/XStatic/endi/template/cargaComentarios.aspx?intElementId=%s&intConfigurationId=12275&intOpcionId=0&blnMostrarForma=True&blnMostrarComentarios=True&blnModerarComentarios=True&strEmailComentarios='
	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(count_url % story_id)
	soup = BeautifulSoup(f.read())

	count = soup.findAll('span', attrs={'id': 'comentarios2'})[0].contents[0].lstrip().rstrip()
	return int(count)


def get_comment_page(story_id, count, page, pages, host):
	comment_url = 'http://www.elnuevodia.com/XStatic/endi/template/cargaListaComentarios.aspx?intConfigurationId=12275&intElementId=%s&p=%s'
	
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	f = opener.open(comment_url % (story_id, page))
	soup = BeautifulSoup(f.read())

	comentarios = soup.findAll('div', attrs={'class': 'comentarios'})

	comments = {
		'comments':[],
		'current_page': int(page),
		'pages': pages,
		'count':count
	}

	if pages > int(page):
		comments['next_page'] = 'http://%s/story/%s/comments/%s/' % (host, story_id, int(page) + 1)
	else:
		comments['next_page'] = None
	
	if int(page) != 1 :
		comments['prev_page'] = 'http://%s/story/%s/comments/%s/' % (host, story_id, int(page) - 1)
	else:
		comments['prev_page'] = None

	for c in comentarios:
		username = c.findAll('h2')[0].contents[-1].lstrip().rstrip()

		if username != 'No existen comentarios':
			comment = c.findAll('p', attrs={'class': 'copete clearfix'})[0].contents[0].lstrip().rstrip()
			
			the_comment = {
				'username':username,
				'comment':comment,
			}
			
			comments['comments'].append(the_comment)
		else:
			comments = []
	
	return comments
