#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Microservice for making podcast rss feed from vk.com audiogroup's walls
and rss feeds for aggregators
"""

import os
import re
import sys
from datetime import datetime
from libs.esvk.esvk import esVKWall
from libs.esrss.esrsslite import esRss
import libs.server.bottle as bottle
import libs.server.wsgiserver as wsgiserver

route = bottle.route
response = bottle.response
static = bottle.static_file

if len(sys.argv) >= 4:
    if sys.argv[3]:
        urlpref = sys.argv[3]
    else:
        urlpref = ''
else:
    urlpref = ''
if len(sys.argv) >= 3:
    if sys.argv[2]:
        host = sys.argv[2]
    else:
        host = 'localhost'
else:
    host = 'localhost'
if len(sys.argv) >= 2:
    if sys.argv[2]:
        port = int(sys.argv[1])
    else:
        port = 8080
else:
    port = 8080

audiopostfix = 'vk2podaudio'
if urlpref:
    localaudiourl = 'http://%s/%s' % (urlpref, audiopostfix)
else:
    localaudiourl = 'http://%s:%s/%s' % (host, str(port), audiopostfix)

vw = esVKWall()

def duration(sec):
    s = int(sec)
    dur = str(s / 60 % 60).zfill(2) + ':' + str(s % 60).zfill(2)
    if s > 360:
        dur = str(s / 60 / 60) + ':' + dur
    return dur

def wall2Pod(gname, localaudiourl=localaudiourl, count=20, offset=0):
    if gname:
        if int(count) > 100:
            count = 100
        group = vw.getGroup(gname)
        if group['is_closed'] == 0:
            photo = vw.getBiggestPhoto(group)
            if photo:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'], image_url=photo)
            else:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'])
            items = vw.getWall(gname, count, offset)['response']
            if items.has_key('items'):
                items = items['items']
            for i in items:
                content = ''
                if type(i) == dict:
                    if i.has_key('text'):
                        description = i['text']
                    if i.has_key('attachments'):
                        for a in i['attachments']:
                            for c in a.keys():
                                if c == 'photo':
                                    description = vw.getBiggestPhoto(a[c], True) + '<br>' + description
                            for c in a.keys():
                                if c == 'audio':
                                    if i.has_key('from_id'):
                                        link = 'https://vk.com/wall' + str(i['from_id']) + '_' + str(i['id'])
                                    elif i.has_key('owner_id'):
                                        link = 'https://vk.com/wall' + str(i['owner_id']) + '_' + str(['id'])
                                    else:
                                        link = ''
                                    if link:
                                        if not content:
                                            r = vw.s.get(link)
                                            if r.ok:
                                                content = r.content.replace('\n', ' ')
                                    oa_id = str(a[c]['owner_id']) + '_' + str(a[c]['id'])
                                    dur = re.findall('(?u)play_' + oa_id + '.*?_audio_duration">(.*?)<',
                                               content)
                                    if dur:
                                        dur = ' [%s]' % dur[0]
                                    else:
                                        dur = ''
                                    title = a[c]['artist'] + ' - ' + a[c]['title']
                                    rss.addItem(title=title + dur, description=description, link=link,
                                                enclosure_url=localaudiourl + '/' + oa_id + '/' + title + '.mp3',
                                                enclosure_type='audio/mpeg', pubDate=datetime.strftime(
                                                datetime.fromtimestamp(int(i['date'])), '%a, %d %b %Y %T'))
            return rss.Feed()
        else:
            print "ERROR: Group is closed"
            return ''

def wall2RSS(gname, localaudiourl=localaudiourl, count=20, offset=0):
    if gname:
        if int(count) > 100:
            count = 100
        group = vw.getGroup(gname)
        if group['is_closed'] == 0:
            photo = vw.getBiggestPhoto(group)
            if photo:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'], image_url=photo)
            else:
                rss = esRss(title=group['name'], link='http://vk.com/' + gname, description=group['description'])
            items = vw.getWall(gname, count, offset)['response']
            if items.has_key('items'):
                items = items['items']
            for i in items:
                if type(i) == dict:
                    title = ''
                    description = ''
                    if i.has_key('text'):
                        description = i['text']
                        title = description.split('\n')[0]
                    if i.has_key('from_id'):
                        link = 'https://vk.com/wall' + str(i['from_id']) + '_' + str(i['id'])
                    elif i.has_key('owner_id'):
                        link = 'https://vk.com/wall' + str(i['owner_id']) + '_' + str(['id'])
                    else:
                        link = ''
                    if i.has_key('attachments'):
                        for a in i['attachments']:
                            for c in a.keys():
                                if c == 'photo':
                                    description += vw.getBiggestPhoto(a[c], True) + '<br>'
                                if c == 'video':
                                    if a[c].has_key('description'):
                                        description += '</br><a href="%s"><img src="%s"></a></br>%s [VIDEO]' % (link,
                                                        vw.getBiggestPhoto(a[c]), a[c]['description'])
                                    else:
                                        description += '</br><a href="%s"><img src="%s"></a></br> [VIDEO]' % (link,
                                                        vw.getBiggestPhoto(a[c]))
                                if c == 'audio':
                                    # if a[c].has_key('duration'):
                                    #     dur = duration(a[c]['duration'])
                                    audiotitle = ''
                                    if a[c].has_key('title'):
                                        audiotitle = a[c]['title']
                                    if a[c].has_key('artist'):
                                        if audiotitle:
                                            audiotitle = a[c]['artist'] + ' - ' + audiotitle
                                        else:
                                            audiotitle = a[c]['artist']
                                    description += '<br><a href="%s">%s</a>' % (localaudiourl + '/' +
                                                    str(a[c]['owner_id']) + '_' + str(a[c]['id']) + '/' + audiotitle +
                                                    '.mp3', audiotitle)
                                if c == 'link':
                                    if a[c].has_key('description'):
                                        description += '</br>' + a[c]['description']
                                    if a[c].has_key('title'):
                                        ltitle = a[c]['title']
                                        if not title and len(i['attachments']) == 1:
                                            title = ltitle
                                    else:
                                        ltitle = ''
                                    if a[c].has_key('photo'):
                                        photo = vw.getBiggestPhoto(a[c]['photo'])
                                        if ltitle:
                                            description += '</br><a href="%s"><img src="%s" alt="%s"></a>' % (
                                            a[c]['url'], photo, ltitle)
                                        else:
                                            description += '</br><a href="%s"><img src="%s"></a>' % (
                                            a[c]['url'], photo)
                                    else:
                                        if ltitle:
                                            description += '</br><a href="%s">%s</a>' % (a[c]['url'], ltitle)
                                if c == 'doc':
                                    if a[c].has_key('title'):
                                        dtitle = a[c]['title']
                                    if a[c].has_key('ext'):
                                        if a[c]['ext'] == u'gif':
                                            photo = '<a href="%s">%s</br><img src="%s" alt="%s"></a>' % \
                                                    (a[c]['url'], dtitle, a[c]['url'], dtitle)
                                    if a[c].has_key('preview'):
                                        if a[c]['preview'].has_key('photo'):
                                            if dtitle and not photo:
                                                photo = '<a href="%s">%s</br><img src="%s" alt="%s"></a>' % \
                                                    (a[c]['url'], dtitle, vw.getBiggestPhoto(a[c]['preview']['photo']),
                                                    dtitle)
                                            else:
                                                if not photo:
                                                    photo = '<a href="%s"><img src="%s"></a>' % (a[c]['url'],
                                                            vw.getBiggestPhoto(a[c]['preview']['photo']))
                                        else:
                                            photo = ''
                                    else:
                                        photo = ''
                                    if photo:
                                        description += '<br>' + photo
                                    else:
                                        description += '<br><a href="%s">%s</a>' % (a[c]['url'], a[c]['title'])
                    if not (title and description):
                        title = '---'
                    rss.addItem(title=title, description=description, link=link,
                                pubDate=datetime.strftime(datetime.fromtimestamp(int(i['date'])), '%a, %d %b %Y %T'))
            return rss.Feed()
        else:
            print "ERROR: Group is closed"
            return ''

@route('/')
def root():
    return static(filename='index.html', root=os.path.join(os.path.curdir, 'static'), mimetype='text/html')

@route('/favicon.ico')
def get_favicon():
    return static(filename='favicon.ico', root=os.path.join(os.path.curdir, 'static'), mimetype='image/x-icon')

@route('/vk2pod/<query>')
@route('/vk2pod/<query>/<count:re:[0-9]+>')
@route('/vk2pod/<query>/<count:re:[0-9]+>/<offset:re:[0-9]+>')
def vk2podq(query='', count=10, offset=0):
    if query:
        response.headers['Content-Type'] = 'xml/application'
        return wall2Pod(query, localaudiourl=localaudiourl, count=count, offset=offset)
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

@route('/vk2rss/<query>')
@route('/vk2rss/<query>/<count>')
@route('/vk2rss/<query>/<count>/<offset>')
def vk2rssq(query='', count=10, offset=0):
    if query:
        response.headers['Content-Type'] = 'xml/application'
        return wall2RSS(query, localaudiourl=localaudiourl, count=count, offset=offset)
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

@route('/' + audiopostfix + '/<oa_id>', method='GET')
@route('/' + audiopostfix + '/<oa_id>/<title>', method='GET')
def audioStream(oa_id='', title=''):
    if oa_id:
        oa_id = oa_id.replace('.mp3', '')
        url = vw.getAudio(oa_id)
        headers = vw.s.head(url).headers
        for h in ['content-length', 'expires', 'content-type']:
            response.headers.append(h, headers[h])
        return vw.s.get(url, stream=True).raw
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

@route('/' + audiopostfix + '/<oa_id>', method='HEAD')
@route('/' + audiopostfix + '/<oa_id>/<title>', method='HEAD')
def audioHead(oa_id='', title=''):
    if oa_id:
        oa_id = oa_id.replace('.mp3', '')
        url = vw.getAudio(oa_id)
        return vw.s.head(url).raw
    else:
        response.headers['Content-Type'] = 'text/plain'
        return 'Empty request'

print 'Server will started on host %s and port %s' % (host, port)

bottle.debug(False)
wsgiapp = bottle.default_app()
httpd = wsgiserver.Server(wsgiapp, listen=host, port=port)
httpd.listen = host
httpd.port = port
httpd.serve_forever()

#TODO: repost
#TODO: player